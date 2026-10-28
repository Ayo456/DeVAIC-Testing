def auth_basic(check, realm='private', text='Access denied'):

    def decorator(handler):

        def wrapped(*args, **kwargs):
            if request.auth is None:
                return HTTPError(401, text).add_header('WWW-Authenticate', f'Basic realm="{realm}"')
            user, password = request.auth
            if not check(user, password):
                return HTTPError(401, text).add_header('WWW-Authenticate', f'Basic realm="{realm}"')
            return handler(*args, **kwargs)
        return wrapped
    return decorator