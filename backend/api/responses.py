# api/responses.py

from rest_framework.response import Response

class CustomResponse(Response):
    def __init__(self, results=None, message=None, error=None, status=None, *args, **kwargs):
        if error is not None:
            response_data = {
                "error": error
            }
        else:
            response_data = {
                "message": message,
                "results": results
            }
        
        super().__init__(data=response_data, status=status, *args, **kwargs)
