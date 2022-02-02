from flask import request

def get_request_data():
    """
    Get keys & values from request
    """
    return request.form