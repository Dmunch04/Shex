class SymbolTable:
    def __init__ (self, Parent = None):
        self.Symbols = {}
        self.Parent = Parent

    def Get (self, Name):
        Value = self.Symbols.get (Name, None)

        if Value == None and self.Parent:
            return self.Parent.Get (Name)

        return Value

    def Set (self, Name, Value):
        self.Symbols[Name] = Value

    def Remove (self, Name):
        del self.Symbols[Name]
