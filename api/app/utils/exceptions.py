# 自定义异常类
from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    """
    基础 API 异常类
    """
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=message)


class NotFoundException(BaseAPIException):
    """
    资源未找到异常
    """
    def __init__(self, message: str = "资源不存在"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class BadRequestException(BaseAPIException):
    """
    请求参数错误异常
    """
    def __init__(self, message: str = "请求参数错误"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)


class UnauthorizedException(BaseAPIException):
    """
    未授权异常
    """
    def __init__(self, message: str = "未授权访问"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)


class InternalServerException(BaseAPIException):
    """
    服务器内部错误异常
    """
    def __init__(self, message: str = "服务器内部错误"):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
