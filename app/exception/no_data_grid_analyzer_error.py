class NoDataGridAnalyzerError(RuntimeError):

    def __init__(self, msg):
        self.msg = msg
        super(NoDataGridAnalyzerError, self).__init__()

