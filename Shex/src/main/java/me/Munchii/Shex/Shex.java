package me.Munchii.Shex;

import me.Munchii.Shex.Errors.Error;
import me.Munchii.Shex.Errors.UnexpectedCharacterError;
import me.Munchii.Shex.Lexing.Lexer;
import me.Munchii.Shex.Tokens.Location;
import me.Munchii.Shex.Tokens.Token;
import me.Munchii.Shex.Utils.Color;

import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class Shex
{

    private String[] Args;
    private static String[] ArgsCopy;

    public Shex (String[] Args) throws IOException
    {
        this.Args = Args;
        ArgsCopy = Args;

        if (Args.length > 1)
        {
            System.out.println (Color.Red.GetANSICode () + "Wrong usage! Usage: jshex [path]");
            System.exit(64);
        }

        else if (Args.length == 1)
        {
            RunFile (Args[0]);
        }

        else
        {
            // Testing:
            //RunCode ("\"Hello, World!\" 1234 12.34 \n or hel\nlo");
            //RunCode ("task Test (x, y) do say (x + y) done");
            //RunCode ("'Hello, World!");

            // Multiline Error Test Case 1:
            // Status: Not Passed
            //RunCode ("aaa\nyeet\noof"); // columns = 12
            //Error (new UnexpectedCharacterError (new Location (2, 3, 6, 10), '\0'));

            // Multiline Error Test Case 2:
            // Status: Not Passed
            RunCode ("aaa\nyeet\noof\ngg"); // columns = 15
            Error (new UnexpectedCharacterError (new Location (2, 4, 6, 12), '\0'));
        }
    }

    private void RunFile (String Path) throws IOException
    {
        byte[] FileBytes = Files.readAllBytes (Paths.get (Path));
        RunCode (new String (FileBytes, Charset.defaultCharset ()));
    }

    private void RunCode (String Code) throws IOException
    {
        Lexer Tokenizer = new Lexer (Code);
        Tokenizer.Lex ();
        List<Token> Tokens = Tokenizer.GetTokens ();

        for (Token Token : Tokens)
        {
            System.out.println (Token);
        }
    }

    public static void Error (Error Exception)
    {
        Exception.Print ();
        System.exit (65);
    }

    public static String GetPath ()
    {
        if (ArgsCopy.length < 1)
        {
            return "/Testing/Test/Case.shex";
        }

        return ArgsCopy[0];
    }

}
