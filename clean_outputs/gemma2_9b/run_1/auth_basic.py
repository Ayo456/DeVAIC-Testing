def auth_basic(check_func):

    def decorator(handler):

        def inner(request):
            auth = request.headers.get('Authorization')
            if not auth:
                return (401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            try:
                user, password = auth.split(' ')[1].decode('base64').split(':')
            except:
                return (401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            if not check_func(user, password):
                return (401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            return handler(request)
        return inner
    return decorator