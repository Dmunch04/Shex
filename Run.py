import Source.Shex as Main

def Run (Path):
    with open (Path, 'r') as File:
        Data = File.read ()

    Main.Run (Path, Data)

# Run ('Path/To/File.shex')
Run ('Test.shex')
