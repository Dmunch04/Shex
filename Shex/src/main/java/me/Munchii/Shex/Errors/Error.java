package me.Munchii.Shex.Errors;

import me.Munchii.Shex.Tokens.Location;

public abstract class Error
{

    private String Error;
    private String Description;
    private Location Position;
    private Object Value;

    public Error (String Error, String Description, Location Position, Object Value)
    {
        this.Error = Error;
        this.Description = Description;
        this.Position = Position;
        this.Value = Value;
    }

    public String toString ()
    {
        return Error + ": " + Description + " @ " + Position.toString ();
    }

    public void Print ()
    {
        System.out.println (this.toString ());
    }

}
