"""
WeChat Services
"""
import requests
import hashlib
import time
from django.conf import settings
from typing import Dict, Optional


class WeChatService:
    """微信公众号服务"""

    def __init__(self):
        self.app_id = settings.WECHAT.get('APP_ID')
        self.app_secret = settings.WECHAT.get('APP_SECRET')
        self.token = settings.WECHAT.get('TOKEN')
        self.encoding_aes_key = settings.WECHAT.get('ENCODING_AES_KEY')

        # API 端点
        self.access_token_url = 'https://api.weixin.qq.com/cgi-bin/token'
        self.user_info_url = 'https://api.weixin.qq.com/cgi-bin/user/info'
        self.oauth_code_url = 'https://open.weixin.qq.com/connect/oauth2/authorize'
        self.oauth_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        self.jsapi_ticket_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket'

    def get_access_token(self) -> Optional[str]:
        """
        获取公众号 access_token
        注意：生产环境应该使用缓存
        """
        params = {
            'grant_type': 'client_credential',
            'appid': self.app_id,
            'secret': self.app_secret,
        }

        try:
            response = requests.get(self.access_token_url, params=params, timeout=5)
            data = response.json()

            if 'access_token' in data:
                return data['access_token']
            else:
                print(f"获取 access_token 失败: {data}")
                return None
        except Exception as e:
            print(f"获取 access_token 异常: {e}")
            return None

    def get_user_info(self, openid: str, access_token: str = None) -> Optional[Dict]:
        """
        获取用户基本信息
        """
        if not access_token:
            access_token = self.get_access_token()

        if not access_token:
            return None

        params = {
            'access_token': access_token,
            'openid': openid,
            'lang': 'zh_CN',
        }

        try:
            response = requests.get(self.user_info_url, params=params, timeout=5)
            data = response.json()

            if 'errcode' in data and data['errcode'] != 0:
                print(f"获取用户信息失败: {data}")
                return None

            return data
        except Exception as e:
            print(f"获取用户信息异常: {e}")
            return None

    def get_oauth_url(self, redirect_uri: str, state: str = 'STATE') -> str:
        """
        获取网页授权 URL
        """
        params = {
            'appid': self.app_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'snsapi_userinfo',  # 获取用户详细信息
            'state': state,
        }

        # 构建授权 URL
        from urllib.parse import urlencode
        return f"{self.oauth_code_url}?{urlencode(params)}#wechat_redirect"

    def get_oauth_access_token(self, code: str) -> Optional[Dict]:
        """
        通过 code 换取网页授权 access_token
        """
        params = {
            'appid': self.app_id,
            'secret': self.app_secret,
            'code': code,
            'grant_type': 'authorization_code',
        }

        try:
            response = requests.get(self.oauth_token_url, params=params, timeout=5)
            data = response.json()

            if 'errcode' in data and data['errcode'] != 0:
                print(f"获取授权 access_token 失败: {data}")
                return None

            return data
        except Exception as e:
            print(f"获取授权 access_token 异常: {e}")
            return None

    def verify_signature(self, signature: str, timestamp: str, nonce: str) -> bool:
        """
        验证微信服务器签名
        """
        # 将 token、timestamp、nonce 三个参数进行字典序排序
        tmp_list = [self.token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)

        # 对三个参数字符串进行 sha1 加密
        tmp_str = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()

        # 将加密后的字符串与 signature 对比
        return tmp_str == signature

    def send_template_message(self, access_token: str, openid: str, template_id: str,
                              data: Dict, url: str = None) -> bool:
        """
        发送模板消息
        """
        api_url = f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'

        message_data = {
            'touser': openid,
            'template_id': template_id,
            'data': data,
        }

        if url:
            message_data['url'] = url

        try:
            response = requests.post(api_url, json=message_data, timeout=5)
            result = response.json()

            if result.get('errcode') == 0:
                return True
            else:
                print(f"发送模板消息失败: {result}")
                return False
        except Exception as e:
            print(f"发送模板消息异常: {e}")
            return False

    def create_jsapi_signature(self, url: str) -> Dict[str, str]:
        """
        生成 JS-SDK 签名
        用于前端调用微信 JS-SDK
        """
        import random
        import string

        # 获取 jsapi_ticket（这里简化处理，生产环境应该缓存）
        access_token = self.get_access_token()
        if not access_token:
            return {}

        params = {
            'access_token': access_token,
            'type': 'jsapi',
        }

        try:
            response = requests.get(self.jsapi_ticket_url, params=params, timeout=5)
            data = response.json()

            if data.get('errcode') != 0:
                return {}

            ticket = data.get('ticket')

            # 生成随机字符串
            nonce_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            timestamp = str(int(time.time()))

            # 生成签名
            sign_str = f'jsapi_ticket={ticket}&noncestr={nonce_str}&timestamp={timestamp}&url={url}'
            signature = hashlib.sha1(sign_str.encode('utf-8')).hexdigest()

            return {
                'appId': self.app_id,
                'timestamp': timestamp,
                'nonceStr': nonce_str,
                'signature': signature,
            }
        except Exception as e:
            print(f"生成 JS-SDK 签名异常: {e}")
            return {}


class WeChatPayService:
    """微信支付服务"""

    def __init__(self):
        self.mch_id = settings.WECHAT_PAY.get('MCH_ID')
        self.api_key = settings.WECHAT_PAY.get('API_KEY')
        self.notify_url = settings.WECHAT_PAY.get('NOTIFY_URL')
        self.order_url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'

    def create_order(self, openid: str, order_no: str, total_fee: int,
                     body: str, ip: str) -> Optional[Dict]:
        """
        创建微信支付订单
        total_fee: 单位为分
        """
        import random
        import string
        from django.conf import settings

        # 生成随机字符串
        nonce_str = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

        # 构建订单参数
        params = {
            'appid': settings.WECHAT.get('APP_ID'),
            'mch_id': self.mch_id,
            'nonce_str': nonce_str,
            'body': body,
            'out_trade_no': order_no,
            'total_fee': total_fee,
            'spbill_create_ip': ip,
            'notify_url': self.notify_url,
            'trade_type': 'JSAPI',
            'openid': openid,
        }

        # 生成签名
        sign = self._generate_sign(params)
        params['sign'] = sign

        # 构建 XML 请求体
        xml_data = self._dict_to_xml(params)

        try:
            response = requests.post(self.order_url, data=xml_data.encode('utf-8'),
                                    headers={'Content-Type': 'application/xml'},
                                    timeout=10)
            result = self._xml_to_dict(response.text)

            if result.get('return_code') == 'SUCCESS' and result.get('result_code') == 'SUCCESS':
                # 构建前端支付参数
                prepay_id = result.get('prepay_id')
                return self._build_jsapi_params(prepay_id)
            else:
                print(f"创建支付订单失败: {result}")
                return None
        except Exception as e:
            print(f"创建支付订单异常: {e}")
            return None

    def _generate_sign(self, params: Dict) -> str:
        """生成签名"""
        # 参数排序
        sorted_params = sorted(params.items())
        # 拼接字符串
        sign_str = '&'.join([f'{k}={v}' for k, v in sorted_params if v])
        sign_str += f'&key={self.api_key}'
        # MD5 加密
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()

    def _dict_to_xml(self, params: Dict) -> str:
        """字典转 XML"""
        xml = '<xml>'
        for k, v in params.items():
            xml += f'<{k}>{v}</{k}>'
        xml += '</xml>'
        return xml

    def _xml_to_dict(self, xml_str: str) -> Dict:
        """XML 转字典"""
        try:
            from xml.etree import ElementTree
            root = ElementTree.fromstring(xml_str)
            return {child.tag: child.text for child in root}
        except Exception as e:
            print(f"XML 解析失败: {e}")
            return {}

    def _build_jsapi_params(self, prepay_id: str) -> Dict:
        """构建前端 JSAPI 支付参数"""
        import random
        import string
        from django.conf import settings

        timeStamp = str(int(time.time()))
        nonceStr = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        package = f'prepay_id={prepay_id}'

        params = {
            'appId': settings.WECHAT.get('APP_ID'),
            'timeStamp': timeStamp,
            'nonceStr': nonceStr,
            'package': package,
            'signType': 'MD5',
        }

        sign = self._generate_sign(params)
        params['paySign'] = sign

        return params

    def verify_notify(self, xml_data: str) -> bool:
        """验证支付回调"""
        data = self._xml_to_dict(xml_data)

        if data.get('return_code') != 'SUCCESS':
            return False

        # 验证签名
        sign = data.pop('sign', None)
        calculated_sign = self._generate_sign(data)

        return sign == calculated_sign
