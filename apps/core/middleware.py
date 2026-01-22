"""
Custom Middleware
"""
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    请求日志中间件
    记录所有 API 请求
    """

    def process_request(self, request):
        """记录请求信息"""
        request_meta = request.META
        path = request.path
        method = request.method

        # 只记录 API 请求
        if path.startswith('/api/'):
            logger.info(f"{method} {path} from {request_meta.get('REMOTE_ADDR')}")

        return None
