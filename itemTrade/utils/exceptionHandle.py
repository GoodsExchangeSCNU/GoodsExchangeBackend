from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from .errors import ValidationError


def api_exception_handler(exc, context):
    """全局异常处理器"""
    # 调用默认的异常处理器以获取标准的响应
    response = exception_handler(exc, context)

    if isinstance(exc,ValidationError):
        return Response(exc.detail,status=exc.status_code)

    # 默认处理
    return response if response is not None else Response({
        'code': 502,
        'message': 'An unexpected error occurred.',
        'details': str(exc)
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

