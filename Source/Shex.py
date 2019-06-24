########################################
#            Rewritten from:           #
#  https://github.com/davidcallanan/   #
#            py-myopl-code             #
#                                      #
#          Original Code By:           #
#            davidcallanan             #
#                                      #
#            Rewritten By:             #
#               Munchii                #
########################################





#######################################
# SETUP
#######################################

import os
import sys
sys.path.append (os.path.abspath (os.path.dirname (__file__)))

Path = ''
print (sys.platform)

if sys.platform == 'windows':
    Path = 'C:/Users/{}/AppData/Local/Programs/GravPack/Lib/{{}}'

elif sys.platform == 'linux':
    Path = '/home/{}/.shex/{{}}'

# Add mac support



#######################################
# IMPORTS
#######################################

from Errors import *

import string
import getpass
from DavesLogger import Logs

GlobalPath = Path.format (getpass.getuser ())



#######################################
# CONSTANTS
#######################################

Digits = '0123456789'
Letters = string.ascii_letters
LettersDigits = Letters + Digits
DefaultFunctions = {
    'print': {
        'Args': ['value'],
        'Body': 'value'
    },

    'import': {
        'Args': ['path'],
        'Body': '"imp::path"'
    },

    'read': {
        'Args': ['path'],
        'Body': '"read::path"'
    },

    'iseven':
    {
        'Args': ['number'],
        'Body': '"iseven::number"'
    },

    'isodd': {
        'Args': ['number'],
        'Body': '"isodd::number"'
    },

    'length': {
        'Args': ['value'],
        'Body': '"length::value"'
    },

    'split': {
        'Args': ['string', 'factor'],
        'Body': '"split::string::factor"'
    },

    'join': {
        'Args': ['list', 'factor'],
        'Body': '"join::list::factor"'
    }
}



#######################################
# ERRORS
#######################################

class Error:
    def __init__ (self, StartPosition, EndPosition, ErrorName, Error):
        self.StartPosition = StartPosition
        self.EndPosition = EndPosition
        self.ErrorName = ErrorName
        self.Error = Error

    def AsString (self):
        Result = f'{self.ErrorName}: {self.Error}\n'
        Result += f'File :: {self.StartPosition.FileName}, Line :: {self.StartPosition.Line + 1}'
        Result += '\n\n' + StringWithArrows (self.StartPosition.FileText, self.StartPosition, self.EndPosition)

        return Result

class IllegalCharError (Error):
    def __init__ (self, StartPosition, EndPosition, Error):
        super ().__init__ (StartPosition, EndPosition, 'Illegal Character', Error)

class ExpectedCharError (Error):
    def __init__ (self, StartPosition, EndPosition, Error):
        super ().__init__ (StartPosition, EndPosition, 'Expected Character', Error)

class InvalidSyntaxError (Error):
    def __init__ (self, StartPosition, EndPosition, Error = ''):
        super ().__init__ (StartPosition, EndPosition, 'Invalid Syntax', Error)

class RTError (Error):
    def __init__(self, StartPosition, EndPosition, Error, Context):
        super ().__init__ (StartPosition, EndPosition, 'Runtime Error', Error)

        self.Context = Context

    def AsString (self):
        Result = self.GenerateTraceback ()
        Result += f'{self.ErrorName}: {self.Error}'
        Result += '\n' + StringWithArrows (self.StartPosition.FileText, self.StartPosition, self.EndPosition)

        return Result

    def GenerateTraceback (self):
        Result = ''
        Position = self.StartPosition
        Context = self.Context

        while Context:
            Result = f'  File :: {Position.FileName}, Line :: {str (Position.Line + 1)}, In :: {Context.DisplayName}\n' + Result
            Position = Context.ParentEntryPos
            Context = Context.Parent

        return 'Traceback (most recent Call last):\n' + Result



#######################################
# POSITION
#######################################

class Position:
    def __init__(self, Index, Line, Column, FileName, FileText):
        self.Index = Index
        self.Line = Line
        self.Column = Column
        self.FileName = FileName
        self.FileText = FileText

    def Advance (self, _CurrentChar = None):
        self.Index += 1
        self.Column += 1

        if _CurrentChar == '\n':
            self.Line += 1
            self.Column = 0

        return self

    def Copy (self):
        return Position (self.Index, self.Line, self.Column, self.FileName, self.FileText)

#######################################
# TOKENS
#######################################

# Types
TokenInt = 'INT'
TokenFloat = 'FLOAT'
TokenString = 'STRING'
TokenKeyword = 'KEYWORD'
TokenIdentifier = 'IDENTIFIER'

# Operators
TokenPlus = 'PLUS'
TokenMinus = 'MINUS'
TokenMultiply = 'MUL'
TokenDivide = 'DIV'
TokenPower = 'POW'
TokenEquals = 'EQ'

# () & []
TokenLeftParenthesis = 'LPAREN'
TokenRightParenthesis = 'RPAREN'
TokenLeftSquareBracket = 'LSQUARE'
TokenRightSquareBracket = 'RSQUARE'

# Equal Compare
TokenNotEquals = 'NE'
TokenEqualsEquals = 'EE'

# More or Less Compare
TokenLessThan = 'LT'
TokenGreaterThan = 'GT'
TokenLessThanEquals = 'LTE'
TokenGreaterThanEquals = 'GTE'

# Special
#TokenPass = 'PASS' - I guess we're not doing it this way
TokenComma = 'COMMA'
TokenArrow = 'ARROW'

# Other
TokenEndOfFile = 'EOF'
TokenIllegal = 'ILLEGAL'

Keywords = [
    'var',
    'and',
    'or',
    'not',
    'if',
    'elseif',
    'else',
    'for',
    'to',
    'step',
    'while',
    'task',
    'object',
    'then'
]

class Token:
    def __init__(self, Type, Value = None, StartPosition = None, EndPosition = None):
        self.Type = Type
        self.Value = Value

        if StartPosition:
            self.StartPosition = StartPosition.Copy ()
            self.EndPosition = StartPosition.Copy ()
            self.EndPosition.Advance ()

        if EndPosition:
            self.EndPosition = EndPosition.Copy ()

    def Matches (self, _Type, _Value):
        return self.Type == _Type and self.Value == _Value

    def __repr__ (self):
        if self.Value:
            return f'{self.Type}:{self.Value}'

        return f'{self.Type}'



#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, FileName, Text):
        self.FileName = FileName
        self.Text = Text
        self.Position = Position (-1, 0, -1, FileName, Text)
        self.CurrentChar = None
        self.Advance ()

    def Advance (self):
        self.Position.Advance (self.CurrentChar)
        self.CurrentChar = self.Text[self.Position.Index] if self.Position.Index < len (self.Text) else None

    def MakeTokens (self):
        Tokens = []

        while self.CurrentChar != None:
            if self.CurrentChar in ' \t':
                self.Advance ()

            elif self.CurrentChar in Digits:
                Tokens.append (self.MakeNumber ())

            elif self.CurrentChar in Letters + '.':
                Tokens.append (self.MakeIdentifier ())

            elif self.CurrentChar == '"' or self.CurrentChar == "'":
                Tokens.append (self.MakeString ())

            elif self.CurrentChar == '+':
                Tokens.append (Token (TokenPlus, StartPosition = self.Position))
                self.Advance ()

            elif self.CurrentChar == '-':
                Tokens.append(self.MakeMinusOrArrow ())

            elif self.CurrentChar == '*':
                Tokens.append (Token (TokenMultiply, StartPosition = self.Position))
                self.Advance ()

            elif self.CurrentChar == '/':
                Tokens.append (Token (TokenDivide, StartPosition = self.Position))
                self.Advance ()

            elif self.CurrentChar == '^':
                Tokens.append (Token (TokenPower, StartPosition = self.Position))
                self.Advance ()

            elif self.CurrentChar == '(':
                Tokens.append (Token (TokenLeftParenthesis, StartPosition = self.Position))
                self.Advance ()

            elif self.CurrentChar == ')':
                Tokens.append (Token (TokenRightParenthesis, StartPosition = self.Position))
                self.Advance ()

            elif self.CurrentChar == '[':
                Tokens.append (Token (TokenLeftSquareBracket, StartPosition = self.Position))
                self.Advance ()

            elif self.CurrentChar == ']':
                Tokens.append (Token (TokenRightSquareBracket, StartPosition = self.Position))
                self.Advance ()

            elif self.CurrentChar == '!':
                CurToken, Error = self.MakeNotEquals ()

                if Error:
                    return [], Error

                Tokens.append (CurToken)

            elif self.CurrentChar == '=':
                Tokens.append (self.MakeEquals ())

            elif self.CurrentChar == '<':
                Tokens.append (self.MakeLessThan ())

            elif self.CurrentChar == '>':
                Tokens.append (self.MakeGreaterThan ())

            elif self.CurrentChar == ',':
                Tokens.append (Token (TokenComma, StartPosition = self.Position))
                self.Advance ()

            #elif self.CurrentChar == '.':
                #Tokens.append (self.MakePass ())

            else:
                StartPosition = self.Position.Copy ()
                Char = self.CurrentChar
                self.Advance ()

                return [], IllegalCharError (StartPosition, self.Position, "'" + Char + "'")

        Tokens.append (Token (TokenEndOfFile, StartPosition = self.Position))
        return Tokens, None

    def MakeNumber (self):
        NumString = ''
        Dots = 0
        StartPosition = self.Position.Copy ()

        while self.CurrentChar != None and self.CurrentChar in Digits + '.':
            if self.CurrentChar == '.':
                if Dots == 1:
                    break

                Dots += 1

            NumString += self.CurrentChar
            self.Advance ()

        if Dots == 0:
            return Token (TokenInt, int (NumString), StartPosition, self.Position)

        else:
            return Token (TokenFloat, float (NumString), StartPosition, self.Position)

    def MakeString (self):
        String = ''
        StartPosition = self.Position.Copy ()
        IsEscapeCharacter = False
        self.Advance ()

        EscapeCharacters = {
            'n': '\n',
            't': '\t'
        }

        while self.CurrentChar != None and (self.CurrentChar != '"' and self.CurrentChar != "'" or IsEscapeCharacter):
            if IsEscapeCharacter:
                String += EscapeCharacters.get (self.CurrentChar, self.CurrentChar)

            else:
                if self.CurrentChar == '\\':
                    IsEscapeCharacter = True

                else:
                    String += self.CurrentChar

            self.Advance ()
            IsEscapeCharacter = False

        self.Advance ()

        return Token (TokenString, String, StartPosition, self.Position)

    def MakeIdentifier (self):
        IdString = ''
        StartPosition = self.Position.Copy ()

        while self.CurrentChar != None and self.CurrentChar in LettersDigits + '_.':
            IdString += self.CurrentChar
            self.Advance ()

        TokenType = TokenKeyword if IdString in Keywords else TokenIdentifier

        return Token (TokenType, IdString, StartPosition, self.Position)

    def MakeMinusOrArrow (self):
        TokenType = TokenMinus
        StartPosition = self.Position.Copy ()
        self.Advance ()

        if self.CurrentChar == '>':
            self.Advance ()
            TokenType = TokenArrow

        return Token (TokenType, StartPosition = StartPosition, EndPosition = self.Position)

    def MakeNotEquals (self):
        StartPosition = self.Position.Copy ()
        self.Advance ()

        if self.CurrentChar == '=':
            self.Advance ()
            return Token (TokenNotEquals, StartPosition = StartPosition, EndPosition = self.Position), None

        self.Advance ()
        return None, ExpectedCharError (StartPosition, self.Position, "'=' (after '!')")

    def MakeEquals (self):
        TokenType = TokenEquals
        StartPosition = self.Position.Copy ()
        self.Advance ()

        if self.CurrentChar == '=':
            self.Advance ()
            TokenType = TokenEqualsEquals

        return Token (TokenType, StartPosition = StartPosition, EndPosition = self.Position)

    def MakeLessThan (self):
        TokenType = TokenLessThan
        StartPosition = self.Position.Copy ()
        self.Advance ()

        if self.CurrentChar == '=':
            self.Advance ()
            TokenType = TokenLessThanEquals

        return Token (TokenType, StartPosition = StartPosition, EndPosition = self.Position)

    def MakeGreaterThan (self):
        TokenType = TokenGreaterThan
        StartPosition = self.Position.Copy ()
        self.Advance ()

        if self.CurrentChar == '=':
            self.Advance ()
            TokenType = TokenGreaterThanEquals

        return Token (TokenType, StartPosition = StartPosition, EndPosition = self.Position)

    def MakePass (self):
        TokenType = TokenIllegal
        StartPosition = self.Position.Copy ()
        self.Advance ()

        if self.CurrentChar == '.':
            self.Advance ()
            TokenType = TokenPass

        return Token (TokenType, StartPosition = StartPosition, EndPosition = self.Position)



#######################################
# NODES
#######################################

class NumberNode:
    def __init__(self, Token):
        self.Token = Token

        self.StartPosition = self.Token.StartPosition
        self.EndPosition = self.Token.EndPosition

    def __repr__ (self):
        return f'{self.Token}'

class StringNode:
    def __init__ (self, Token):
        self.Token = Token

        self.StartPosition = self.Token.StartPosition
        self.EndPosition = self.Token.EndPosition

    def __repr__ (self):
        return f'{self.Token}'

class ListNode:
    def __init__ (self, ElementNodes, StartPosition, EndPosition):
        self.ElementNodes = ElementNodes

        self.StartPosition = StartPosition
        self.EndPosition = EndPosition

class VarAccessNode:
    def __init__ (self, VarNameToken):
        self.VarNameToken = VarNameToken

        self.StartPosition = self.VarNameToken.StartPosition
        self.EndPosition = self.VarNameToken.EndPosition

class VarAssignNode:
    def __init__ (self, VarNameToken, ValueNode):
        self.VarNameToken = VarNameToken
        self.ValueNode = ValueNode

        self.StartPosition = self.VarNameToken.StartPosition
        self.EndPosition = self.ValueNode.EndPosition

class BinOpNode:
    def __init__ (self, LeftNode, OperatorToken, RightNode):
        self.LeftNode = LeftNode
        self.OperatorToken = OperatorToken
        self.RightNode = RightNode

        self.StartPosition = self.LeftNode.StartPosition
        self.EndPosition = self.RightNode.EndPosition

    def __repr__ (self):
        return f'({self.LeftNode}, {self.OperatorToken}, {self.RightNode})'

class UnaryOpNode:
    def __init__(self, OperatorToken, Node):
        self.OperatorToken = OperatorToken
        self.Node = Node

        self.StartPosition = self.OperatorToken.StartPosition
        self.EndPosition = Node.EndPosition

    def __repr__ (self):
        return f'({self.OperatorToken}, {self.Node})'

class IfNode:
    def __init__ (self, Cases, ElseCase):
        self.Cases = Cases
        self.ElseCase = ElseCase

        self.StartPosition = self.Cases[0][0].StartPosition
        self.EndPosition = (self.ElseCase or self.Cases[len (self.Cases) - 1][0]).EndPosition

class ForNode:
    def __init__ (self, VarNameToken, StartValueNode, EndValueNode, StepValueNode, BodyNode):
        self.VarNameToken = VarNameToken
        self.StartValueNode = StartValueNode
        self.EndValueNode = EndValueNode
        self.StepValueNode = StepValueNode
        self.BodyNode = BodyNode

        self.StartPosition = self.VarNameToken.StartPosition
        self.EndPosition = self.BodyNode.EndPosition

class WhileNode:
    def __init__ (self, ConditionNode, BodyNode):
        self.ConditionNode = ConditionNode
        self.BodyNode = BodyNode

        self.StartPosition = self.ConditionNode.StartPosition
        self.EndPosition = self.BodyNode.EndPosition

class FuncDefNode:
    def __init__ (self, VarNameToken, ArgNameTokens, BodyNode):
        self.VarNameToken = VarNameToken
        self.ArgNameTokens = ArgNameTokens
        self.BodyNode = BodyNode

        if self.VarNameToken:
            self.StartPosition = self.VarNameToken.StartPosition

        elif len (self.ArgNameTokens) > 0:
            self.StartPosition = self.ArgNameTokens[0].StartPosition

        else:
            self.StartPosition = self.BodyNode.StartPosition

        self.EndPosition = self.BodyNode.EndPosition

class ClassDefNode:
    def __init__ (self, VarNameToken, ArgNameTokens, BodyNode):
        self.VarNameToken = VarNameToken
        self.ArgNameTokens = ArgNameTokens
        self.BodyNode = BodyNode

        if self.VarNameToken:
            self.StartPosition = self.VarNameToken.StartPosition

        elif len (self.ArgNameTokens) > 0:
            self.StartPosition = self.ArgNameTokens[0].StartPosition

        else:
            self.StartPosition = self.BodyNode.StartPosition

        self.EndPosition = self.BodyNode.EndPosition

class CallNode:
    def __init__ (self, NodeToCall, ArgNodes):
        self.NodeToCall = NodeToCall
        self.ArgNodes = ArgNodes

        self.StartPosition = self.NodeToCall.StartPosition

        if len (self.ArgNodes) > 0:
            self.EndPosition = self.ArgNodes[len (self.ArgNodes) - 1].EndPosition

        else:
            self.EndPosition = self.NodeToCall.EndPosition



#######################################
# PARSE RESULT
#######################################

class ParseResult:
    def __init__ (self):
        self.Error = None
        self.Node = None
        self.LastRegisteredAdvanceCount = 0
        self.AdvanceCount = 0

    def RegisterAdvancement (self):
        self.LastRegisteredAdvanceCount = 1
        self.AdvanceCount += 1

    def Register (self, _Result):
        self.LastRegisteredAdvanceCount = _Result.AdvanceCount
        self.AdvanceCount += _Result.AdvanceCount

        if _Result.Error:
            _Result.Error = _Result.Error

        return _Result.Node

    def Success (self, _Node):
        self.Node = _Node

        return self

    def Failure (self, _Error):
        if not self.Error or self.LastRegisteredAdvanceCount == 0:
            self.Error = _Error

        return self



#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, Tokens):
        self.Tokens = Tokens
        self.TokenIndex = -1
        self.Advance ()

    def Advance (self, ):
        self.TokenIndex += 1

        if self.TokenIndex < len (self.Tokens):
            self.CurrentToken = self.Tokens[self.TokenIndex]

        return self.CurrentToken

    def Parse (self):
        Result = self.Expression ()

        if not Result.Error and self.CurrentToken.Type != TokenEndOfFile:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected '+', '-', '*', '/', '^', '==', '!=', '<', '>', <=', '>=', 'and' or 'or'"
            ))

        return Result

    def Expression (self):
        Result = ParseResult ()

        if self.CurrentToken.Matches (TokenKeyword, 'var'):
            Result.RegisterAdvancement ()
            self.Advance ()

            if self.CurrentToken.Type != TokenIdentifier:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                    'Expected identifier'
                ))

            VarName = self.CurrentToken
            Result.RegisterAdvancement ()
            self.Advance ()

            if self.CurrentToken.Type != TokenEquals:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                    "Expected '='"
                ))

            Result.RegisterAdvancement ()
            self.Advance ()
            Expr = Result.Register (self.Expression ())

            if Result.Error:
                return Result

            return Result.Success (VarAssignNode (VarName, Expr))

        Node = Result.Register (self.BinOp (self.CompExpression, ((TokenKeyword, 'and'), (TokenKeyword, 'or'))))

        if Result.Error:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected 'var', 'if', 'for', 'while', 'task', int, float, identifier, '+', '-', '(', '[' or 'not'"
            ))

        return Result.Success (Node)

    def CompExpression (self):
        Result = ParseResult ()

        if self.CurrentToken.Matches (TokenKeyword, 'not'):
            OperatorToken = self.CurrentToken
            Result.RegisterAdvancement ()
            self.Advance ()

            Node = Result.Register (self.CompExpression ())

            if Result.Error:
                return Result

            return Result.Success (UnaryOpNode (OperatorToken, Node))

        Node = Result.Register (self.BinOp (
                self.ArithExpression,
                (
                    TokenEqualsEquals, TokenNotEquals, TokenLessThan, TokenGreaterThan, TokenLessThanEquals, TokenGreaterThanEquals
                )
            )
        )

        if Result.Error:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected int, float, identifier, '+', '-', '(', '[', 'if', 'for', 'while', 'task' or 'not'"
            ))

        return Result.Success (Node)

    def ArithExpression (self):
        return self.BinOp (self.Term, (TokenPlus, TokenMinus))

    def Term (self):
        return self.BinOp (self.Factor, (TokenMultiply, TokenDivide))

    def Factor (self):
        Result = ParseResult ()
        Token = self.CurrentToken

        if Token.Type in (TokenPlus, TokenMinus):
            Result.RegisterAdvancement ()
            self.Advance ()
            Factor = Result.Register (self.Factor())

            if Result.Error:
                return Result

            return Result.Success (UnaryOpNode (Token, Factor))

        return self.Power ()

    def Power (self):
        return self.BinOp (self.Call, (TokenPower, ), self.Factor)

    def Call (self):
        Result = ParseResult ()
        Atom = Result.Register (self.Atom())

        if Result.Error:
            return Result

        if self.CurrentToken.Type == TokenLeftParenthesis:
            Result.RegisterAdvancement ()
            self.Advance ()
            ArgNodes = []

            if self.CurrentToken.Type == TokenRightParenthesis:
                Result.RegisterAdvancement ()
                self.Advance ()

            else:
                ArgNodes.append (Result.Register (self.Expression ()))

                if Result.Error:
                    return Result.Failure (InvalidSyntaxError (
                        self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                        "Expected ')', 'var', 'if', 'for', 'while', 'task', int, float, identifier, '+', '-', '(', '[' or 'not'"
                    ))

                while self.CurrentToken.Type == TokenComma:
                    Result.RegisterAdvancement ()
                    self.Advance ()

                    ArgNodes.append (Result.Register (self.Expression ()))

                    if Result.Error:
                        return Result

                if self.CurrentToken.Type != TokenRightParenthesis:
                    return Result.Failure (InvalidSyntaxError (
                        self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                        f"Expected ',' or ')'"
                    ))

                Result.RegisterAdvancement ()
                self.Advance ()

            return Result.Success (CallNode (Atom, ArgNodes))

        return Result.Success (Atom)

    def Atom (self):
        Result = ParseResult ()
        Token = self.CurrentToken

        if Token.Type in (TokenInt, TokenFloat):
            Result.RegisterAdvancement ()
            self.Advance ()

            return Result.Success (NumberNode (Token))

        elif Token.Type == TokenString:
            Result.RegisterAdvancement ()
            self.Advance ()

            return Result.Success (StringNode (Token))

        elif Token.Type == TokenIdentifier:
            Result.RegisterAdvancement ()
            self.Advance ()

            return Result.Success (VarAccessNode (Token))

        elif Token.Type == TokenLeftParenthesis:
            Result.RegisterAdvancement ()
            self.Advance ()
            Expr = Result.Register (self.Expression ())

            if Result.Error:
                return Result

            if self.CurrentToken.Type == TokenRightParenthesis:
                Result.RegisterAdvancement ()
                self.Advance ()

                return Result.Success (Expr)

            else:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                    "Expected ')'"
                ))

        elif Token.Type == TokenLeftSquareBracket:
            ListExpression = Result.Register (self.ListExpression ())

            if Result.Error:
                return Result

            return Result.Success (ListExpression)

        elif Token.Matches (TokenKeyword, 'if'):
            IfExpression = Result.Register (self.IfExpression ())

            if Result.Error:
                return Result

            return Result.Success (IfExpression)

        elif Token.Matches (TokenKeyword, 'for'):
            ForExpression = Result.Register (self.ForExpression ())

            if Result.Error:
                return Result

            return Result.Success (ForExpression)

        elif Token.Matches (TokenKeyword, 'while'):
            WhileExpression = Result.Register (self.WhileExpression ())

            if Result.Error:
                return Result

            return Result.Success (WhileExpression)

        elif Token.Matches (TokenKeyword, 'task'):
            FunctionDefinition = Result.Register (self.FunctionDefinition ())

            if Result.Error:
                return Result

            return Result.Success (FunctionDefinition)

        elif Token.Matches (TokenKeyword, 'object'):
            ClassDefinition = Result.Register (self.ClassDefinition ())

            if Result.Error:
                return Result

            return Result.Success (ClassDefinition)

        return Result.Failure (InvalidSyntaxError (
            Token.StartPosition, Token.EndPosition,
            "Expected int, float, identifier, '+', '-', '(', '[', IF', 'for', 'while', 'task'"
        ))

    def ListExpression (self):
        Result = ParseResult ()
        ElementNodes = []
        StartPosition = self.CurrentToken.StartPosition.Copy ()

        if self.CurrentToken.Type != TokenLeftSquareBracket:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected '['"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type == TokenRightSquareBracket:
            Result.RegisterAdvancement ()
            self.Advance ()

        else:
            ElementNodes.append (Result.Register (self.Expression ()))

            if Result.Error:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                    "Expected ']', 'var', 'if', 'for', 'while', 'task', int, float, identifier, '+', '-', '(', '[' or 'not'"
                ))

            while self.CurrentToken.Type == TokenComma:
                Result.RegisterAdvancement ()
                self.Advance ()

                ElementNodes.append (Result.Register (self.Expression ()))

                if Result.Error:
                    return Result

            if self.CurrentToken.Type != TokenRightSquareBracket:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                    "Expected ',' or ']'"
                ))

            Result.RegisterAdvancement ()
            self.Advance ()

        return Result.Success (ListNode (
            ElementNodes,
            StartPosition,
            self.CurrentToken.EndPosition.Copy ()
        ))

    def IfExpression (self):
        Result = ParseResult ()
        Cases = []
        ElseCase = None

        if not self.CurrentToken.Matches (TokenKeyword, 'if'):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected 'if'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        Condition = Result.Register (self.Expression ())

        if Result.Error:
            return Result

        if not self.CurrentToken.Matches (TokenKeyword, 'then'):
            return Result.Failure (InvalidSyntaxError(
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected 'then'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        Expr = Result.Register (self.Expression ())

        if Result.Error:
            return Result

        Cases.append ((Condition, Expr))

        while self.CurrentToken.Matches (TokenKeyword, 'elseif'):
            Result.RegisterAdvancement ()
            self.Advance ()

            Condition = Result.Register (self.Expression ())

            if Result.Error:
                return Result

            if not self.CurrentToken.Matches (TokenKeyword, 'then'):
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                    "Expected 'then'"
                ))

            Result.RegisterAdvancement ()
            self.Advance ()

            Expr = Result.Register (self.Expression ())

            if Result.Error:
                return Result

            Cases.append ((Condition, Expr))

        if self.CurrentToken.Matches (TokenKeyword, 'else'):
            Result.RegisterAdvancement ()
            self.Advance ()

            ElseCase = Result.Register (self.Expression ())

            if Result.Error:
                return Result

        return Result.Success (IfNode (Cases, ElseCase))

    def ForExpression (self):
        Result = ParseResult ()

        if not self.CurrentToken.Matches (TokenKeyword, 'for'):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected 'for'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type != TokenIdentifier:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected identifier"
            ))

        VarName = self.CurrentToken
        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type != TokenEquals:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected '='"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        StartValue = Result.Register (self.Expression ())

        if Result.Error:
            return Result

        if not self.CurrentToken.Matches (TokenKeyword, 'to'):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected 'to'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        EndValue = Result.Register (self.Expression ())

        if Result.Error:
            return Result

        if self.CurrentToken.Matches (TokenKeyword, 'step'):
            Result.RegisterAdvancement ()
            self.Advance ()

            StepValue = Result.Register (self.Expression ())

            if Result.Error:
                return Result

        else:
            StepValue = None

        if not self.CurrentToken.Matches (TokenKeyword, 'then'):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected 'then'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        Body = Result.Register (self.Expression ())

        if Result.Error:
            return Result

        return Result.Success (ForNode (VarName, StartValue, EndValue, StepValue, Body))

    def WhileExpression (self):
        Result = ParseResult ()

        if not self.CurrentToken.Matches (TokenKeyword, 'while'):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected 'while'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        Condition = Result.Register (self.Expression ())

        if Result.Error:
            return Result

        if not self.CurrentToken.Matches (TokenKeyword, 'then'):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected 'then'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        Body = Result.Register (self.Expression ())

        if Result.Error:
            return Result

        return Result.Success (WhileNode (Condition, Body))

    def FunctionDefinition (self):
        Result = ParseResult ()

        if not self.CurrentToken.Matches (TokenKeyword, 'task'):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected 'task'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type == TokenIdentifier:
            VarNameToken = self.CurrentToken
            Result.RegisterAdvancement ()
            self.Advance ()

            if self.CurrentToken.Type != TokenLeftParenthesis:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                    "Expected '('"
                ))

        else:
            VarNameToken = None

            if self.CurrentToken.Type != TokenLeftParenthesis:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                    "Expected identifier or '('"
                ))

        Result.RegisterAdvancement ()
        self.Advance ()
        ArgNameTokens = []

        if self.CurrentToken.Type == TokenIdentifier:
            ArgNameTokens.append (self.CurrentToken)
            Result.RegisterAdvancement ()
            self.Advance ()

            while self.CurrentToken.Type == TokenComma:
                Result.RegisterAdvancement ()
                self.Advance ()

                if self.CurrentToken.Type != TokenIdentifier:
                    return Result.Failure (InvalidSyntaxError (
                        self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                        "Expected identifier"
                    ))

                ArgNameTokens.append (self.CurrentToken)
                Result.RegisterAdvancement ()
                self.Advance ()

            if self.CurrentToken.Type != TokenRightParenthesis:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                    "Expected ',' or ')'"
                ))

        else:
            if self.CurrentToken.Type != TokenRightParenthesis:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                    "Expected identifier or ')'"
                ))

        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type != TokenArrow:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected '->'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()
        NodeToReturn = Result.Register (self.Expression ())

        if Result.Error:
            return Result

        return Result.Success (FuncDefNode (
            VarNameToken,
            ArgNameTokens,
            NodeToReturn
        ))

    def ClassDefinition (self):
        Result = ParseResult ()

        if not self.CurrentToken.Matches (TokenKeyword, 'object'):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected 'object'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type == TokenIdentifier:
            VarNameToken = self.CurrentToken
            Result.RegisterAdvancement ()
            self.Advance ()

            if self.CurrentToken.Type != TokenLeftParenthesis:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                    "Expected '('"
                ))

        else:
            VarNameToken = None

            if self.CurrentToken.Type != TokenLeftParenthesis:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                    "Expected identifier or '('"
                ))

        Result.RegisterAdvancement ()
        self.Advance ()
        ArgNameTokens = []

        if self.CurrentToken.Type == TokenIdentifier:
            ArgNameTokens.append (self.CurrentToken)
            Result.RegisterAdvancement ()
            self.Advance ()

            while self.CurrentToken.Type == TokenComma:
                Result.RegisterAdvancement ()
                self.Advance ()

                if self.CurrentToken.Type != TokenIdentifier:
                    return Result.Failure (InvalidSyntaxError (
                        self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                        "Expected identifier"
                    ))

                ArgNameTokens.append (self.CurrentToken)
                Result.RegisterAdvancement ()
                self.Advance ()

            if self.CurrentToken.Type != TokenRightParenthesis:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                    "Expected ',' or ')'"
                ))

        else:
            if self.CurrentToken.Type != TokenRightParenthesis:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                    "Expected identifier or ')'"
                ))

        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type != TokenArrow:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition, self.CurrentToken.EndPosition,
                "Expected '->'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()
        NodeToReturn = Result.Register (self.Expression ())

        if Result.Error:
            return Result

        return Result.Success (ClassDefNode (
            VarNameToken,
            ArgNameTokens,
            NodeToReturn
        ))

    def BinOp (self, _FunctionA, _Operators, _FunctionB = None):
        if _FunctionB == None:
            _FunctionB = _FunctionA

        Result = ParseResult ()
        Left = Result.Register (_FunctionA ())

        if Result.Error:
            return Result

        while self.CurrentToken.Type in _Operators or (self.CurrentToken.Type, self.CurrentToken.Value) in _Operators:
            OperatorToken = self.CurrentToken
            Result.RegisterAdvancement ()
            self.Advance ()
            Right = Result.Register (_FunctionB ())

            if Result.Error:
                return Result

            Left = BinOpNode (Left, OperatorToken, Right)

        return Result.Success (Left)



#######################################
# RUNTIME RESULT
#######################################

class RTResult:
    def __init__(self):
        self.Value = None
        self.Error = None

    def Register (self, _Result):
        self.Error = _Result.Error

        return _Result.Value

    def Success (self, _Value):
        self.Value = _Value

        return self

    def Failure (self, _Error):
        self.Error = _Error

        return self



#######################################
# VALUES
#######################################

class Value:
    def __init__ (self):
        self.SetPosition ()
        self.SetContext ()

    def SetPosition (self, _StartPosition = None, _EndPosition = None):
        self.StartPosition = _StartPosition
        self.EndPosition = _EndPosition

        return self

    def SetContext (self, _Context = None):
        self.Context = _Context

        return self

    def AddedTo (self, _Value):
        return None, self.illegal_operation (_Value)

    def SubtractedBy (self, _Value):
        return None, self.IllegalOperation (_Value)

    def MultipliedBy (self, _Value):
        return None, self.IllegalOperation (_Value)

    def DividedBy (self, _Value):
        return None, self.IllegalOperation (_Value)

    def PowerdBy (self, _Value):
        return None, self.IllegalOperation (_Value)

    def GetComparisonEqual (self, _Value):
        return None, self.IllegalOperation (_Value)

    def GetComparisonNotEqual (self, _Value):
        return None, self.IllegalOperation (_Value)

    def GetComparisonLessThan (self, _Value):
        return None, self.IllegalOperation (_Value)

    def GetComparisonGreaterThan (self, _Value):
        return None, self.IllegalOperation (_Value)

    def GetComparisonLessThanEquals (self, _Value):
        return None, self.IllegalOperation (_Value)

    def GetComparisonGreaterThanEquals (self, _Value):
        return None, self.IllegalOperation (_Value)

    def AndedBy (self, _Value):
        return None, self.IllegalOperation (_Value)

    def OredBy (self, _Value):
        return None, self.IllegalOperation (_Value)

    def Notted (self, _Value):
        return None, self.IllegalOperation (_Value)

    def Execute (self, _Args):
        return RTResult ().Failure (self.IllegalOperation ())

    def Copy (self):
        raise Exception ('No copy method defined')

    def IsTrue (self):
        return False

    def IllegalOperation (self, _Other = None):
        if not _Other:
            _Other = self

        return RTError (
            self.StartPosition, _Other.EndPosition,
            'Illegal operation',
            self.Context
        )

class Number (Value):
    def __init__ (self, Value):
        super ().__init__ ()

        self.Value = Value

    def AddedTo (self, _Value):
        if isinstance (_Value, Number):
            return Number (self.Value + _Value.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def SubtractedBy (self, _Value):
        if isinstance (_Value, Number):
            return Number (self.Value - _Value.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def MultipliedBy (self, _Value):
        if isinstance (_Value, Number):
            return Number (self.Value * _Value.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def DividedBy (self, _Value):
        if isinstance(_Value, Number):
            if _Value.Value == 0:
                return None, RTError (
                    other.StartPosition, other.EndPosition,
                    'Division by zero',
                    self.Context
                )

            return Number (self.Value / _Value.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def PowerdBy (self, _Value):
        if isinstance (_Value, Number):
            return Number (self.Value ** _Value.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def GetComparisonEqual (self, _Value):
        if isinstance (_Value, Number):
            return Number (int (self.Value == _Value.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def GetComparisonNotEqual (self, _Value):
        if isinstance (_Value, Number):
            return Number (int (self.Value != _Value.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def GetComparisonLessThan (self, _Value):
        if isinstance(_Value, Number):
            return Number (int (self.Value < _Value.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def GetComparisonGreaterThan (self, _Value):
        if isinstance(_Value, Number):
            return Number (int (self.Value > _Value.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def GetComparisonLessThanEquals (self, _Value):
        if isinstance(_Value, Number):
            return Number (int (self.Value <= _Value.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def GetComparisonGreaterThanEquals (self, _Value):
        if isinstance(_Value, Number):
            return Number (int (self.Value >= _Value.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def AndedBy (self, _Value):
        if isinstance(_Value, Number):
            return Number (int (self.Value and _Value.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def OredBy (self, _Value):
        if isinstance (_Value, Number):
            return Number (int (self.Value or _Value.Value)).SetContext (self.Context), None
        else:
            return None, Value.IllegalOperation (self, _Value)

    def Notted (self):
        return Number (1 if self.Value == 0 else 0).SetContext (self.Context), None

    def Copy (self):
        Copy = Number (self.Value)
        Copy.SetPosition (self.StartPosition, self.EndPosition)
        Copy.SetContext (self.Context)

        return Copy

    def IsTrue (self):
        return self.Value != 0

    def __repr__(self):
        return str (self.Value)

class String (Value):
    def __init__ (self, Value):
        super ().__init__ ()

        self.Value = Value

    def AddedTo (self, _Value):
        if isinstance(_Value, String):
            return String (self.Value + _Value.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def MultipliedBy (self, _Value):
        if isinstance(_Value, Number):
            return String (self.Value * _Value.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def IsTrue (self):
        return len (self.Value) > 0

    def Copy (self):
        Copy = String (self.Value)
        Copy.SetPosition (self.StartPosition, self.EndPosition)
        Copy.SetContext (self.Context)

        return Copy

    def __repr__ (self):
        #return f'"{self.Value}"'
        return f'{self.Value}'

class List (Value):
    def __init__ (self, Elements):
        super ().__init__ ()

        self.Elements = Elements

    def AddedTo (self, _Value):
        NewList = self.Copy ()
        NewList.Elements.append (_Value)

        return NewList, None

    def SubtractedBy (self, _Value):
        if isinstance (_Value, Number):
            NewList = self.Copy ()

            try:
                NewList.Elements.pop (_Value.Value)

                return NewList, None

            except:
                return None, RTError (
                    _Value.StartPosition, _Value.EndPosition,
                    'Element at this index could not be removed from list because index is out of bounds',
                    self.Context
                )

        else:
            return None, Value.IllegalOperation (self, _Value)

    def MultipliedBy (self, _Value):
        if isinstance (_Value, List):
            NewList = self.Copy ()
            NewList.Elements.extend (_Value.Elements)

            return NewList, None

        else:
            return None, Value.IllegalOperation (self, _Value)

    def DividedBy (self, _Value):
        if isinstance (_Value, Number):
            try:
                return self.Elements[_Value.Value], None

            except:
                return None, RTError (
                    _Value.StartPosition, _Value.EndPosition,
                    'Element at this index could not be retrieved from list because index is out of bounds',
                    self.Context
                )

        else:
            return None, Value.IllegalOperation (self, _Value)

    def Copy (self):
        Copy = List (self.Elements[:])
        Copy.SetPosition (self.StartPosition, self.EndPosition)
        Copy.SetContext (self.Context)

        return Copy

    def __repr__(self):
        return f'[{", ".join ([str (Element) for Element in self.Elements])}]'

class Function (Value):
    def __init__ (self, Name, BodyNode, ArgNames):
        super ().__init__ ()
        self.Name = Name or '<anonymous>'
        self.BodyNode = BodyNode
        self.ArgNames = ArgNames

    def Execute (self, _Args):
        Result = RTResult ()
        NewInterpreter = Interpreter ()
        NewContext = Context (self.Name, self.Context, self.StartPosition)
        NewContext.SymbolTable = SymbolTable (NewContext.Parent.SymbolTable)

        if len (_Args) > len (self.ArgNames):
            return Result.Failure (RTError (
                self.StartPosition, self.EndPosition,
                f"{len (_Args) - len (self.ArgNames)} too many args passed into '{self.Name}'",
                self.Context
            ))

        if len (_Args) < len (self.ArgNames):
            return Result.Failure (RTError (
                self.StartPosition, self.EndPosition,
                f"{len (self.ArgNames) - len (_Args)} too few args passed into '{self.Name}'",
                self.Context
            ))

        for I in range (len (_Args)):
            ArgName = self.ArgNames[I]
            ArgValue = _Args[I]
            ArgValue.SetContext (NewContext)
            NewContext.SymbolTable.Set (ArgName, ArgValue)

        Value = Result.Register (NewInterpreter.Visit (self.BodyNode, NewContext))

        if Result.Error:
            return Result

        return Result.Success  (Value)

    def Copy (self):
        Copy = Function (self.Name, self.BodyNode, self.ArgNames)
        Copy.SetContext (self.Context)
        Copy.SetPosition (self.StartPosition, self.EndPosition)

        return Copy

    def __repr__ (self):
        #return f"<task {self.Name}>"
        return ''

class Class (Value):
    def __init__ (self, Name, BodyNode, ArgNames):
        super ().__init__ ()

        self.Name = Name or '<anonymous>'
        self.BodyNode = BodyNode
        self.ArgNames = ArgNames

    def Execute (self, _Args):
        Result = RTResult ()
        self.Interpreter = Interpreter ()
        self.Context = Context (self.Name, self.Context, self.StartPosition)
        self.Context.SymbolTable = SymbolTable (self.Context.Parent.SymbolTable)

        if len (_Args) > len (self.ArgNames):
            return Result.Failure (RTError (
                self.StartPosition, self.EndPosition,
                f"{len (_Args) - len (self.ArgNames)} too many args passed into '{self.Name}'",
                self.Context
            ))

        if len (_Args) < len (self.ArgNames):
            return Result.Failure (RTError (
                self.StartPosition, self.EndPosition,
                f"{len (self.ArgNames) - len (_Args)} too few args passed into '{self.Name}'",
                self.Context
            ))

        for I in range (len (_Args)):
            ArgName = self.ArgNames[I]
            ArgValue = _Args[I]
            ArgValue.SetContext (NewContext)
            self.Context.SymbolTable.Set (ArgName, ArgValue)

        Value = Result.Register (self.Interpreter.Visit (self.BodyNode, self.Context))

        if Result.Error:
            return Result

        return Result.Success  (Value)

    def Copy (self):
        Copy = Function (self.Name, self.BodyNode, self.ArgNames)
        Copy.SetContext (self.Context)
        Copy.SetPosition (self.StartPosition, self.EndPosition)

        return Copy

    def AddObject (self, _Name, _Node):
        self.Context.SymbolTable.Set (_Name, _Node)

    def __repr__ (self):
        #return f"<task {self.Name}>"
        return ''

class Dict (Value):
    def __init__ (self, Elements):
        super ().__init__ ()

        self.Elements = Elements

class Class (Value):
    def __init__ (self, Name, Values, Functions):
        super ().__init__ ()

        self.Name = Name
        self.Values = Values
        self.Functions = Functions



#######################################
# CONTEXT
#######################################

class Context:
    def __init__(self, DisplayName, Parent = None, ParentEntryPos = None):
        self.DisplayName = DisplayName
        self.Parent = Parent
        self.ParentEntryPos = ParentEntryPos
        self.SymbolTable = None



#######################################
# SYMBOL TABLE
#######################################

class SymbolTable:
    def __init__ (self, Parent = None):
        self.Symbols = {}
        self.Parent = Parent

    def Get (self, _Name):
        Value = self.Symbols.get (_Name, None)

        if Value == None and self.Parent:
            return self.Parent.Get (_Name)

        return Value

    def Set (self, _Name, _Value):
        self.Symbols[_Name] = _Value

    def Remove (self, _Name):
        del self.Symbols[_Name]



#######################################
# INTERPRETER
#######################################

class Interpreter:
    def Visit (self, _Node, _Context):
        MethodName = f'Visit{type (_Node).__name__}'
        Method = getattr (self, MethodName, self.NoVisitMethod)

        return Method (_Node, _Context)

    def NoVisitMethod (self, _Node, _Context):
        raise Exception (f'No Visit{type (_Node).__name__} method defined')

    def VisitNumberNode (self, _Node, _Context):
        return RTResult ().Success  (
            Number (_Node.Token.Value).SetContext (
                _Context).SetPosition (_Node.StartPosition, _Node.EndPosition)
        )

    def VisitStringNode (self, _Node, _Context):
        return RTResult ().Success  (
            String (_Node.Token.Value).SetContext (
                _Context).SetPosition (_Node.StartPosition, _Node.EndPosition)
        )

    def VisitListNode (self, _Node, _Context):
        Result = RTResult ()
        Elements = []

        for ElementNode in _Node.ElementNodes:
            Elements.append (Result.Register (self.Visit (ElementNode, _Context)))

            if Result.Error:
                return Result

        return Result.Success (
            List (Elements).SetContext (_Context).SetPosition (
                _Node.StartPosition, _Node.EndPosition)
        )

    def VisitVarAccessNode (self, _Node, _Context):
        Result = RTResult ()
        VarName = _Node.VarNameToken.Value
        Value = _Context.SymbolTable.Get (VarName)

        if not Value:
            return Result.Failure (RTError (
                _Node.StartPosition, _Node.EndPosition,
                f"'{VarName}' is not defined",
                _Context
            ))

        Value = Value.Copy ().SetPosition (_Node.StartPosition, _Node.EndPosition)
        return Result.Success (Value)

    def VisitVarAssignNode (self, _Node, _Context):
        Result = RTResult ()
        VarName = _Node.VarNameToken.Value
        Value = Result.Register (self.Visit (_Node.ValueNode, _Context))

        if Result.Error:
            return Result

        _Context.SymbolTable.Set (VarName, Value)
        #return Result.Success (Value)
        return Result.Success  ('')

    def VisitBinOpNode (self, _Node, _Context):
        Result = RTResult ()
        Left = Result.Register (self.Visit (_Node.LeftNode, _Context))

        if Result.Error:
            return Result

        Right = Result.Register (self.Visit (_Node.RightNode, _Context))

        if Result.Error:
            return Result

        if _Node.OperatorToken.Type == TokenPlus:
            _Result, Error = Left.AddedTo (Right)

        elif _Node.OperatorToken.Type == TokenMinus:
            _Result, Error = Left.SubtractedBy (Right)

        elif _Node.OperatorToken.Type == TokenMultiply:
            _Result, Error = Left.MultipliedBy (Right)

        elif _Node.OperatorToken.Type == TokenDivide:
            _Result, Error = Left.DividedBy (Right)

        elif _Node.OperatorToken.Type == TokenPower:
            _Result, Error = Left.PowerdBy (Right)

        elif _Node.OperatorToken.Type == TokenEqualsEquals:
            _Result, Error = Left.GetComparisonEqual (Right)

        elif _Node.OperatorToken.Type == TokenNotEquals:
            _Result, Error = Left.GetComparisonNotEqual (Right)

        elif _Node.OperatorToken.Type == TokenLessThan:
            _Result, Error = Left.GetComparisonLessThan (Right)

        elif _Node.OperatorToken.Type == TokenGreaterThan:
            _Result, Error = Left.GetComparisonGreaterThan (Right)

        elif _Node.OperatorToken.Type == TokenLessThanEquals:
            _Result, Error = Left.GetComparisonLessThanEquals (Right)

        elif _Node.OperatorToken.Type == TokenGreaterThanEquals:
            _Result, Error = Left.GetComparisonGreaterThanEquals (Right)

        elif _Node.OperatorToken.Matches (TokenKeyword, 'and'):
            _Result, Error = Left.AndedBy (Right)

        elif _Node.OperatorToken.Matches (TokenKeyword, 'or'):
            _Result, Error = Left.OredBy (Right)

        if Error:
            return Result.Failure (Error)

        else:
            return Result.Success (_Result.SetPosition (_Node.StartPosition, _Node.EndPosition))

    def VisitUnaryOpNode (self, _Node, _Context):
        Result = RTResult ()
        xNumber = Result.Register (self.Visit (_Node.Node, _Context))

        if Result.Error:
            return Result

        Error = None

        if _Node.OperatorToken.Type == TokenMinus:
            xNumber, Error = xNumber.MultipliedBy (Number (-1))

        elif _Node.OperatorToken.Matches (TokenKeyword, 'not'):
            xNumber, Error = xNumber.Notted ()

        if Error:
            return Result.Failure (Error)

        else:
            return Result.Success (xNumber.SetPosition (_Node.StartPosition, _Node.EndPosition))

    def VisitIfNode (self, _Node, _Context):
        Result = RTResult()

        for Condition, Expression in _Node.Cases:
            ConditionValue = Result.Register (self.Visit (Condition, _Context))

            if Result.Error:
                return Result

            if ConditionValue.IsTrue ():
                ExpressionValue = Result.Register (self.Visit (Expression, _Context))

                if Result.Error:
                    return Result

                try:
                    FunctionName = Expression.NodeToCall.VarNameToken.Value
                    Args = []
                    for Arg in Expression.ArgNodes:
                        if isinstance (Arg, VarAccessNode):
                            Args.append (Arg.VarNameToken.Value)

                        elif isinstance (Arg, NumberNode):
                            Args.append (str (Arg.Token.Value))

                        elif isinstance (Arg, StringNode):
                            Args.append (f'"{Arg.Token.Value}"')

                    Args = ', '.join (Args)

                    if FunctionName in GlobalSymbolTable.Symbols:
                        xResult, xError = Run ('<SELF>', f'{FunctionName} ({Args})')

                        if xError:
                            Logs.Error (xError.AsString ())

                        else:
                            print (xResult)

                except:
                    pass

                #return Result.Success (expr_value)
                return Result.Success ('')

        if _Node.ElseCase:
            ElseValue = Result.Register (self.Visit (_Node.ElseCase, _Context))

            if Result.Error:
                return Result

            return Result.Success (ElseValue)

        return Result.Success (None)

    def VisitForNode (self, _Node, _Context):
        Result = RTResult ()
        Elements = []

        StartValue = Result.Register (self.Visit (_Node.StartValueNode, _Context))

        if Result.Error:
            return Result

        EndValue = Result.Register (self.Visit (_Node.EndValueNode, _Context))

        if Result.Error:
            return Result

        if _Node.StepValueNode:
            StepValue = Result.Register (
                self.Visit (_Node.StepValueNode, _Context))

            if Result.Error:
                return Result

        else:
            StepValue = Number (1)

        I = StartValue.Value

        if StepValue.Value >= 0:
            def Condition (): return I < EndValue.Value

        else:
            def Condition (): return I > EndValue.Value

        while Condition ():
            _Context.SymbolTable.Set (_Node.VarNameToken.Value, Number (I))
            I += StepValue.Value

            Elements.append (Result.Register (self.Visit (_Node.BodyNode, _Context)))

            if Result.Error:
                return Result

        return Result.Success (
            List (Elements).SetContext (_Context).SetPosition (
                _Node.StartPosition, _Node.EndPosition)
        )

    def VisitWhileNode (self, _Node, _Context):
        Result = RTResult ()
        Elements = []

        while True:
            Condition = Result.Register (self.Visit (_Node.ConditionNode, _Context))

            if Result.Error:
                return Result

            if not Condition.IsTrue ():
                break

            Elements.append(Result.Register (self.Visit (_Node.BodyNode, _Context)))

            if Result.Error:
                return Result

        return Result.Success (
            List (Elements).SetContext (_Context).SetPosition (
                _Node.StartPosition, _Node.EndPosition)
        )

    def VisitFuncDefNode (self, _Node, _Context):
        Result = RTResult ()

        FuncName = _Node.VarNameToken.Value if _Node.VarNameToken else None
        BodyNode = _Node.BodyNode
        ArgNames = [ArgName.Value for ArgName in _Node.ArgNameTokens]
        FuncValue = Function (FuncName, BodyNode, ArgNames).SetContext (
            _Context).SetPosition (_Node.StartPosition, _Node.EndPosition)

        if _Node.VarNameToken:
            _Context.SymbolTable.Set (FuncName, FuncValue)

        return Result.Success (FuncValue)

    def VisitClassDefNode (self, _Node, _Context):
        Result = RTResult ()

        ClassName = _Node.VarNameToken.Value if _Node.VarNameToken else None
        BodyNode = _Node.BodyNode
        ArgNames = [ArgName.Value for ArgName in _Node.ArgNameTokens]
        ClassValue = Class (ClassName, BodyNode, ArgNames).SetContext (
            _Context).SetPosition (_Node.StartPosition, _Node.EndPosition)

        if _Node.VarNameToken:
            _Context.SymbolTable.Set (ClassName, ClassValue)

        return Result.Success (ClassValue)

    def VisitCallNode (self, _Node, _Context):
        Result = RTResult ()
        Args = []

        ValueToCall = Result.Register (self.Visit (_Node.NodeToCall, _Context))

        if Result.Error:
            return Result

        ValueToCall = ValueToCall.Copy ().SetPosition (_Node.StartPosition, _Node.EndPosition)

        for ArgNode in _Node.ArgNodes:
            Args.append (Result.Register (self.Visit (ArgNode, _Context)))

            if Result.Error:
                return Result

        if _Node.NodeToCall.VarNameToken.Value == 'import':
            Value = DefaultFunctions['import']['Body'][1 : len (DefaultFunctions['import']['Body']) - 1]
            Values = Value.split ('::')
            Path = str (Args[0])

            if Values[0] == 'imp':
                if Values[1] == 'path':
                    try:
                        with open (Path, 'r') as File:
                            Data = File.read ()
                            Lines = Data.split ('\n')

                    except:
                        try:
                            Path = GlobalPath.format (Path)

                            with open (Path, 'r') as File:
                                Data = File.read ()
                                Lines = Data.split ('\n')

                            LoadFromFile (Path, Lines)

                        except:
                            return Result.Failure (RTError (
                                _Node.StartPosition, _Node.EndPosition,
                                f"Cannot open file: '{Args[0]}'",
                                _Context
                            ))

                    LoadFromFile (Path, Lines)

                    return Result.Success ('')

        elif _Node.NodeToCall.VarNameToken.Value == 'read':
            Value = DefaultFunctions['read']['Body'][1 : len (DefaultFunctions['read']['Body']) - 1]
            Values = Value.split ('::')
            Path = str (Args[0])

            if Values[0] == 'read':
                if Values[1] == 'path':
                    try:
                        with open (Path, 'r') as File:
                            Data = File.read ()

                    except:
                        return Result.Failure (RTError (
                            _Node.StartPosition, _Node.EndPosition,
                            f"Cannot open file: '{Args[0]}'",
                            _Context
                        ))

                    return Result.Success (String (Data))

        elif _Node.NodeToCall.VarNameToken.Value == 'iseven':
            Value = DefaultFunctions['iseven']['Body'][1 : len (DefaultFunctions['iseven']['Body']) - 1]
            Values = Value.split ('::')
            Value = int (str (Args[0]))

            if Values[0] == 'iseven':
                if Values[1] == 'number':
                    if Value % 2 == 0:
                        return Result.Success (Number (1))

                    elif Value % 2 == 1:
                        return Result.Success (Number (0))

        elif _Node.NodeToCall.VarNameToken.Value == 'isodd':
            Value = DefaultFunctions['isodd']['Body'][1 : len (DefaultFunctions['isodd']['Body']) - 1]
            Values = Value.split ('::')
            Value = int (str (Args[0]))

            if Values[0] == 'isodd':
                if Values[1] == 'number':
                    if Value % 2 == 0:
                        return Result.Success (Number (0))

                    elif Value % 2 == 1:
                        return Result.Success (Number (1))

        elif _Node.NodeToCall.VarNameToken.Value == 'length':
            Value = DefaultFunctions['length']['Body'][1 : len (DefaultFunctions['length']['Body']) - 1]
            Values = Value.split ('::')
            Value = len (str (Args[0]))

            if Values[0] == 'length':
                if Values[1] == 'value':
                    return Result.Success (Number (Value))

        elif _Node.NodeToCall.VarNameToken.Value == 'split':
            Value = DefaultFunctions['split']['Body'][1 : len (DefaultFunctions['split']['Body']) - 1]
            Values = Value.split ('::')
            Value = str (Args[0]).split (str (Args[1]))

            if Values[0] == 'split':
                if Values[1] == 'string':
                    if Values[2] == 'factor':
                        return Result.Success (List (Value))

        elif _Node.NodeToCall.VarNameToken.Value == 'join':
            Value = DefaultFunctions['join']['Body'][1 : len (DefaultFunctions['join']['Body']) - 1]
            Values = Value.split ('::')
            ValueList = [Element for Element in Args[0].Elements]
            Value = str (Args[1]).join (ValueList)

            if Values[0] == 'join':
                if Values[1] == 'list':
                    if Values[2] == 'factor':
                        return Result.Success (String (Value))

        ReturnValue = Result.Register (ValueToCall.Execute (Args))

        if Result.Error:
            return Result

        return Result.Success (ReturnValue)



#######################################
# RUN
#######################################

GlobalSymbolTable = SymbolTable ()
GlobalSymbolTable.Set ('null', Number (0))
GlobalSymbolTable.Set ('false', Number (0))
GlobalSymbolTable.Set ('true', Number (1))
GlobalSymbolTable.Set ('..', Number (0))

def Run (_File, _Line):
    xLexer = Lexer (_File, _Line)
    Tokens, Error = xLexer.MakeTokens ()

    if Error:
        return None, Error

    xParser = Parser (Tokens)
    AST = xParser.Parse ()

    if AST.Error:
        return None, AST.Error

    xInterpreter = Interpreter ()
    xContext = Context ('<program>')
    xContext.SymbolTable = GlobalSymbolTable
    Result = xInterpreter.Visit (AST.Node, xContext)

    return Result.Value, Result.Error

def LoadFromFile (_Path, _Lines):
    for Line in _Lines:
        if Line == '' or Line in ' \n\t' or Line.startswith ('--'):
            continue

        xResult, xError = Run (_Path, Line)

        if xError:
            Logs.Error (xError.AsString ())
            return

        elif str (xResult) != '':
            print (xResult)

def LoadFunctions (_File, _Functions):
    if isinstance (_Functions, str):
        _Functions = [_Functions]

    elif isinstance (_Functions, dict):
        for Function in _Functions:
            Name = Function
            Function = _Functions[Function]
            FunctionString = f"task {Name} ({', '.join (Function['Args'])}) -> {Function['Body']}"

            Run (_File, FunctionString)

        return

    for Function in _Functions:
        Run (_File, Function)

LoadFunctions ('<self>', DefaultFunctions)
