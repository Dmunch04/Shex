class ParseResult:
    def __init__ (self):
        self.Error = None
        self.Node = None
        self.LastRegisteredAdvanceCount = 0
        self.AdvanceCount = 0
        self.ToReverseCount = 0

    def RegisterAdvancement (self):
        self.LastRegisteredAdvanceCount = 1
        self.AdvanceCount += 1

    def Register (self, Result):
        self.LastRegisteredAdvanceCount = Result.AdvanceCount
        self.AdvanceCount += Result.AdvanceCount

        if Result.Error:
            self.Error = Result.Error

        return Result.Node

    def TryRegister (self, Result):
        if Result.Error:
            self.ToReverseCount = Result.AdvanceCount

            return None

        return self.Register (Result)

    def Success (self, Node):
        self.Node = Node

        return self

    def Failure (self, Error):
        if not self.Error or self.LastRegisteredAdvanceCount == 0:
            self.Error = Error

        return self
