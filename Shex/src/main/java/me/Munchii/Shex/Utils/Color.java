package me.Munchii.Shex.Utils;

public enum Color
{

    // Source: http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html

    Reset ("\u001b[0m"),
    Clear (Reset.ANSICode),

    Bold ("\u001b[1m"),
    Underline ("\u001b[4m"),
    Reversed ("\u001b[7m"),

    Black ("\u001b[30m"),
    BoldBlack ("\u001b[30;1m"),
    Red ("\u001b[31m"),
    BoldRed ("\u001b[31;1m"),
    Green ("\u001b[32m"),
    BoldGreen ("\u001b[32;1m"),
    Yellow ("\u001b[33m"),
    BoldYellow ("\u001b[33;1m"),
    Blue ("\u001b[34m"),
    BoldBlue ("\u001b[34;1m"),
    Purple ("\u001b[35m"),
    BoldPurple ("\u001b[35;1m"),
    Cyan ("\u001b[36m"),
    BoldCyan ("\u001b[36;1m"),
    White ("\u001b[37m"),
    BoldWhite ("\u001b[37;1m"),

    BackgroundBlack ("\u001b[40m"),
    BackgroundBoldBlack ("\u001b[40;1m"),
    BackgroundRed ("\u001b[41m"),
    BackgroundBoldRed ("\u001b[41;1m"),
    BackgroundGreen ("\u001b[42m"),
    BackgroundBoldGreen ("\u001b[42;1m"),
    BackgroundYellow ("\u001b[43m"),
    BackgroundBoldYellow ("\u001b[43;1m"),
    BackgroundBlue ("\u001b[44m"),
    BackgroundBoldBlue ("\u001b[44;1m"),
    BackgroundPurple ("\u001b[45m"),
    BackgroundBoldPurple ("\u001b[45;1m"),
    BackgroundCyan ("\u001b[46m"),
    BackgroundBoldCyan ("\u001b[46;1m"),
    BackgroundWhite ("\u001b[47m"),
    BackgroundBoldWhite ("\u001b[47;1m");

    private String ANSICode;

    Color (String ANSICode)
    {
        this.ANSICode = ANSICode;
    }

    public String toString ()
    {
        return ANSICode;
    }

    public String GetANSICode ()
    {
        return ANSICode;
    }

    public static String Make256Color (int Index)
    {
        return "\u001b[38;5;" + Index + "m";
    }

    public static String Make256BackgroundColor (int Index)
    {
        return "\u001b[48;5;" + Index + "m";
    }

}
