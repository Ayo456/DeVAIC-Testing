from functools import wraps
import falcon

def auth_basic(check_func):

    @wraps(check_func)
    def decorated(self, req, resp):
        try:
            auth_header = req.get_header('Authorization')
            if not auth_header:
                raise falcon.HTTPUnauthorized('Authentication required')
            auth_method, encoded_credentials = auth_header.split(' ', 1)
            if auth_method.lower() != 'basic':
                raise falcon.HTTPUnauthorized('Invalid authentication method')
            user, password = falcon.utils.base64_decode(encoded_credentials).strip().split(':')
            if not check_func(user, password):
                raise falcon.HTTPUnauthorized('Authentication failed')
            check_func(self, req, resp)
        except falcon.HTTPUnauthorized as e:
            resp.status = falcon.HTTP_401
            resp.body = 'Authentication required'
            resp.set_header('WWW-Authenticate', 'Basic realm="Example Realm"')
    return decorated