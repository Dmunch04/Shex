import Source.Shex as Main
from DavesLogger import Logs

def Run ():
    while True:
        Input = input ('Shex >>> ').strip ()

        if not Input.startswith ('--'):
            Result, Error = Main.Run ('<stdin>', Input)

            if Error:
                Logs.Error (Error.AsString ())

            elif Result:
                print (Result)

Run ()
