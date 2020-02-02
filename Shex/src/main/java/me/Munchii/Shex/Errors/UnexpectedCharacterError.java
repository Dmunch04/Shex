package me.Munchii.Shex.Errors;

import me.Munchii.Shex.Lexing.Lexer;
import me.Munchii.Shex.Tokens.Location;
import me.Munchii.Shex.Utils.Color;
import me.Munchii.Shex.Utils.ErrorHelper;

public class UnexpectedCharacterError extends Error
{

    private final String Error = "UnexpectedCharacterError";
    private final String Description = "Unexpected character";
    private final Location Position;
    private final char Value;

    public UnexpectedCharacterError (Location Position, char Value)
    {
        super ("UnexpectedCharacterError", "Unexpected character", Position, Value);

        this.Position = Position;
        this.Value = Value;
    }

    @Override
    public String toString ()
    {
        String Line = Lexer.GetLine (Position.GetStartLine () - 1);
        String FirstLine = Line.substring (0, Position.GetStartColumn ());
        String LastLine = Line.substring (Position.GetEndColumn ());

        String FixedLine = Color.Make256Color (245) + FirstLine + Color.Reset.GetANSICode () + Color.Bold.GetANSICode () + Value + Color.Reset.GetANSICode () + Color.Make256Color (245) + LastLine;

        return Color.BoldRed.GetANSICode () + Error + Color.Reset.GetANSICode () + " " + Color.Red.GetANSICode () + Description + ": '" + Value + "'" + '\n' +
                Color.Reset.GetANSICode () + Color.Red.GetANSICode () + Position.GetStartLine () + " | " + Color.Reset + FixedLine + '\n' +
                Color.Make256Color (245) + ErrorHelper.MakeArrow (Position.GetEndColumn () + (String.valueOf (Position.GetStartLine ()).length () + 3)) + Color.Reset;
    }

}
