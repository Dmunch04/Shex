package me.Munchii.Shex.Utils;

import me.Munchii.Shex.Lexing.Lexer;
import me.Munchii.Shex.Tokens.Location;

import java.util.ArrayList;
import java.util.List;

public class ErrorHelper
{

    public static String MakeArrow (int Column)
    {
        StringBuilder ArrowString = new StringBuilder ();

        for (int Index = 0; Index < Column - 1; Index++)
        {
            ArrowString.append (" ");
        }

        ArrowString.append ("^");

        return ArrowString.toString ();
    }

    public static String MakeLines (Location Position)
    {
        int StartLine = Position.GetStartLine ();
        int EndLine = Position.GetEndLine ();
        int StartColumn = Position.GetStartColumn ();
        int EndColumn = Position.GetEndColumn ();

        StringBuilder Lines = new StringBuilder ();

        for (int LineIndex = StartLine; LineIndex <= EndLine; LineIndex++)
        {
            String Line = Lexer.GetLine (LineIndex - 1);
            System.out.println(Line);

            String Start = '\t' + Color.Reset.GetANSICode () + Color.Make256Color (60) + LineIndex + Color.Reset.GetANSICode () + " | ";
            if (LineIndex == StartLine) {
                // Get other string
                Lines.append(Start + Line.substring(0, StartColumn) + Color.Reset.GetANSICode () + Color.BoldRed.GetANSICode ());
                Lines.append(Line.substring(StartColumn));
                Lines.append("\n");
            } else if (LineIndex > StartLine && LineIndex < EndLine-1) {
                Lines.append(Start + Color.BoldRed.GetANSICode () + Line);
                Lines.append("\n");
            } else if (LineIndex == EndLine-1) {
                Lines.append(Start + Color.Reset.GetANSICode () + Color.BoldRed.GetANSICode () + Line.substring(0, EndColumn) + Color.Reset.GetANSICode ());
                Lines.append(Line.substring(EndColumn));
            }

            // TODO: Actually get this to work. I can't seem to normalize/fit the original given start and end columns to the current line

            //String FixedLine = FirstLine + Color.Reset.GetANSICode () + Color.BoldRed.GetANSICode () + Value + Color.Reset.GetANSICode () + LastLine;
            //String FormattedLine = '\t' + Color.Reset.GetANSICode () + Color.Make256Color (60) + LineIndex + Color.Reset.GetANSICode () + " | " + FixedLine + '\n';
            //Lines.append (FormattedLine);
        }

        return Lines.toString ();
    }

    /*
    public static String MakeLines (Location Position)
    {
        int StartLine = Position.GetStartLine ();
        int EndLine = Position.GetEndLine ();
        int StartColumn = Position.GetStartColumn ();
        int EndColumn = Position.GetEndColumn ();

        StringBuilder Lines = new StringBuilder ();

        for (int LineIndex = StartLine; LineIndex <= EndLine; LineIndex++)
        {
            int LineNumber = Position.GetStartLine () + LineIndex;
            String Line = Lexer.GetLine (LineIndex - 1);

            int ActualStartColumn = StartColumn - Line.length ();
            int ActualEndColumn = EndColumn - Line.length () - ActualStartColumn;

            System.out.println (ActualStartColumn);
            System.out.println (ActualEndColumn);

            String FirstLine = "";
            String LastLine = "";
            String Value = "";

            if (ActualStartColumn <= Line.length () && ActualEndColumn >= Line.length ())
            {
                System.out.println ("a");
                FirstLine = Line.substring (0, ActualStartColumn);
                LastLine = "";
                Value = Line.substring (ActualStartColumn, ActualEndColumn);
            }

            else if (ActualStartColumn <= Line.length () && ActualEndColumn <= Line.length ())
            {
                System.out.println ("b");
                FirstLine = "";
                LastLine = Line.substring (ActualEndColumn);
                Value = Line.substring (0, ActualEndColumn);
            }

            else
            {
                System.out.println ("c");
            }

            String FixedLine = FirstLine + Color.Reset.GetANSICode () + Color.BoldRed.GetANSICode () + Value + Color.Reset.GetANSICode () + LastLine;
            String FormattedLine = '\t' + Color.Reset.GetANSICode () + Color.Make256Color (60) + LineIndex + Color.Reset.GetANSICode () + " | " + FixedLine + '\n';
            Lines.append (FormattedLine);

            StartColumn -= ActualStartColumn;
            EndColumn -= ActualEndColumn;
        }

        return Lines.toString ();
    }
    */

}
