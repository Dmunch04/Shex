class ShexContext:
    def __init__ (self, DisplayName, Parent = None, ParentEntryPosition = None):
        self.DisplayName = DisplayName
        self.Parent = Parent
        self.ParentEntryPosition = ParentEntryPosition
        self.SymbolTable = None
