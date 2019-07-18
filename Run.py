import Source.Shex as Main

def Run (Path):
    with open (Path, 'r') as File:
        Data = File.read ()

    Main.Run (Path, Data)

def Test (Index):
    Run (f'Tests/Test{str (Index)}.shex')

# Run ('Path/To/File.shex')
Test (3)
