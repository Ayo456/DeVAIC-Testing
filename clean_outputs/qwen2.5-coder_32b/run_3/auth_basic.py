def auth_basic(check, realm='private', text='Access denied'):

    def decorator(handler):

        def wrapper(*args, **kwargs):
            auth = request.auth
            if not auth or not check(*auth):
                response = HTTPError(401, text)
                response.add_header('WWW-Authenticate', f'Basic realm="{realm}"')
                return response
            return handler(*args, **kwargs)
        return wrapper
    return decorator