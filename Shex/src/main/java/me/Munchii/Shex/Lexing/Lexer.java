package me.Munchii.Shex.Lexing;

import me.Munchii.Shex.Errors.UnexpectedCharacterError;
import me.Munchii.Shex.Errors.UnterminatedStringError;
import me.Munchii.Shex.Shex;
import me.Munchii.Shex.Tokens.Location;
import me.Munchii.Shex.Tokens.Token;
import me.Munchii.Shex.Tokens.TokenType;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Lexer
{

    private String Source;
    private static String SourceCopy;

    private List<Token> Tokens;
    private int Index;

    private int Start = 0;
    private int Current = 0;
    private int Line = 1;

    public Lexer (String Source)
    {
        this.Source = Source;
        this.Tokens = new ArrayList<Token> ();
        this.Index = 0;

        SourceCopy = Source;
    }

    public void Lex ()
    {
        while (!IsAtEnd ())
        {
            Start = Current;
            LexToken ();
        }

        Tokens.add (new Token (TokenType.EOF, new Location (Line, Line, Start, Current), null, ""));
    }

    private void LexToken ()
    {
        char CurrentChar = Advance ();

        switch (CurrentChar)
        {
            case '(': AddToken (TokenType.LeftParenthesis); break;
            case ')': AddToken (TokenType.RightParenthesis); break;
            case '[': AddToken (TokenType.LeftBracket); break;
            case ']': AddToken (TokenType.RightBracket); break;
            case '{': AddToken (TokenType.LeftBrace); break;
            case '}': AddToken (TokenType.RightBrace); break;
            case ',': AddToken (TokenType.Comma); break;
            case '.': AddToken (TokenType.Dot); break;
            case '|': AddToken (TokenType.Pipe); break;
            case '?': AddToken (TokenType.QuestionMark); break;
            case '+': AddToken (Match ('=') ? TokenType.PlusEquals : TokenType.Plus); break;
            case '-':
                if (Match ('-'))
                {
                    while (Peek () != '\n' && !IsAtEnd ()) Advance ();
                }

                else if (Match ('>'))
                {
                    AddToken (TokenType.Arrow);
                }

                else
                {
                    AddToken (Match ('=') ? TokenType.DashEquals : TokenType.Dash);
                }
                break;
            case '*': AddToken (Match ('=') ? TokenType.StarEquals : TokenType.Star); break;
            case '/': AddToken (Match ('=') ? TokenType.SlashEquals : TokenType.Slash); break;
            case ':': AddToken (Match (':') ? TokenType.ColonColon : TokenType.Colon);
            case ';': AddToken (TokenType.SemiColon); break;
            case '!': AddToken (Match ('=') ? TokenType.BangEquals : TokenType.Bang); break;
            case '=': AddToken (Match ('=') ? TokenType.EqualEquals : TokenType.Equal); break;
            case '>': AddToken (Match ('=') ? TokenType.GreaterThanEquals : TokenType.GreaterThan); break;
            case '<': AddToken (Match ('=') ? TokenType.LessThanEquals : TokenType.LessThan); break;
            case ' ':
            case '\r':
            case '\t':
                break;
            case '\n':
                Line++;
                break;
            case '"':
            case '\'':
                MakeString (); break;
            default:
                if (IsAlpha (CurrentChar))
                {
                    MakeIdentifier ();
                }

                else if (IsDigit (CurrentChar))
                {
                    MakeNumber ();
                }

                else
                {
                    Shex.Error (new UnexpectedCharacterError (new Location (Line, Line, Start, Current), CurrentChar));
                }
                break;
        }
    }

    private boolean IsAtEnd ()
    {
        return Current >= Source.length ();
    }

    private char Advance ()
    {
        Current++;
        return Source.charAt (Current - 1);
    }

    private void AddToken (TokenType Type) {
        AddToken (Type, null);
    }

    private void AddToken (TokenType Type, Object Literal)
    {
        String Text = Source.substring (Start, Current);
        Tokens.add (new Token (Type, new Location (Line, Line, Start, Current), Text, Literal));
    }

    private boolean Match (char Expected)
    {
        if (IsAtEnd ()) return false;
        if (Source.charAt (Current) != Expected) return false;

        Current++;
        return true;
    }

    private char Peek ()
    {
        if (IsAtEnd ()) return '\0';
        return Source.charAt (Current);
    }

    private char Peek (int Amount)
    {
        if (Current + Amount >= Source.length ()) return '\0';
        return Source.charAt (Current + Amount);
    }

    private boolean IsAlpha (char Target)
    {
        return (Target >= 'a' && Target <= 'z') || (Target >= 'A' && Target <= 'Z') || Target == '_';
    }

    private boolean IsDigit (char Target)
    {
        return Target >= '0' && Target <= '9';
    }

    private boolean IsAlphaNumeric (char Target)
    {
        return IsAlpha (Target) || IsDigit (Target);
    }

    private void MakeString ()
    {
        int StartLine = Line;

        while (Peek () != '"' && Peek () != '\'' && !IsAtEnd())
        {
            if (Peek () == '\n') Line++;
            Advance ();
        }

        if (IsAtEnd ())
        {
            Shex.Error (new UnterminatedStringError (new Location (StartLine, Line, Start, Current), Source.substring (Start, Current)));
            return;
        }

        Advance();

        String Value = Source.substring (Start + 1, Current - 1);
        AddToken (TokenType.String, Value);
    }

    private void MakeNumber ()
    {
        while (IsDigit (Peek ())) Advance();

        if (Peek () == '.' && IsDigit (Peek (1)))
        {
            Advance();

            while (IsDigit (Peek ())) Advance();
        }

        AddToken (TokenType.Number, Double.parseDouble (Source.substring (Start, Current)));
    }

    private void MakeIdentifier ()
    {
        while (IsAlphaNumeric (Peek ())) Advance();

        String Text = Source.substring (Start, Current);

        TokenType Type = Keywords.get (Text);
        if (Type == null) Type = TokenType.Identifier;
        AddToken (Type);
    }

    public List<Token> GetTokens ()
    {
        return Tokens;
    }

    private static final Map<String, TokenType> Keywords;
    static
    {
        Keywords = new HashMap<String, TokenType> ();
        Keywords.put ("and", TokenType.And);
        Keywords.put ("object", TokenType.Object);
        Keywords.put ("var", TokenType.Variable);
        Keywords.put ("task", TokenType.Task);
        Keywords.put ("for", TokenType.For);
        Keywords.put ("while", TokenType.While);
        Keywords.put ("if", TokenType.If);
        Keywords.put ("else", TokenType.Else);
        Keywords.put ("or", TokenType.Or);
        Keywords.put ("import", TokenType.Import);
        Keywords.put ("return", TokenType.Return);
        Keywords.put ("true", TokenType.True);
        Keywords.put ("false", TokenType.False);
        Keywords.put ("switch", TokenType.Switch);
        Keywords.put ("case", TokenType.Case);
        Keywords.put ("this", TokenType.This);
        Keywords.put ("type", TokenType.Type);
        Keywords.put ("do", TokenType.Do);
        Keywords.put ("done", TokenType.Done);
    }

    public static String GetLine (int LineIndex)
    {
        try {
            return SourceCopy.split ("\n")[LineIndex];
        } catch (ArrayIndexOutOfBoundsException e) {
            return null;
        }
    }

}
