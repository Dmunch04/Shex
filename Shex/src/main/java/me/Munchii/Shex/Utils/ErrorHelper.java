package me.Munchii.Shex.Utils;

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

}
