package me.Munchii.Shex.Tokens;

public class Location
{

    private int StartLine;
    private int EndLine;
    private int StartColumn;
    private int EndColumn;

    public Location (int StartLine, int EndLine, int StartColumn, int EndColumn)
    {
        this.StartLine = StartLine;
        this.EndLine = EndLine;
        this.StartColumn = StartColumn;
        this.EndColumn = EndColumn;
    }

    public String toString ()
    {
        return StartLine + ":" + StartColumn + " - " + EndLine + ":" + EndColumn;
    }

    public int GetStartLine ()
    {
        return StartLine;
    }

    public int GetEndLine ()
    {
        return EndLine;
    }

    public int GetStartColumn ()
    {
        return StartColumn;
    }

    public int GetEndColumn ()
    {
        return EndColumn;
    }

}
