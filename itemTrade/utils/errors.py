from rest_framework.exceptions import APIException


class ValidationError(APIException):
    """自定义异常"""
    status_code = 200
    default_code = 0
    default_detail = "字段验证异常"

    def __init__(self, code=None, detail=None):
        if detail is None:
            detail = self.default_detail
        self.detail = {'message': detail, 'code': code or self.default_code}