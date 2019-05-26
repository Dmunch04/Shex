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
