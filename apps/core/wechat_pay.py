"""
微信支付服务
支持个人账号和企业对公账户的微信支付功能
"""
import hashlib
import time
import uuid
import xml.etree.ElementTree as ET
from decimal import Decimal
from datetime import datetime

from django.conf import settings
from apps.core.models import WeChatPayConfig


class WeChatPayService:
    """微信支付服务类"""

    def __init__(self, config=None):
        """
        初始化微信支付服务
        :param config: WeChatPayConfig实例
        """
        self.config = config or self._get_default_config()
        self.api_url = 'https://api.mch.weixin.qq.com'
        if self.config.account_type == 'personal':
            # 个人账号使用不同的API地址
            self.api_url = 'https://api2.mch.weixin.qq.com'

    def _get_default_config(self):
        """获取默认配置"""
        try:
            return WeChatPayConfig.objects.filter(account_type='enterprise').first()
        except:
            return None

    def create_payment_order(self, bill, client_ip):
        """
        创建支付订单
        :param bill: PaymentBill实例
        :param client_ip: 客户端IP
        :return: 支付订单数据或错误信息
        """
        if not self.config:
            return {
                'success': False,
                'error': '微信支付未配置'
            }

        try:
            # 生成商户订单号
            out_trade_no = f"PROP{bill.id.hex[:16].upper()}_{int(time.time())}"

            # 订单参数
            params = {
                'appid': self.config.app_id,
                'mch_id': self.config.mch_id,
                'nonce_str': self._generate_nonce_str(),
                'body': f'{bill.community.name}-{bill.billing_period}物业费',
                'out_trade_no': out_trade_no,
                'total_fee': int(bill.unpaid_amount * 100),  # 单位：分
                'spbill_create_ip': client_ip,
                'notify_url': self.config.notify_url or '',
                'trade_type': 'JSAPI',
                'openid': ''  # 需要从前端获取用户openid
            }

            # 生成签名
            params['sign'] = self._generate_sign(params)

            # 转换为XML
            xml_data = self._dict_to_xml(params)

            # 调用统一下单API
            import requests
            response = requests.post(
                f'{self.api_url}/pay/unifiedorder',
                data=xml_data.encode('utf-8'),
                headers={'Content-Type': 'application/xml'},
                verify=False  # 开发环境可以不验证证书
            )

            # 解析返回结果
            result = self._parse_xml_response(response.text)

            if result.get('return_code') == 'SUCCESS' and result.get('result_code') == 'SUCCESS':
                # 二维码链接
                code_url = result.get('code_url', '')
                prepay_id = result.get('prepay_id', '')

                return {
                    'success': True,
                    'out_trade_no': out_trade_no,
                    'code_url': code_url,
                    'prepay_id': prepay_id,
                    'order_data': result
                }
            else:
                return {
                    'success': False,
                    'error': result.get('return_msg', '创建支付订单失败')
                }

        except Exception as e:
            return {
                'success': False,
                'error': f'创建支付订单异常: {str(e)}'
            }

    def query_payment_status(self, out_trade_no):
        """
        查询支付状态
        :param out_trade_no: 商户订单号
        :return: 支付状态
        """
        if not self.config:
            return {
                'success': False,
                'error': '微信支付未配置'
            }

        try:
            params = {
                'appid': self.config.app_id,
                'mch_id': self.config.mch_id,
                'out_trade_no': out_trade_no,
                'nonce_str': self._generate_nonce_str()
            }

            params['sign'] = self._generate_sign(params)

            xml_data = self._dict_to_xml(params)

            import requests
            response = requests.post(
                f'{self.api_url}/pay/orderquery',
                data=xml_data.encode('utf-8'),
                headers={'Content-Type': 'application/xml'},
                verify=False
            )

            result = self._parse_xml_response(response.text)

            if result.get('return_code') == 'SUCCESS':
                trade_state = result.get('trade_state', '')
                status_map = {
                    'SUCCESS': '支付成功',
                    'REFUND': '转入退款',
                    'NOTPAY': '未支付',
                    'CLOSED': '已关闭',
                    'REVOKED': '已撤销（刷卡支付）',
                    'USERPAYING': '用户支付中',
                    'PAYERROR': '支付失败'
                }

                return {
                    'success': True,
                    'trade_state': trade_state,
                    'trade_state_desc': status_map.get(trade_state, '未知状态'),
                    'transaction_id': result.get('transaction_id', ''),
                    'total_fee': result.get('total_fee', '0'),
                    'time_end': result.get('time_end', ''),
                    'data': result
                }
            else:
                return {
                    'success': False,
                    'error': result.get('return_msg', '查询失败')
                }

        except Exception as e:
            return {
                'success': False,
                'error': f'查询支付状态异常: {str(e)}'
            }

    def _generate_nonce_str(self):
        """生成随机字符串"""
        return str(uuid.uuid4()).replace('-', '')[:32]

    def _generate_sign(self, params):
        """
        生成签名
        :param params: 参数字典
        :return: 签名字符串
        """
        # 参数排序
        sorted_params = sorted(params.items())

        # 拼接参数字符串
        stringA = '&'.join([f'{k}={v}' for k, v in sorted_params if v])

        # 拼接API密钥
        string_sign_temp = f'{stringA}&key={self.config.api_key}'

        # MD5签名
        sign = hashlib.md5(string_sign_temp.encode('utf-8')).hexdigest().upper()

        return sign

    def _dict_to_xml(self, params):
        """
        将字典转换为XML
        :param params: 参数字典
        :return: XML字符串
        """
        root = ET.Element('xml')
        for key, value in params.items():
            child = ET.SubElement(root, key)
            child.text = str(value)
        return ET.tostring(root, encoding='unicode')

    def _parse_xml_response(self, xml_str):
        """
        解析XML响应
        :param xml_str: XML字符串
        :return: 字典
        """
        root = ET.fromstring(xml_str)
        result = {}
        for child in root:
            result[child.tag] = child.text
        return result

    def verify_notify(self, xml_data):
        """
        验证支付回调通知
        :param xml_data: XML数据
        :return: 验证结果
        """
        try:
            result = self._parse_xml_response(xml_data)

            # 验证签名
            sign = result.pop('sign', '')
            calculated_sign = self._generate_sign(result)

            if sign != calculated_sign:
                return {
                    'success': False,
                    'error': '签名验证失败'
                }

            return {
                'success': True,
                'data': result
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'验证通知异常: {str(e)}'
            }


class WeChatPayJSAPI:
    """微信支付JSAPI相关功能"""

    @staticmethod
    def generate_jsapi_params(prepay_id, config=None):
        """
        生成JSAPI支付参数
        :param prepay_id: 预支付交易会话标识
        :param config: WeChatPayConfig实例
        :return: JSAPI参数
        """
        if not config:
            return None

        try:
            import time
            timestamp = str(int(time.time()))

            # 生成随机字符串
            nonce_str = str(uuid.uuid4()).replace('-', '')[:16]

            # 生成支付签名
            package = f'prepay_id={prepay_id}'
            sorted_params = sorted([
                ('appId', config.app_id),
                ('nonceStr', nonce_str),
                ('package', package),
                ('signType', 'MD5'),
                ('timeStamp', timestamp)
            ])

            stringA = '&'.join([f'{k}={v}' for k, v in sorted_params])
            string_sign_temp = f'{stringA}&key={config.api_key}'
            pay_sign = hashlib.md5(string_sign_temp.encode('utf-8')).hexdigest().upper()

            return {
                'appId': config.app_id,
                'timeStamp': timestamp,
                'nonceStr': nonce_str,
                'package': package,
                'signType': 'MD5',
                'paySign': pay_sign
            }

        except Exception as e:
            print(f"生成JSAPI参数异常: {e}")
            return None
