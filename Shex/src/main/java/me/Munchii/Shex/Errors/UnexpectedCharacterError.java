package me.Munchii.Shex.Errors;

import me.Munchii.Shex.Lexing.Lexer;
import me.Munchii.Shex.Shex;
import me.Munchii.Shex.Tokens.Location;
import me.Munchii.Shex.Utils.Color;
import me.Munchii.Shex.Utils.ErrorHelper;

import java.util.stream.IntStream;

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
        String Lines = ErrorHelper.MakeLines (Position);

        StringBuilder LinesAmount = new StringBuilder ();
        LinesAmount.append (Position.GetStartLine ());
        if (!(Position.GetStartLine () == Position.GetEndLine ())) LinesAmount.append ("-" + Position.GetEndLine ());

        return Color.BoldRed.GetANSICode () + Color.Underline.GetANSICode () + Error + Color.Reset.GetANSICode () + '\n' + '\n' +
                '\t' + Color.Reset.GetANSICode () + Description + ": '" + Value + "'" + '\n' +
                '\t' + Color.Reset.GetANSICode () + Color.Make256Color (60) + Shex.GetPath () + ":" + LinesAmount.toString () + '\n' + '\n' +
                Lines;
    }

}
