package me.Munchii.Shex.Tokens;

public class Token
{

    private TokenType Type;
    private Location Position;
    private String Lexeme;
    private Object Literal;

    public Token (TokenType Type, Location Position, String Lexeme, Object Literal)
    {
        this.Type = Type;
        this.Position = Position;
        this.Lexeme = Lexeme;
        this.Literal = Literal;
    }

    public String toString ()
    {
        return Type + " " + Lexeme + " " + Literal + " @ " + Position.toString ();
    }

    public TokenType GetType ()
    {
        return Type;
    }

    public Location GetPosition ()
    {
        return Position;
    }

    public String GetLexeme ()
    {
        return Lexeme;
    }

    public Object GetLiteral ()
    {
        return Literal;
    }

}
