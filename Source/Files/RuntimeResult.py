class RTResult:
    def __init__ (self):
        self.Value = None
        self.Error = None

    def Register (self, Result):
        self.Error = Result.Error

        return Result.Value

    def Success (self, Value):
        self.Value = Value

        return self

    def Failure (self, Error):
        self.Error = Error

        return self
