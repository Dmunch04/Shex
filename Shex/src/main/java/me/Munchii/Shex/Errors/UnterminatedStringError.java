package me.Munchii.Shex.Errors;

import me.Munchii.Shex.Tokens.Location;
import me.Munchii.Shex.Utils.Color;
import me.Munchii.Shex.Utils.ErrorHelper;

public class UnterminatedStringError extends Error
{

    private final String Error = "UnterminatedStringError";
    private final String Description = "Unterminated string";
    private final Location Position;
    private final String Target;

    public UnterminatedStringError (Location Position, String Target)
    {
        super ("UnexpectedCharacterError", "Unexpected character", Position, '\0');

        this.Position = Position;
        this.Target = Target;
    }

    @Override
    public String toString ()
    {
        return Color.BoldRed.GetANSICode () + Error + Color.Reset.GetANSICode () + " " + Color.Red.GetANSICode () + Description + '\n' +
            Color.Reset.GetANSICode () + Color.Red.GetANSICode () + Position.GetStartLine () + " | " + Color.Reset + Target + '\n' +
            Color.Make256Color (245) + ErrorHelper.MakeArrow (Position.GetEndColumn () + 1 + (String.valueOf (Position.GetStartLine ()).length () + 3)) + Color.Reset;
    }

}
