class Position:
    def __init__ (self, Index, Line, Column, FileName, FileText):
        self.Index = Index
        self.Line = Line
        self.Column = Column
        self.FileName = FileName
        self.FileText = FileText

    def Advance (self, CurrentChar = None):
        self.Index += 1
        self.Column += 1

        if CurrentChar == '\n':
            self.Line += 1
            self.Column = 0

        return self

    def Copy (self):
        return Position (self.Index, self.Line, self.Column, self.FileName, self.FileText)
