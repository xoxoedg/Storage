class NoDataStorageError(ValueError):
    def __init__(self, msg):
        self.msg = msg
        super(NoDataStorageError, self).__init__()

