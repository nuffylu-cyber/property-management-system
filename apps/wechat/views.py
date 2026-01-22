"""
WeChat Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import WeChatUser, WeChatMessage
from .serializers import WeChatUserSerializer, WeChatOAuthSerializer, WeChatBindSerializer
from .services import WeChatService, WeChatPayService


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def wechat_verify(request):
    """
    微信服务器验证
    用于微信公众号配置验证
    """
    wechat_service = WeChatService()

    if request.method == 'GET':
        # 验证服务器配置
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')

        if wechat_service.verify_signature(signature, timestamp, nonce):
            return Response(echostr, content_type='text/plain')
        else:
            return Response('Verification failed', status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'POST':
        # 处理微信消息推送
        # TODO: 解析 XML，处理消息
        return Response({'message': 'Message received'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def wechat_oauth_url(request):
    """
    获取微信授权 URL
    前端调用此接口获取授权 URL，然后跳转
    """
    redirect_uri = request.GET.get('redirect_uri', f"{settings.SITE_URL}/api/wechat/callback/")
    state = request.GET.get('state', 'STATE')

    wechat_service = WeChatService()
    oauth_url = wechat_service.get_oauth_url(redirect_uri, state)

    return Response({'oauth_url': oauth_url})


@api_view(['GET'])
@permission_classes([AllowAny])
def wechat_callback(request):
    """
    微信授权回调
    处理微信授权后的回调
    """
    code = request.GET.get('code')
    state = request.GET.get('state')

    if not code:
        return Response({'error': '缺少授权 code'}, status=status.HTTP_400_BAD_REQUEST)

    wechat_service = WeChatService()

    # 通过 code 获取 access_token 和 openid
    auth_data = wechat_service.get_oauth_access_token(code)
    if not auth_data:
        return Response({'error': '获取授权信息失败'}, status=status.HTTP_400_BAD_REQUEST)

    openid = auth_data.get('openid')
    access_token = auth_data.get('access_token')

    # 获取用户信息
    user_info = wechat_service.get_user_info(openid, access_token)

    # 查找或创建微信用户
    wechat_user, created = WeChatUser.objects.get_or_create(
        openid=openid,
        defaults={
            'unionid': auth_data.get('unionid'),
            'nickname': user_info.get('nickname') if user_info else '',
            'avatar_url': user_info.get('headimgurl') if user_info else '',
            'sex': user_info.get('sex') if user_info else None,
            'city': user_info.get('city') if user_info else '',
            'province': user_info.get('province') if user_info else '',
            'country': user_info.get('country') if user_info else '',
        }
    )

    # 如果已经绑定了系统用户，直接返回 JWT token
    if wechat_user.user:
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(wechat_user.user)
        return Response({
            'message': '登录成功',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': WeChatUserSerializer(wechat_user).data,
        })

    # 否则返回 openid，前端引导用户绑定
    return Response({
        'message': '请先绑定账号',
        'openid': openid,
        'wechat_user': WeChatUserSerializer(wechat_user).data,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def wechat_bind(request):
    """
    微信用户绑定系统账号
    """
    serializer = WeChatBindSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    openid = request.data.get('openid')
    name = serializer.validated_data['name']
    id_card = serializer.validated_data['id_card']
    property_id = serializer.validated_data['property_id']

    # 查找业主
    from apps.property.models import Owner
    try:
        owner = Owner.objects.get(name=name, id_card=id_card)
    except Owner.DoesNotExist:
        return Response({'error': '未找到对应的业主信息'}, status=status.HTTP_404_NOT_FOUND)

    # 验证房产
    from apps.property.models import OwnerProperty
    try:
        owner_property = OwnerProperty.objects.get(owner=owner, property_id=property_id)
    except OwnerProperty.DoesNotExist:
        return Response({'error': '该房产不属于此业主'}, status=status.HTTP_400_BAD_REQUEST)

    # 查找微信用户
    try:
        wechat_user = WeChatUser.objects.get(openid=openid)
    except WeChatUser.DoesNotExist:
        return Response({'error': '未找到微信用户'}, status=status.HTTP_404_NOT_FOUND)

    # 如果业主还没有系统用户，创建一个
    if not owner.user:
        from apps.core.models import User
        user = User.objects.create_user(
            username=f"owner_{owner.id}",
            role='owner',
            phone=owner.phone,
            first_name=owner.name,
        )
        owner.user = user
        owner.save()

    # 绑定微信用户和系统用户
    wechat_user.user = owner.user
    wechat_user.save()

    # 更新业主的微信信息
    owner.wechat_openid = openid
    owner.wechat_nickname = wechat_user.nickname
    owner.avatar_url = wechat_user.avatar_url
    owner.is_verified = True
    owner.save()

    # 返回 JWT token
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(owner.user)

    return Response({
        'message': '绑定成功',
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': WeChatUserSerializer(wechat_user).data,
    })


class WeChatUserViewSet(viewsets.ReadOnlyModelViewSet):
    """微信用户管理视图集"""
    queryset = WeChatUser.objects.all()
    serializer_class = WeChatUserSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['is_subscribed']
    search_fields = ['nickname', 'openid']
    ordering = ['-created_at']


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wechat_jsapi_config(request):
    """
    获取微信 JS-SDK 配置
    前端调用此接口获取 JS-SDK 签名
    """
    url = request.GET.get('url')
    if not url:
        return Response({'error': '缺少 url 参数'}, status=status.HTTP_400_BAD_REQUEST)

    wechat_service = WeChatService()
    config = wechat_service.create_jsapi_signature(url)

    return Response(config)
