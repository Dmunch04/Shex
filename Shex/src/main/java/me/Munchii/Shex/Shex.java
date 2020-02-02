package me.Munchii.Shex;

import me.Munchii.Shex.Errors.Error;
import me.Munchii.Shex.Lexing.Lexer;
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

    public Shex (String[] Args) throws IOException
    {
        this.Args = Args;

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
            RunCode ("task Test (x, y) do say (x + y) done");
            //RunCode ("'Hello, World!");
            //RunCode ("aaa \\ yeet");
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

}
