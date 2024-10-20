from fastapi import HTTPException,status

class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "server error"
    def __init__(self):
        super().__init__(status_code=self.STATUS_CODE,
                          detail = self.DETAIL)

class UserNotFoundException(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "User is not found"

class WeightNotFoundException(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "You haven't weight, please, first add the weight with create_weight funciton"