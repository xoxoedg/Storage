class NoDataError(ValueError):
    def __init__(self, msg):
        self.msg = msg
        super(NoDataError, self).__init__()

