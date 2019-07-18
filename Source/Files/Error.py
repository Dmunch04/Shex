class Error:
    def __init__ (self, StartPosition, EndPosition, Name, Error):
        self.StartPosition = StartPosition
        self.EndPosition = EndPosition
        self.Name = Name
        self.Error = Error

    def AsString (self):
        Result = f'{self.Name}: {self.Error}\n'
        Result += f'File {self.StartPosition.FileName}, line {self.StartPosition.Line + 1}'
        Result += '\n\n' + StringWithArrows (self.StartPosition.FileText, self.StartPosition, self.EndPosition)

        return Result

class IllegalCharError (Error):
    def __init__ (self, StartPosition, EndPosition, Error):
        super ().__init__ (StartPosition, EndPosition, 'Illegal Character', Error)

class ExpectedCharError (Error):
    def __init__ (self, StartPosition, EndPosition, Error):
        super ().__init__ (StartPosition, EndPosition, 'Expected Character', Error)

class InvalidSyntaxError (Error):
    def __init__ (self, StartPosition, EndPosition, Error = ''):
        super ().__init__ (StartPosition, EndPosition, 'Invalid Syntax', Error)

class RTError (Error):
    def __init__ (self, StartPosition, EndPosition, Error, Context):
        super ().__init__ (StartPosition, EndPosition, 'Runtime Error', Error)

        self.Context = Context

    def AsString (self):
        Result  = self.GenerateTraceback ()
        Result += f'{self.Name}: {self.Error}'
        Result += '\n\n' + StringWithArrows (self.StartPosition.FileText, self.StartPosition, self.EndPosition)

        return Result

    def GenerateTraceback (self):
        Result = ''
        Position = self.StartPosition
        Context = self.Context

        while Context:
            Result = f'  File {Position.FileName}, line {str (Position.Line + 1)}, in {Context.DisplayName}\n' + Result
            Position = Context.ParentEntryPos
            Context = Context.Parent

        return 'Traceback (most recent call last):\n' + Result

def StringWithArrows (_Text, _StartPosition, _EndPosition):
    Result = ''

    StartIndex = max (_Text.rfind ('\n', 0, _StartPosition.Index), 0)
    EndIndex = _Text.find ('\n', StartIndex + 1)

    if EndIndex < 0:
        EndIndex = len (_Text)

    Lines = _EndPosition.Line - _StartPosition.Line + 1
    for I in range (Lines):
        Line = _Text[StartIndex : EndIndex]
        StartColumn = _StartPosition.Column if I == 0 else 0
        EndColumn = _EndPosition.Column if I == Lines - 1 else len (Line) - 1

        Result += Line + '\n'
        Result += ' ' * StartColumn + '^' * (EndColumn - StartColumn)

        StartIndex = EndIndex
        EndIndex = _Text.find ('\n', StartIndex + 1)

        if EndIndex < 0:
            EndIndex = len (_Text)

    return Result.replace ('\t', '')
