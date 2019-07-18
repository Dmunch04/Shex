class Token:
    def __init__ (self, Type, Value = None, StartPosition = None, EndPosition = None):
        self.Type = Type
        self.Value = Value

        if StartPosition:
            self.StartPosition = StartPosition.Copy ()
            self.EndPosition = StartPosition.Copy ()
            self.EndPosition.Advance ()

        if EndPosition:
            self.EndPosition = EndPosition.Copy ()

    def Matches (self, Type, Value) -> bool:
        return self.Type == Type and self.Value == Value

    def __repr__ (self):
        return f'{self.Type}:{self.Value}' if self.Value else f'{self.Type}'

TokenInt                    = 'INT'
TokenFloat                  = 'FLOAT'
TokenString                 = 'STRING'
TokenIdentifier             = 'IDENTIFIER'
TokenKeyword                = 'KEYWORD'
TokenPlus                   = 'PLUS'
TokenMinus                  = 'MINUS'
TokenMultiply               = 'MUL'
TokenDivide                 = 'DIV'
TokenPower                  = 'POW'
TokenModulo                 = 'MOD'
TokenPlusAssign             = 'PLUSASSIGN'
TokenMinusAssign            = 'MINUSASSIGN'
TokenMultiplyAssign         = 'MULASSIGN'
TokenDivideAssign           = 'DIVASSIGN'
TokenPowerAssign            = 'POWASSIGN'
TokenModuloAssign           = 'MODASSIGN'
TokenEquals                 = 'EQ'
TokenLeftParenthesis        = 'LPAREN'
TokenRightParenthesis       = 'RPAREN'
TokenLeftSquareBracket      = 'LSQUARE'
TokenRightSquareBracket     = 'RSQUARE'
TokenEqualsEquals           = 'EE'
TokenNotEquals              = 'NE'
TokenLessThan               = 'LT'
TokenGreaterThan            = 'GT'
TokenLessThanEquals         = 'LTE'
TokenGreaterThanEquals      = 'GTE'
TokenComma                  = 'COMMA'
TokenArrow                  = 'ARROW'
TokenNewline                = 'NEWLINE'
TokenEmbed                  = 'EMBED'
TokenConfig                 = 'CONFIG'
TokenEndOfFile              = 'EOF'

Keywords = {
    'VAR': 'var',
    'AND': 'and',
    'OR': 'or',
    'NOT': 'not',
    'IF': 'if',
    'ELIF': 'elif',
    'ELSE': 'else',
    'FOR': 'for',
    'TO': 'to',
    'STEP': 'step',
    'WHILE': 'while',
    'TASK': 'task',
    'DO': 'do',
    'DONE': 'done'
}
