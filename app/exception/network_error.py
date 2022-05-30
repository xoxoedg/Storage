class NetworkError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg
        super(NetworkError, self).__init__()