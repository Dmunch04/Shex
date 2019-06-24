import Source.Shex as Main
from DavesLogger import Logs

def Run (_Path):
    with open (_Path, 'r') as File:
        Lines = File.read ().split ('\n')

    for Line in Lines:
        Line = Line.strip ()

        if Line == '' or Line in ' \n\t' or Line.startswith ('--'):
            continue

        Result, Error = Main.Run (_Path, Line)

        if Error:
            Logs.Error (Error.AsString ())
            return

        elif str (Result) != '':
            print (Result)

# Run ('Path/To/File.shex')
Run ('Test.shex')
