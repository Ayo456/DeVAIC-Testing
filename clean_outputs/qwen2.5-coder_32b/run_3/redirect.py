class HTTPResponseException(Exception):

    def __init__(self, status_code: int, headers: dict, body: str=''):
        self.status_code = status_code
        self.headers = headers
        self.body = body
        super().__init__(f'HTTP Response: {status_code}')

    def __str__(self):
        header_str = '\n'.join((f'{k}: {v}' for k, v in self.headers.items()))
        return f'{self.status_code} HTTP Response\nHeaders:\n{header_str}\n\nBody:\n{self.body}'