#
# TODO: Fix the config things: %%IF yeet;
# TODO: Also fix: <= >= += -= *= /= ^= %=
#

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

if sys.platform == 'windows':
    Path = 'C:/Users/{}/AppData/Local/Programs/GravPack/Lib/{{}}'

elif sys.platform == 'linux':
    Path = '/home/{}/.shex/{{}}'

# TODO: Add mac support



#######################################
# IMPORTS
#######################################

from Files.Token import *
from Files.Nodes import *
from Files.Position import Position
from Files.Context import ShexContext
from Files.RuntimeResult import RTResult
from Files.SymbolTable import SymbolTable
from Files.ParseResult import ParseResult
from Files.Error import IllegalCharError, ExpectedCharError, InvalidSyntaxError, RTError

import os
import math
import string
from DavesLogger import Logs



#######################################
# CONSTANTS
#######################################

Digits = '0123456789'
Letters = string.ascii_letters
LettersDigits = Letters + Digits



#######################################
# ERRORS
#######################################
"""
class Error:
    def __init__ (self, StartPosition, EndPosition, Name, Error):
        self.StartPosition = StartPosition
        self.EndPosition = EndPosition
        self.Name = Name
        self.Error = Error

    def AsString (self):
        Result = f'{self.Name}: {self.Error}\n'
        Result += f'File {self.StartPosition.FileName}, line {self.StartPosition.Line + 1}'
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
    def __init__ (self, StartPosition, EndPosition, Error, Context):
        super ().__init__ (StartPosition, EndPosition, 'Runtime Error', Error)

        self.Context = Context

    def AsString (self):
        Result  = self.GenerateTraceback ()
        Result += f'{self.Name}: {self.Error}'
        Result += '\n\n' + StringWithArrows (self.StartPosition.FileText, self.StartPosition, self.EndPosition)

        return Result

    def GenerateTraceback (self):
        Result = ''
        Position = self.StartPosition
        Context = self.Context

        while Context:
            Result = f'  File {Position.FileName}, line {str (Position.Line + 1)}, in {Context.DisplayName}\n' + Result
            Position = Context.ParentEntryPos
            Context = Context.Parent

        return 'Traceback (most recent call last):\n' + Result
"""


#######################################
# POSITION
#######################################
"""
class Position:
    def __init__ (self, Index, Line, Column, FileName, FileText):
        self.Index = Index
        self.Line = Line
        self.Column = Column
        self.FileName = FileName
        self.FileText = FileText

    def Advance (self, CurrentChar = None):
        self.Index += 1
        self.Column += 1

        if CurrentChar == '\n':
            self.Line += 1
            self.Column = 0

        return self

    def Copy (self):
        return Position (self.Index, self.Line, self.Column, self.FileName, self.FileText)
"""


#######################################
# TOKENS
#######################################
"""
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

    def Matches (self, Type, Value):
        return self.Type == Type and self.Value == Value

    def __repr__ (self):
        return f'{self.Type}:{self.Value}' if self.Value else f'{self.Type}'
"""


#######################################
# LEXER
#######################################

class ShexLexer:
    def __init__ (self, FileName, Text):
        self.FileName = FileName
        self.Text = Text
        self.Position = Position (-1, 0, -1, FileName, Text)
        self.CurrentChar = None

        self.Advance ()

    def Advance (self):
        self.Position.Advance (self.CurrentChar)
        self.CurrentChar = self.Text[self.Position.Index] if self.Position.Index < len (self.Text) else None

    def Tokenize (self):
        Tokens = []

        while self.CurrentChar != None:
            if self.CurrentChar in ' \t':
                self.Advance ()

            elif self.CurrentChar in ';\n':
                Tokens.append (Token (TokenNewline, StartPosition = self.Position))
                self.Advance ()

            elif self.CurrentChar in Digits:
                Tokens.append (self.MakeNumber ())

            elif self.CurrentChar in Letters:
                Tokens.append (self.MakeIdentifier ())

            elif self.CurrentChar in ('\'', '"'):
                Tokens.append (self.MakeString ())

            elif self.CurrentChar == '`':
                Tokens.append (self.MakeEmbed ())

            elif self.CurrentChar == '%':
                Tokens.append (self.MakeModulo ())

            elif self.CurrentChar == '+':
                Tokens.append (self.MakePlus ())

            elif self.CurrentChar == '-':
                Tokens.append (self.MakeMinus ())

            elif self.CurrentChar == '*':
                Tokens.append (self.MakeMultiply ())

            elif self.CurrentChar == '/':
                Tokens.append (self.MakeDivide ())

            elif self.CurrentChar == '^':
                Tokens.append (self.MakePower ())

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
                _Token, Error = self.MakeNotEquals ()

                if Error:
                    return [], Error

                Tokens.append (_Token)

            elif self.CurrentChar == '=':
                Tokens.append (self.MakeEquals ())

            elif self.CurrentChar == '<':
                Tokens.append (self.MakeLessThan ())

            elif self.CurrentChar == '>':
                Tokens.append (self.MakeGreaterThan ())

            elif self.CurrentChar == ',':
                Tokens.append (Token (TokenComma, StartPosition = self.Position))
                self.Advance ()

            else:
                StartPosition = self.Position.Copy ()
                Char = self.CurrentChar
                self.Advance ()

                return [], IllegalCharError (StartPosition, self.Position, f'\'{Char}\'')

        Tokens.append (Token (TokenEndOfFile, StartPosition = self.Position))

        return Tokens, None

    def MakeNumber (self):
        Number = ''
        Dots = 0
        StartPosition = self.Position.Copy ()

        while self.CurrentChar != None and self.CurrentChar in Digits + '.':
            if self.CurrentChar == '.':
                if Dots == 1:
                    break

                Dots += 1

            Number += self.CurrentChar
            self.Advance ()

        if not Dots:
            return Token (TokenInt, int (Number), StartPosition, self.Position)

        else:
            return Token (TokenFloat, float (Number), StartPosition, self.Position)

    def MakeString (self):
        String = ''
        StartPosition = self.Position.Copy ()
        EscapeCharacter = False

        self.Advance ()

        EscapeCharacters = {
            'n': '\n',
            't': '\t'
        }

        while self.CurrentChar != None and (self.CurrentChar not in ('\'', '"') or EscapeCharacter):
            if EscapeCharacter:
                String += EscapeCharacter.get (self.CurrentChar, self.CurrentChar)

            else:
                if self.CurrentChar == '\\':
                    EscapeCharacter = True

                else:
                    String += self.CurrentChar

            self.Advance ()
            EscapeCharacter = False

        self.Advance ()

        return Token (TokenString, String, StartPosition, self.Position)

    def MakeEmbed (self):
        Embed = ''
        StartPosition = self.Position.Copy ()

        self.Advance ()

        while self.CurrentChar != None and self.CurrentChar != '`':
            if self.CurrentChar == ';':
                self.Advance ()

                if self.CurrentChar == ';':
                    Embed += '\n'

            else:
                Embed += self.CurrentChar

            self.Advance ()

        self.Advance ()

        return Token (TokenEmbed, Embed, StartPosition, self.Position)

    def MakeModulo (self):
        TokenType = TokenModulo
        StartPosition = self.Position.Copy ()

        self.Advance ()

        if self.CurrentChar == '%':
            self.Advance ()

            TokenType = TokenConfig
            Config = ''

            while self.CurrentChar != None and self.CurrentChar != ';':
                Config += self.CurrentChar

                self.Advance ()

            return Token (TokenType, Config, StartPosition = StartPosition, EndPosition = self.Position)

        elif self.CurrentChar == '=':
            self.Advance ()

            TokenType = TokenModuloAssign

        return Token (TokenType, StartPosition = StartPosition, EndPosition = self.Position)

    def MakeIdentifier (self):
        ID = ''
        StartPosition = self.Position.Copy ()

        while self.CurrentChar != None and self.CurrentChar in LettersDigits + '_':
            ID += self.CurrentChar

            self.Advance ()

        TokenType = TokenKeyword if ID in list (Keywords.values ()) else TokenIdentifier

        return Token (TokenType, ID, StartPosition, self.Position)

    def MakePlus (self):
        TokenType = TokenPlus
        StartPosition = self.Position.Copy ()

        self.Advance ()

        if self.CurrentChar == '=':
            self.Advance ()

            TokenType = TokenPlusAssign

        return Token (TokenType, StartPosition = StartPosition, EndPosition = self.Position)

    def MakeMinus (self):
        TokenType = TokenMinus
        StartPosition = self.Position.Copy ()

        self.Advance ()

        if self.CurrentChar == '>':
            self.Advance ()

            TokenType = TokenArrow

        elif self.CurrentChar == '=':
            self.Advance ()

            TokenType = TokenMinusAssign

        return Token (TokenType, StartPosition = StartPosition, EndPosition = self.Position)

    def MakeMultiply (self):
        TokenType = TokenMultiply
        StartPosition = self.Position.Copy ()

        self.Advance ()

        if self.CurrentChar == '=':
            self.Advance ()

            TokenType = TokenMultiplyAssign

        return Token (TokenType, StartPosition = StartPosition, EndPosition = self.Position)

    def MakeDivide (self):
        TokenType = TokenDivide
        StartPosition = self.Position.Copy ()

        self.Advance ()

        if self.CurrentChar == '=':
            self.Advance ()

            TokenType = TokenDivideAssign

        return Token (TokenType, StartPosition = StartPosition, EndPosition = self.Position)

    def MakePower (self):
        TokenType = TokenPower
        StartPosition = self.Position.Copy ()

        self.Advance ()

        if self.CurrentChar == '=':
            self.Advance ()

            TokenType = TokenPowerAssign

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



#######################################
# NODES
#######################################
"""
class NumberNode:
    def __init__ (self, Token):
        self.Token = Token

        self.StartPosition = Token.StartPosition
        self.EndPosition = Token.EndPosition

    def __repr__ (self):
        return f'{self.Token}'

class StringNode:
    def __init__ (self, Token):
        self.Token = Token

        self.StartPosition = Token.StartPosition
        self.EndPosition = Token.EndPosition

    def __repr__ (self):
        return f'{self.Token}'

class EmbedNode:
    def __init__ (self, Token):
        self.Token = Token

        self.StartPosition = Token.StartPosition
        self.EndPosition = Token.EndPosition

    def __repr__ (self):
        return f'{self.Token}'

class ConfigNode:
    def __init__ (self, Token):
        self.Token = Token

        self.StartPosition = Token.StartPosition
        self.EndPosition = Token.EndPosition

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

        self.StartPosition = VarNameToken.StartPosition
        self.EndPosition = VarNameToken.EndPosition

class VarAssignNode:
    def __init__ (self, VarNameToken, ValueNode):
        self.VarNameToken = VarNameToken
        self.ValueNode = ValueNode

        self.StartPosition = VarNameToken.StartPosition
        self.EndPosition = ValueNode.EndPosition

class BinOpNode:
    def __init__ (self, LeftNode, OperatorToken, RightNode):
        self.LeftNode = LeftNode
        self.OperatorToken = OperatorToken
        self.RightNode = RightNode

        self.StartPosition = LeftNode.StartPosition
        self.EndPosition = RightNode.EndPosition

    def __repr__ (self):
        return f'({self.LeftNode}, {self.OperatorToken}, {self.RightNode})'

class UnaryOpNode:
    def __init__ (self, OperatorToken, Node):
        self.OperatorToken = OperatorToken
        self.Node = Node

        self.StartPosition = OperatorToken.StartPosition
        self.EndPosition = Node.EndPosition

    def __repr__ (self):
        return f'({self.OperatorToken}, {self.Node})'

class IfNode:
    def __init__ (self, Cases, ElseCase):
        self.Cases = Cases
        self.ElseCase = ElseCase

        self.StartPosition = Cases[0][0].StartPosition
        self.EndPosition = (ElseCase or Cases[len (Cases) - 1])[0].EndPosition

class ForNode:
    def __init__ (self, VarNameToken, StartValueNode, EndValueNode, StepValueNode, BodyNode, ShouldReturnNull):
        self.VarNameToken = VarNameToken
        self.StartValueNode = StartValueNode
        self.EndValueNode = EndValueNode
        self.StepValueNode = StepValueNode
        self.BodyNode = BodyNode
        self.ShouldReturnNull = ShouldReturnNull

        self.StartPosition = VarNameToken.StartPosition
        self.EndPosition = BodyNode.EndPosition

class WhileNode:
    def __init__ (self, ConditionNode, BodyNode, ShouldReturnNull):
        self.ConditionNode = ConditionNode
        self.BodyNode = BodyNode
        self.ShouldReturnNull = ShouldReturnNull

        self.StartPosition = ConditionNode.StartPosition
        self.EndPosition = BodyNode.EndPosition

class FunctionDefinitionNode:
    def __init__ (self, VarNameToken, ArgNameTokens, BodyNode, ShouldReturnNull):
        self.VarNameToken = VarNameToken
        self.ArgNameTokens = ArgNameTokens
        self.BodyNode = BodyNode
        self.ShouldReturnNull = ShouldReturnNull

        if VarNameToken:
            self.StartPosition = VarNameToken.StartPosition

        elif len (ArgNameTokens) > 0:
            self.StartPosition = ArgNameTokens[0].StartPosition

        else:
            self.StartPosition = BodyNode.StartPosition

        self.EndPosition = BodyNode.EndPosition

class CallNode:
    def __init__ (self, NodeToCall, ArgNodes):
        self.NodeToCall = NodeToCall
        self.ArgNodes = ArgNodes

        self.StartPosition = NodeToCall.StartPosition

        if len (ArgNodes) > 0:
            self.EndPosition = ArgNodes[len (ArgNodes) - 1].EndPosition

        else:
            self.EndPosition = NodeToCall.EndPosition
"""


#######################################
# PARSE RESULT
#######################################
"""
class ParseResult:
    def __init__ (self):
        self.Error = None
        self.Node = None
        self.LastRegisteredAdvanceCount = 0
        self.AdvanceCount = 0
        self.ToReverseCount = 0

    def RegisterAdvancement (self):
        self.LastRegisteredAdvanceCount = 1
        self.AdvanceCount += 1

    def Register (self, Result):
        self.LastRegisteredAdvanceCount = Result.AdvanceCount
        self.AdvanceCount += Result.AdvanceCount

        if Result.Error:
            self.Error = Result.Error

        return Result.Node

    def TryRegister (self, Result):
        if Result.Error:
            self.ToReverseCount = Result.AdvanceCount

            return None

        return self.Register (Result)

    def Success (self, Node):
        self.Node = Node

        return self

    def Failure (self, Error):
        if not self.Error or self.LastRegisteredAdvanceCount == 0:
            self.Error = Error

        return self
"""


#######################################
# PARSER
#######################################

class ShexParser:
    def __init__ (self, Tokens):
        self.Tokens = Tokens
        self.TokenIndex = -1
        self.CurrentToken = None

        self.Advance ()

    def Advance (self):
        self.TokenIndex += 1
        self.UpdateCurrentToken ()

        return self.CurrentToken

    def Reverse (self, Amount = 1):
        self.TokenIndex -= Amount
        self.UpdateCurrentToken ()

        return self.CurrentToken

    def UpdateCurrentToken (self):
        if self.TokenIndex >= 0 and self.TokenIndex < len (self.Tokens):
            self.CurrentToken = self.Tokens[self.TokenIndex]

    def Parse (self):
        Result = self.Statements ()

        if not Result.Error and self.CurrentToken.Type != TokenEndOfFile:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                f"Expected '+', '-', '*', '/', '^', '%', '+=', '-=', '*=', '/=', '^=', '%=', '==', '!=', '<', '>', <=', '>=', '{Keywords['AND']}' or '{Keywords['OR']}'"
            ))

        return Result

    def Statements (self):
        Result = ParseResult ()
        Statements = []
        StartPosition = self.CurrentToken.StartPosition.Copy ()

        while self.CurrentToken.Type == TokenNewline:
            Result.RegisterAdvancement ()
            self.Advance ()

        Statement = Result.Register (self.Expr ())

        # ========================================
        # ||              Okay so               ||
        # ||       I have no idea if this       ||
        # ||       is a good idea. I just       ||
        # ||   do it because it kind of works   ||
        # ||     like it changes it, so ye      ||
        # ||    and I just have this message    ||
        # ||     so I can spot this easier.     ||
        # ========================================
        #if Statement.Token.Type == TokenConfig:
            #Name, Value = Statement.Token.Value.split (' ')

            #if Name in Keywords:
                #Keywords[Name] = Value

        if Result.Error:
            return Result

        Statements.append (Statement)

        MoreStatements = True

        while True:
            NewLineCount = 0

            while self.CurrentToken.Type == TokenNewline:
                Result.RegisterAdvancement ()
                self.Advance ()

                NewLineCount += 1

            if NewLineCount == 0:
                MoreStatements = False

            if not MoreStatements:
                break

            Statement = Result.TryRegister (self.Expr ())

            if not Statement:
                self.Reverse (Result.ToReverseCount)

                MoreStatements = False

                continue

            Statements.append (Statement)

        return Result.Success (ListNode (
            Statements,
            StartPosition,
            self.CurrentToken.EndPosition.Copy ()
        ))

    def Expr (self):
        Result = ParseResult ()

        if self.CurrentToken.Matches (TokenKeyword, Keywords['VAR']):
            Result.RegisterAdvancement ()
            self.Advance ()

            if self.CurrentToken.Type != TokenIdentifier:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition,
                    self.CurrentToken.EndPosition,
                    'Expected identifier'
                ))

            VarName = self.CurrentToken

            Result.RegisterAdvancement ()
            self.Advance ()

            if self.CurrentToken.Type != TokenEquals:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition,
                    self.CurrentToken.EndPosition,
                    "Expected '='"
                ))

            Result.RegisterAdvancement ()
            self.Advance ()

            Expr = Result.Register (self.Expr ())

            if Result.Error:
                return Result

            return Result.Success (VarAssignNode (VarName, Expr))

        Node = Result.Register (self.BinOp (self.CompExpr, ((TokenKeyword, 'and'), (TokenKeyword, 'or'))))

        if Result.Error:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                f"Expected '{Keywords['VAR']}', '{Keywords['IF']}', '{Keywords['FOR']}', '{Keywords['WHILE']}', '{Keywords['TASK']}', int, float, identifier, '+', '-', '(', '[' or '{Keywords['NOT']}'"
            ))

        return Result.Success (Node)

    def CompExpr (self):
        Result = ParseResult ()

        if self.CurrentToken.Matches (TokenKeyword, Keywords['NOT']):
            OperatorToken = self.CurrentToken

            Result.RegisterAdvancement ()
            self.Advance ()

            Node = Result.Register (self.CompExpr ())

            if Result.Error:
                return Result

            return Result.Success (UnaryOpNode (OperatorToken, Node))

        Node = Result.Register (self.BinOp (self.ArithExpr, (TokenEqualsEquals, TokenNotEquals, TokenLessThan, TokenGreaterThan, TokenLessThanEquals, TokenGreaterThan)))

        if Result.Error:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                f"Expected int, float, identifier, '+', '-', '(', '[', '{Keywords['IF']}', '{Keywords['FOR']}', '{Keywords['WHILE']}', '{Keywords['TASK']}' or '{Keywords['NOT']}'"
            ))

        return Result.Success (Node)

    def ArithExpr (self):
        return self.BinOp (self.Term, (TokenPlus, TokenMinus))

    def Term (self):
        return self.BinOp(self.Factor, (TokenMultiply, TokenDivide))

    def Factor (self):
        Result = ParseResult ()
        Token = self.CurrentToken

        if Token.Type in (TokenPlus, TokenMinus):
            Result.RegisterAdvancement ()
            self.Advance ()

            Factor = Result.Register (self.Factor ())

            if Result.Error:
                return Result

            return Result.Success (UnaryOpNode (Token, Factor))

        return self.Power ()

    def Power (self):
        return self.BinOp (self.Call, (TokenPower, ), self.Factor)

    def Call (self):
        Result = ParseResult ()
        Atom = Result.Register (self.Atom ())

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
                ArgNodes.append (Result.Register (self.Expr ()))

                if Result.Error:
                    return Result.Failure (InvalidSyntaxError (
                        self.CurrentToken.StartPosition,
                        self.CurrentToken.EndPosition,
                        f"Expected ')', '{Keywords['VAR']}', '{Keywords['IF']}', '{Keywords['FOR']}', '{Keywords['WHILE']}', '{Keywords['TASK']}', int, float, identifier, '+', '-', '(', '[' or '{Keywords['NOT']}'"
                    ))

                while self.CurrentToken.Type == TokenComma:
                    Result.RegisterAdvancement ()
                    self.Advance ()

                    ArgNodes.append (Result.Register (self.Expr ()))

                    if Result.Error:
                        return Result

                if self.CurrentToken.Type != TokenRightParenthesis:
                    return Result.Failure (InvalidSyntaxError (
                        self.CurrentToken.StartPosition,
                        self.CurrentToken.EndPosition,
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

        elif Token.Type == TokenEmbed:
            Result.RegisterAdvancement ()
            self.Advance ()

            return Result.Success (EmbedNode (Token))

        elif Token.Type == TokenConfig:
            Result.RegisterAdvancement ()
            self.Advance ()

            return Result.Success (ConfigNode (Token))

        elif Token.Type == TokenIdentifier:
            Result.RegisterAdvancement ()
            self.Advance ()

            return Result.Success (VarAccessNode (Token))

        elif Token.Type == TokenLeftParenthesis:
            Result.RegisterAdvancement ()
            self.Advance ()

            Expr = Result.Register (self.Expr ())

            if Result.Error:
                return Result

            if self.CurrentToken.Type == TokenRightParenthesis:
                Result.RegisterAdvancement ()
                self.Advance ()

                return Result.Success (Expr)

            else:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition,
                    self.CurrentToken.EndPosition,
                    "Expected ')'"
                ))

        elif Token.Type == TokenLeftSquareBracket:
            ListExpr = Result.Register (self.ListExpr ())

            if Result.Error:
                return Result

            return Result.Success (ListExpr)

        elif Token.Matches (TokenKeyword, Keywords['IF']):
            IfExpr = Result.Register (self.IfExpr ())

            if Result.Error:
                return Result

            return Result.Success (IfExpr)

        elif Token.Matches (TokenKeyword, Keywords['FOR']):
            ForExpr = Result.Register (self.ForExpr ())

            if Result.Error:
                return Result

            return Result.Success (ForExpr)

        elif Token.Matches (TokenKeyword, Keywords['WHILE']):
            WhileExpr = Result.Register (self.WhileExpr ())

            if Result.Error:
                return Result

            return Result.Success (WhileExpr)

        elif Token.Matches (TokenKeyword, Keywords['TASK']):
            FunctionDefinition = Result.Register (self.FunctionDefinition ())

            if Result.Error:
                return Result

            return Result.Success (FunctionDefinition)

        return Result.Failure (InvalidSyntaxError (
            Token.StartPosition,
            Token.EndPosition,
            f"Expected int, float, identifier, '+', '-', '(', '[', '{Keywords['IF']}', '{Keywords['FOR']}', 'Keywords['WHILE']', 'Keywords['TASK']'"
        ))

    def ListExpr(self):
        Result = ParseResult ()
        ElementNodes = []
        StartPosition = self.CurrentToken.StartPosition.Copy ()

        if self.CurrentToken.Type != TokenLeftSquareBracket:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                "Expected '['"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type == TokenRightSquareBracket:
            Result.RegisterAdvancement ()
            self.Advance ()

        else:
            ElementNodes.append (Result.Register (self.Expr ()))

            if Result.Error:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition,
                    self.CurrentToken.EndPosition,
                    f"Expected ']', '{Keywords['VAR']}', 'Keywords['IF']', 'Keywords['FOR']', 'Keywords['WHILE']', 'Keywords['TASK']', int, float, identifier, '+', '-', '(', '[' or 'Keywords['NOT']'"
                ))

            while self.CurrentToken.Type == TokenComma:
                Result.RegisterAdvancement ()
                self.Advance ()

                ElementNodes.append (Result.Register (self.Expr ()))

                if Result.Error:
                    return Result

            if self.CurrentToken.Type != TokenRightSquareBracket:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition,
                    self.CurrentToken.EndPosition,
                    "Expected ',' or ']'"
                ))

            Result.RegisterAdvancement ()
            self.Advance ()

        return Result.Success (ListNode (
          ElementNodes,
          StartPosition,
          self.CurrentToken.EndPosition.Copy ()
        ))

    def IfExpr (self):
        Result = ParseResult ()
        AllCases = Result.Register (self.IfExprCases (Keywords['IF']))

        if Result.Error:
            return Result

        Cases, ElseCase = AllCases

        return Result.Success (IfNode (Cases, ElseCase))

    def IfExprB (self):
        return self.IfExprCases (Keywords['ELIF'])

    def IfExprC (self):
        Result = ParseResult ()
        ElseCase = None

        if self.CurrentToken.Matches (TokenKeyword, Keywords['ELSE']):
            Result.RegisterAdvancement ()
            self.Advance ()

            if self.CurrentToken.Type == TokenNewline:
                Result.RegisterAdvancement ()
                self.Advance ()

                Statements = Result.Register (self.Statements ())

                if Result.Error:
                    return Result

                ElseCase = (Statements, True)

                if self.CurrentToken.Matches (TokenKeyword, Keywords['DONE']):
                    Result.RegisterAdvancement ()
                    self.Advance ()

                else:
                    return Result.Failure (InvalidSyntaxError (
                        self.CurrentToken.StartPosition,
                        self.CurrentToken.EndPosition,
                        f"Expected '{Keywords['DONE']}'"
                    ))

            else:
                Expr = Result.Register (self.Expr ())

                if Result.Error:
                    return Result

                ElseCase = (Expr, False)

        return Result.Success (ElseCase)

    def IfExprBOrC (self):
        Result = ParseResult ()
        Cases = []
        ElseCase = None

        if self.CurrentToken.Matches (TokenKeyword, Keywords['ELIF']):
            AllCases = Result.Register (self.IfExprB ())

            if Result.Error:
                return Result

            Cases, ElseCase = AllCases

        else:
            ElseCase = Result.Register (self.IfExprC ())

            if Result.Error:
                return Result

        return Result.Success ((Cases, ElseCase))

    def IfExprCases (self, CaseKeyword):
        Result = ParseResult ()
        Cases = []
        ElseCase = None

        if not self.CurrentToken.Matches (TokenKeyword, CaseKeyword):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                f"Expected '{CaseKeyword}'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        Condition = Result.Register (self.Expr ())

        if Result.Error:
            return Result

        if not self.CurrentToken.Matches (TokenKeyword, Keywords['DO']):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                f"Expected '{Keywords['DO']}'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type == TokenNewline:
            Result.RegisterAdvancement ()
            self.Advance ()

            Statements = Result.Register (self.Statements ())

            if Result.Error:
                return Result

            Cases.append ((Condition, Statements, True))

            if self.CurrentToken.Matches (TokenKeyword, Keywords['DONE']):
                Result.RegisterAdvancement ()
                self.Advance ()

            else:
                AllCases = Result.Register (self.IfExprBOrC ())

                if Result.Error:
                    return Result

                NewCases, ElseCase = AllCases
                Cases.extend (NewCases)

        else:
            Expr = Result.Register (self.Expr ())

            if Result.Error:
                return Result

            Cases.append ((Condition, Expr, False))

            AllCases = Result.Register (self.IfExprBOrC ())

            if Result.Error:
                return Result

            NewCases, ElseCase = AllCases
            Cases.extend (NewCases)

        return Result.Success ((Cases, ElseCase))

    def ForExpr (self):
        Result = ParseResult ()

        if not self.CurrentToken.Matches (TokenKeyword, Keywords['FOR']):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                f"Expected '{Keywords['FOR']}'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type != TokenIdentifier:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                "Expected identifier"
            ))

        VarName = self.CurrentToken

        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type != TokenEquals:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                "Expected '='"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        StartValue = Result.Register (self.Expr ())

        if Result.Error:
            return Result

        if not self.CurrentToken.Matches (TokenKeyword, Keywords['TO']):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                f"Expected '{Keywords['TO']}'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        EndValue = Result.Register (self.Expr ())

        if Result.Error:
            return Result

        if self.CurrentToken.Matches (TokenKeyword, Keywords['STEP']):
            Result.RegisterAdvancement ()
            self.Advance ()

            StepValue = Result.Register (self.Expr ())

            if Result.Error:
                return Result

        else:
            StepValue = None

        if not self.CurrentToken.Matches (TokenKeyword, Keywords['DO']):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                f"Expected '{Keywords['DO']}'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type == TokenNewline:
            Result.RegisterAdvancement ()
            self.Advance ()

            Body = Result.Register (self.Statements ())

            if Result.Error:
                return Result

            if not self.CurrentToken.Matches (TokenKeyword, Keywords['DONE']):
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition,
                    self.CurrentToken.EndPosition,
                    f"Expected '{Keywords['DONE']}'"
                ))

            Result.RegisterAdvancement ()
            self.Advance ()

            return Result.Success (ForNode (VarName, StartValue, EndValue, StepValue, Body, True))

        Body = Result.Register (self.Expr ())

        if Result.Error:
            return Result

        return Result.Success (ForNode (VarName, StartValue, EndValue, StepValue, Body, False))

    def WhileExpr (self):
        Result = ParseResult ()

        if not self.CurrentToken.Matches (TokenKeyword, Keywords['WHILE']):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                f"Expected '{Keywords['WHILE']}'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        Condition = Result.Register (self.Expr ())

        if Result.Error:
            return Result

        if not self.CurrentToken.Matches (TokenKeyword, Keywords['DO']):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                f"Expected '{Keywords['DO']}'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type == TokenNewline:
            Result.RegisterAdvancement ()
            self.Advance ()

            Body = Result.Register (self.Statements ())

            if Result.Error:
                return Result

            if not self.CurrentToken.Matches (TokenKeyword, Keywords['DONE']):
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition,
                    self.CurrentToken.EndPosition,
                    f"Expected '{Keywords['DONE']}'"
                ))

            Result.RegisterAdvancement ()
            self.Advance ()

            return Result.Success (WhileNode (Condition, Body, True))

        Body = Result.Register (self.Expr ())

        if Result.Error:
            return Result

        return Result.Success (WhileNode (Condition, Body, False))

    def FunctionDefinition (self):
        Result = ParseResult ()

        if not self.CurrentToken.Matches (TokenKeyword, Keywords['TASK']):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                f"Expected '{Keywords['TASK']}'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type == TokenIdentifier:
            VarNameToken = self.CurrentToken

            Result.RegisterAdvancement ()
            self.Advance ()

            if self.CurrentToken.Type != TokenLeftParenthesis:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition,
                    self.CurrentToken.EndPosition,
                    "Expected '('"
                ))

        else:
            VarNameToken = None

            if self.CurrentToken.Type != TokenLeftParenthesis:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition,
                    self.CurrentToken.EndPosition,
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
                        self.CurrentToken.StartPosition,
                        self.CurrentToken.EndPosition,
                        "Expected identifier"
                    ))

                ArgNameTokens.append (self.CurrentToken)

                Result.RegisterAdvancement ()
                self.Advance ()

            if self.CurrentToken.Type != TokenRightParenthesis:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition,
                    self.CurrentToken.EndPosition,
                    "Expected ',' or ')'"
                ))

        else:
            if self.CurrentToken.Type != TokenRightParenthesis:
                return Result.Failure (InvalidSyntaxError (
                    self.CurrentToken.StartPosition,
                    self.CurrentToken.EndPosition,
                    "Expected identifier or ')'"
                ))

        Result.RegisterAdvancement ()
        self.Advance ()

        if self.CurrentToken.Type == TokenArrow:
            Result.RegisterAdvancement ()
            self.Advance ()

            Body = Result.Register (self.Expr ())

            if Result.Error:
                return Result

            return Result.Success (FunctionDefinitionNode (
              VarNameToken,
              ArgNameTokens,
              Body,
              False
            ))

        if self.CurrentToken.Type != TokenNewline:
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                "Expected '->' or NEWLINE"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        Body = Result.Register (self.Statements ())

        if Result.Error:
            return Result

        if not self.CurrentToken.Matches (TokenKeyword, Keywords['DONE']):
            return Result.Failure (InvalidSyntaxError (
                self.CurrentToken.StartPosition,
                self.CurrentToken.EndPosition,
                f"Expected '{Keywords['DONE']}'"
            ))

        Result.RegisterAdvancement ()
        self.Advance ()

        return Result.Success (FunctionDefinitionNode (
          VarNameToken,
          ArgNameTokens,
          Body,
          # This here used to be True, but I changed it, so functions can now return
          #True
          False
        ))

    def BinOp (self, FunctionA, Operators, FunctionB = None):
        if not FunctionB:
            FunctionB = FunctionA

        Result = ParseResult ()
        Left = Result.Register (FunctionA ())

        if Result.Error:
            return Result

        while self.CurrentToken.Type in Operators or (self.CurrentToken.Type, self.CurrentToken.Value) in Operators:
            OperatorToken = self.CurrentToken

            Result.RegisterAdvancement ()
            self.Advance ()

            Right = Result.Register (FunctionB ())

            if Result.Error:
                return Result

            Left = BinOpNode (Left, OperatorToken, Right)

        return Result.Success (Left)



#######################################
# RUNTIME RESULT
#######################################
"""
class RTResult:
    def __init__ (self):
        self.Value = None
        self.Error = None

    def Register (self, Result):
        self.Error = Result.Error

        return Result.Value

    def Success (self, Value):
        self.Value = Value

        return self

    def Failure (self, Error):
        self.Error = Error

        return self
"""


#######################################
# VALUES
#######################################

class Value:
    def __init__ (self):
        self.SetPosition ()
        self.SetContext ()

    def SetPosition (self, StartPosition = None, EndPosition = None):
        self.StartPosition = StartPosition
        self.EndPosition = EndPosition

        return self

    def SetContext (self, Context = None):
        self.Context = Context

        return self

    def AddedTo (self, Other):
        return None, self.IllegalOperation (Other)

    def SubtractedBy (self, Other):
        return None, self.IllegalOperation (Other)

    def MultipliedBy (self, Other):
        return None, self.IllegalOperation (Other)

    def DividedBy (self, Other):
        return None, self.IllegalOperation (Other)

    def PoweredBy (self, Other):
        return None, self.IllegalOperation (Other)

    def ModulodBy (self, Other):
        return None, self.IllegalOperation (Other)

    def AddedToAssign (self, Other):
        return None, self.IllegalOperation (Other)

    def SubtractedByAssign (self, Other):
        return None, self.IllegalOperation (Other)

    def MultipliedByAssign (self, Other):
        return None, self.IllegalOperation (Other)

    def DividedByAssign (self, Other):
        return None, self.IllegalOperation (Other)

    def PoweredByAssign (self, Other):
        return None, self.IllegalOperation (Other)

    def ModulodByAssign (self, Other):
        return None, self.IllegalOperation (Other)

    def GetComparisonEqual (self, Other):
        return None, self.IllegalOperation (Other)

    def GetComparisonNotEqual (self, Other):
        return None, self.IllegalOperation (Other)

    def GetComparisonLessThan (self, Other):
        return None, self.IllegalOperation (Other)

    def GetComparisonGreaterThan (self, Other):
        return None, self.IllegalOperation (Other)

    def GetComparisonLessThanEquals (self, Other):
        return None, self.IllegalOperation (Other)

    def GetComparisonGreaterThanEquals (self, Other):
        return None, self.IllegalOperation (Other)

    def AndedBy (self, Other):
        return None, self.IllegalOperation (Other)

    def OredBy (self, Other):
        return None, self.IllegalOperation (Other)

    def Notted (self, Other):
        return None, self.IllegalOperation (Other)

    def Execute (self, Args):
        return RTResult ().Failure (self.IllegalOperation ())

    def Copy (self):
        Logs.Error ('No copy method defined!')
        return None

    def IsTrue (self):
        return False

    def IllegalOperation (self, Other = None):
        if not Other:
            Other = self

        return RTError (
            self.StartPosition,
            Other.EndPosition,
            'Illegal operation',
            self.Context
        )

class Number (Value):
    def __init__ (self, Value):
        super ().__init__ ()

        self.Value = Value

    def AddedTo (self, Other):
        if isinstance (Other, Number):
            return Number (self.Value + Other.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def SubtractedBy (self, Other):
        if isinstance (Other, Number):
            return Number (self.Value - Other.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def MultipliedBy (self, Other):
        if isinstance (Other, Number):
            return Number (self.Value * Other.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def DividedBy (self, Other):
        if isinstance (Other, Number):
            if Other.value == 0:
                return None, RTError (
                    Other.StartPosition,
                    Other.EndPosition,
                    'Division by zero',
                    self.Context
                )

            return Number (self.Value / Other.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def PoweredBy (self, Other):
        if isinstance (Other, Number):
            return Number (self.Value ** Other.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def ModulodBy (self, Other):
        if isinstance (Other, Number):
            return Number (self.Value % Other.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def AddedToAssign (self, Other):
        if isinstance (Other, Number):
            self.Value += Other.Value

            return Number (self.Value + Other.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def SubtractedByAssign (self, Other):
        if isinstance (Other, Number):
            self.Value -= Other.Value

            return Number (self.Value - Other.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def MultipliedByAssign (self, Other):
        if isinstance (Other, Number):
            self.Value *= Other.Value

            return Number (self.Value * Other.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def DividedByAssign (self, Other):
        if isinstance (Other, Number):
            self.Value /= Other.Value

            return Number (self.Value / Other.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def PoweredByAssign (self, Other):
        if isinstance (Other, Number):
            self.Value **= Other.Value

            return Number (self.Value ** Other.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def ModulodByAssign (self, Other):
        if isinstance (Other, Number):
            self.Value %= Other.Value

            return Number (self.Value % Other.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def GetComparisonEqual (self, Other):
        if isinstance (Other, Number):
            return Number (int (self.Value == Other.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def GetComparisonNotEqual (self, Other):
        if isinstance (Other, Number):
            return Number (int (self.Value != Other.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def GetComparisonLessThan (self, Other):
        if isinstance (Other, Number):
            return Number (int (self.Value < Other.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def GetComparisonGreaterThan (self, Other):
        if isinstance (Other, Number):
            return Number (int (self.Value > Other.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def GetComparisonLessThanEquals (self, Other):
        if isinstance (Other, Number):
            return Number (int (self.Value <= Other.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def GetComparisonGreaterThanEquals (self, Other):
        if isinstance (Other, Number):
            return Number (int (self.Value >= Other.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def AndedBy (self, Other):
        if isinstance (Other, Number):
            return Number (int (self.Value and Other.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def OredBy (self, Other):
        if isinstance (Other, Number):
            return Number (int (self.Value or Other.Value)).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def Notted (self):
        return Number (1 if self.Value == 0 else 0).SetContext (self.Context), None

    def Copy (self):
        Copy = Number (self.Value)
        Copy.SetPosition (self.StartPosition, self.EndPosition)
        Copy.SetContext (self.Context)

        return Copy

    def IsTrue (self):
        return self.Value != 0

    def __str__ (self):
        return str (self.Value)

    def __repr__ (self):
        return str (self.Value)

Number.Null = Number (0)
Number.FalseValue = Number (0)
Number.TrueValue = Number (1)
Number.Pi = Number (math.pi)

class String (Value):
    def __init__ (self, Value):
        super ().__init__ ()

        self.Value = Value

    def AddedTo (self, Other):
        if isinstance (Other, String):
            return String (self.Value + Other.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def MultipliedBy (self, Other):
        if isinstance (Other, Number):
            return String (self.Value * Other.Value).SetContext (self.Context), None

        else:
            return None, Value.IllegalOperation (self, Other)

    def IsTrue (self):
        return len (self.Value) > 0

    def Copy (self):
        Copy = String (self.Value)
        Copy.SetPosition (self.StartPosition, self.EndPosition)
        Copy.SetContext (self.Context)

        return Copy

    def __str__ (self):
        return str (self.Value)

    def __repr__ (self):
        #return f'"{self.Value}"'
        return self.Value

class List (Value):
    def __init__ (self, Elements):
        super ().__init__ ()

        self.Elements = Elements

    def AddedTo (self, Other):
        NewList = self.Copy ()
        NewList.Elements.append (Other)

        return NewList, None

    def SubtractedBy (self, Other):
        if isinstance (Other, Number):
            NewList = self.Copy ()

            try:
                NewList.Elements.pop (Other.Value)

                return NewList, None

            except:
                return None, RTError (
                    Other.StartPosition,
                    Other.EndPosition,
                    'Element at this index could not be removed from list because index is out of bounds',
                    self.Context
                )

        else:
            return None, Value.IllegalOperation (self, Other)

    def MultipliedBy (self, Other):
        if isinstance (Other, List):
            NewList = self.Copy ()
            NewList.Elements.extend (Other.Elements)

            return NewList, None

        else:
            return None, Value.IllegalOperation (self, Other)

    def DividedBy (self, Other):
        if isinstance (Other, Number):
            try:
                return self.Elements[Other.Value], None

            except:
                return None, RTError (
                    Other.StartPosition,
                    Other.EndPosition,
                    'Element at this index could not be retrieved from list because index is out of bounds',
                    self.Context
                )

        else:
            return None, Value.IllegalOperation (self, Other)

    def Copy (self):
        Copy = List (self.Elements)
        Copy.SetPosition (self.StartPosition, self.EndPosition)
        Copy.SetContext (self.Context)

        return Copy

    def __str__ (self):
        return f'[{", ".join ([str (Element) for Element in self.Elements])}]'
        #return ', '.join ([str (Element) for Element in self.Elements])

    def __repr__ (self):
        return f'[{", ".join ([repr (Element) for Element in self.Elements])}]'

class BaseFunction (Value):
    def __init__ (self, Name):
        super ().__init__ ()

        self.Name = Name or '<anonymous>'

    def GenerateNewContext (self):
        NewContext = ShexContext (self.Name, self.Context, self.StartPosition)
        NewContext.SymbolTable = SymbolTable (NewContext.Parent.SymbolTable)

        return NewContext

    def CheckArgs (self, TakenArgs, GivenArgs):
        Result = RTResult ()

        if len (GivenArgs) > len (TakenArgs):
            return Result.Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                f'{len (GivenArgs) - len (TakenArgs)} too many args passed into {self}',
                self.Context
            ))

        if len (GivenArgs) < len (TakenArgs):
            return Result.Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                f'{len (TakenArgs) - len (GivenArgs)} too few args passed into {self}',
                self.Context
            ))

        return Result.Success (None)

    def PopulateArgs (self, TakenArgs, GivenArgs, ExecuteContext):
        for I in range (len (GivenArgs)):
            TakenArg = TakenArgs[I]
            GivenArg = GivenArgs[I]

            GivenArg.SetContext (ExecuteContext)
            ExecuteContext.SymbolTable.Set (TakenArg, GivenArg)

    def CheckAndPopulateArgs (self, TakenArgs, GivenArgs, ExecuteContext):
        Result = RTResult ()

        Result.Register (self.CheckArgs (TakenArgs, GivenArgs))

        if Result.Error:
            return Result

        self.PopulateArgs (TakenArgs, GivenArgs, ExecuteContext)

        return Result.Success (None)

class Function (BaseFunction):
    def __init__ (self, Name, BodyNode, TakenArgs, ShouldReturnNull):
        super ().__init__ (Name)

        self.BodyNode = BodyNode
        self.TakenArgs = TakenArgs
        self.ShouldReturnNull = ShouldReturnNull

    def Execute (self, GivenArgs):
        Result = RTResult ()
        Interpreter = ShexInterpreter ()

        ExecuteContext = self.GenerateNewContext ()

        Result.Register (self.CheckAndPopulateArgs (self.TakenArgs, GivenArgs, ExecuteContext))

        if Result.Error:
            return Result

        Value = Result.Register (Interpreter.Visit (self.BodyNode, ExecuteContext))

        if isinstance (Value, List):
            if not Value.Elements:
                self.ShouldReturnNull = True

            else:
                Value = Value.Elements[-1]

        else:
            if not Value.Value:
                self.ShouldReturnNull = True

        if Result.Error:
            return Result

        return Result.Success (Number.Null if self.ShouldReturnNull else Value)

    def Copy (self):
        Copy = Function (self.Name, self.BodyNode, self.TakenArgs, self.ShouldReturnNull)
        Copy.SetPosition (self.StartPosition, self.EndPosition)
        Copy.SetContext (self.Context)

        return Copy

    def __repr__ (self):
        return f'<function {self.Name}>'

class BuiltInFunction (BaseFunction):
    def __init__ (self, Name):
        super ().__init__ (Name)

    def Execute (self, Args):
        Result = RTResult ()
        ExecuteContext = self.GenerateNewContext ()

        MethodName = f'Execute{self.Name}'
        Method = getattr (self, MethodName, self.NoVisitMethod)

        Result.Register (self.CheckAndPopulateArgs (Method.TakenArgs, Args, ExecuteContext))

        if Result.Error:
            return Result

        ReturnValue = Result.Register (Method (ExecuteContext))

        if Result.Error:
            return Result

        return Result.Success (ReturnValue)

    def NoVisitMethod (self, Node, Context):
        Logs.Error (f'No Execute{self.Name} method defined')

    def Copy (self):
        Copy = BuiltInFunction (self.Name)
        Copy.SetContext (self.Context)
        Copy.SetPosition (self.StartPosition, self.EndPosition)

        return Copy

    def __repr__ (self):
        return f'<built-in function {self.Name}>'

    def ExecuteImport (self, ExecuteContext):
        FilePath = ExecuteContext.SymbolTable.Get ('File')

        if not isinstance (FilePath, String):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be a string',
                ExecuteContext
            ))

        FilePath = str (FilePath.Value).strip ()

        if not FilePath.endswith ('.shex'):
            FilePath += '.shex'

        try:
            with open (FilePath, 'r') as File:
                Data = File.read ()

        except:
            try:
                FilePath = Path.format (Path)

                with open (FilePath, 'r') as File:
                    Data = File.read ()

                Run (FilePath, Data)

            except:
                return Result.Failure (RTError (
                    self.StartPosition,
                    self.EndPosition,
                    f"Cannot open file: '{Args[0]}'",
                    ExecuteContext
                ))

        Run (FilePath, Data)

        return RTResult ().Success (Number.Null)
    ExecuteImport.TakenArgs = ['File']

    def ExecutePrint (self, ExecuteContext):
        print(str (ExecuteContext.SymbolTable.Get ('Value')))

        return RTResult ().Success (Number.Null)
    ExecutePrint.TakenArgs = ['Value']

    def ExecuteInput (self, ExecuteContext):
        Text = input ()

        return RTResult ().Success (String (Text))
    ExecuteInput.TakenArgs = []

    def ExecuteInputPrompt (self, ExecuteContext):
        Text = input (str (ExecuteContext.SymbolTable.Get ('Prompt')))

        return RTResult ().Success (String (Text))
    ExecuteInputPrompt.TakenArgs = ['Prompt']

    def ExecuteClear (self, ExecuteContext):
        os.system ('cls' if os.name == 'nt' else 'clear')

        return RTResult ().Success (Number.Null)
    ExecuteClear.TakenArgs = []

    def ExecuteIsNumber (self, ExecuteContext):
        IsNumber = isinstance (ExecuteContext.SymbolTable.Get ('Value'), Number)

        return RTResult ().Success (Number.TrueValue if IsNumber else Number.FalseValue)
    ExecuteIsNumber.TakenArgs = ['Value']

    def ExecuteIsString (self, ExecuteContext):
        IsString = isinstance (ExecuteContext.SymbolTable.Get ('Value'), String)

        return RTResult ().Success (Number.TrueValue if IsString else Number.FalseValue)
    ExecuteIsString.TakenArgs = ['Value']

    def ExecuteIsList (self, ExecuteContext):
        IsList = isinstance (ExecuteContext.SymbolTable.Get ('value'), List)

        return RTResult ().Success (Number.TrueValue if IsList else Number.FalseValue)
    ExecuteIsList.TakenArgs = ['Value']

    def ExecuteIsFunction (self, ExecuteContext):
        IsFunction = isinstance (ExecuteContext.SymbolTable.Get ('value'), BaseFunction)

        return RTResult ().Success (Number.TrueValue if IsFunction else Number.FalseValue)
    ExecuteIsFunction.TakenArgs = ['Value']

    def ExecuteAppend (self, ExecuteContext):
        Target = ExecuteContext.SymbolTable.Get ('List')
        Value = ExecuteContext.SymbolTable.Get ('Value')

        if not isinstance (Target, List):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be list',
                ExecuteContext
            ))

        Target.Elements.append (Value)
        return RTResult ().Success(Number.Null)
    ExecuteAppend.TakenArgs = ['List', 'Value']

    def ExecutePop (self, ExecuteContext):
        Target = ExecuteContext.SymbolTable.Get ('List')
        Index = ExecuteContext.SymbolTable.Get ('Index')

        if not isinstance (Target, List):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be list',
                ExecuteContext
            ))

        if not isinstance (Index, Number):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'Second argument must be number',
                ExecuteContext
            ))

        try:
            Element = Target.Elements.pop (Index.Value)

        except:
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'Element at this index could not be removed from list because index is out of bounds',
                ExecuteContext
            ))

        return RTResult ().Success (Element)
    ExecutePop.TakenArgs = ['List', 'Index']

    def ExecuteExtend (self, ExecuteContext):
        ListA = ExecuteContext.SymbolTable.Get ('ListA')
        ListB = ExecuteContext.SymbolTable.Get ('ListB')

        if not isinstance (ListA, List):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be a list',
                ExecuteContext
            ))

        if not isinstance (ListB, List):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'Second argument must be a list',
                ExecuteContext
            ))

        ListA.Elements.extend (ListB.Elements)

        return RTResult ().Success(Number.Null)
    ExecuteExtend.TakenArgs = ['ListA', 'ListB']

    def ExecuteGet (self, ExecuteContext):
        Target = ExecuteContext.SymbolTable.Get ('List')
        Index = ExecuteContext.SymbolTable.Get ('Index')

        if not isinstance (Target, List):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be a list',
                ExecuteContext
            ))

        if not isinstance (Index, Number):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'Second argument must be a number',
                ExecuteContext
            ))

        try:
            Value = Target.Elements[Index.Value]

            if isinstance (Value, String):
                Value = String (Value)

            elif isinstance (Value, Number):
                Value = Number (Value)

            else:
                Value = List (Value)

            return RTResult ().Success (Value)

        except IndexError:
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'Could not get element at that index',
                ExecuteContext
            ))
    ExecuteGet.TakenArgs = ['List', 'Index']

    def ExecuteToInt (self, ExecuteContext):
        Value = ExecuteContext.SymbolTable.Get ('Value')

        try:
            return RTResult ().Success (Number (int (Value.Value)))

        except:
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                f'Cannot convert given value ({str (Value.Value)}) to an int!',
                ExecuteContext
            ))
    ExecuteToInt.TakenArgs = ['Value']

    def ExecuteToString (self, ExecuteContext):
        Value = ExecuteContext.SymbolTable.Get ('Value')

        try:
            return RTResult ().Success (String (str (Value.Value)))

        except:
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                f'Cannot convert given value ({str (Value.Value)}) to a string!',
                ExecuteContext
            ))
    ExecuteToString.TakenArgs = ['Value']

    def ExecuteIsOdd (self, ExecuteContext):
        Value = ExecuteContext.SymbolTable.Get ('Value')

        if not isinstance (Value, Number):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be an int',
                ExecuteContext
            ))

        if int (Value.Value) % 2 == 0:
            return RTResult ().Success (Number (0))

        elif int (Value.Value) % 2 == 1:
            return RTResult ().Success (Number (1))
    ExecuteIsOdd.TakenArgs = ['Value']

    def ExecuteIsEven (self, ExecuteContext):
        Value = ExecuteContext.SymbolTable.Get ('Value')

        if not isinstance (Value, Number):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be an int',
                ExecuteContext
            ))

        if int (Value.Value) % 2 == 0:
            return RTResult ().Success (Number (1))

        elif int (Value.Value) % 2 == 1:
            return RTResult ().Success (Number (0))
    ExecuteIsEven.TakenArgs = ['Value']

    def ExecuteLower (self, ExecuteContext):
        Value = ExecuteContext.SymbolTable.Get ('Value')

        if not isinstance (Value, String):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be a string',
                ExecuteContext
            ))

        return RTResult ().Success (String (str (Value.Value).lower ()))
    ExecuteLower.TakenArgs = ['Value']

    def ExecuteUpper (self, ExecuteContext):
        Value = ExecuteContext.SymbolTable.Get ('Value')

        if not isinstance (Value, String):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be a string',
                ExecuteContext
            ))

        return RTResult ().Success (String (str (Value.Value).upper ()))
    ExecuteUpper.TakenArgs = ['Value']

    def ExecuteRead (self, ExecuteContext):
        Path = ExecuteContext.SymbolTable.Get ('Path')

        if not isinstance (Path, String):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be a string',
                ExecuteContext
            ))

        Data = ''
        if Path:
            with open (Path, 'r') as File:
                Data = File.read ()

        return RTResult ().Success (String (Data))
    ExecuteRead.TakenArgs = ['Path']

    def ExecuteWrite (self, ExecuteContext):
        Path = ExecuteContext.SymbolTable.Get ('Path')
        Mode = ExecuteContext.SymbolTable.Get ('Mode')
        Content = ExecuteContext.SymbolTable.Get ('Content')

        if not isinstance (Path, String):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be a string',
                ExecuteContext
            ))

        if not isinstance (Mode, String):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'Second argument must be a string',
                ExecuteContext
            ))

        if not isinstance (Content, String):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'Third argument must be a string',
                ExecuteContext
            ))

        if Path and Mode:
            with open (Path, Mode) as File:
                File.write (Content)

        return RTResult ().Success (Number (Number.TrueValue))
    ExecuteWrite.TakenArgs = ['Path', 'Mode', 'Content']

    def ExecuteSplit (self, ExecuteContext):
        Value = ExecuteContext.SymbolTable.Get ('String')
        Factor = ExecuteContext.SymbolTable.Get ('Factor')

        if not isinstance (Value, String):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be a string',
                ExecuteContext
            ))

        if not isinstance (Factor, String):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'Second argument must be a string',
                ExecuteContext
            ))

        return RTResult ().Success (List (str (Value.Value).split (str (Factor.Value))))
    ExecuteSplit.TakenArgs = ['String', 'Factor']

    def ExecuteJoin (self, ExecuteContext):
        Value = ExecuteContext.SymbolTable.Get ('String')
        Factor = ExecuteContext.SymbolTable.Get ('Factor')

        if not isinstance (Value, List):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be a list',
                ExecuteContext
            ))

        if not isinstance (Factor, String):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'Second argument must be a string',
                ExecuteContext
            ))

        return RTResult ().Success (String (str (Factor.Value).join (Value.Elements)))
    ExecuteJoin.TakenArgs = ['List', 'Factor']

    def ExecuteLength (self, ExecuteContext):
        Value = ExecuteContext.SymbolTable.Get ('Value')

        if isinstance (Value, List):
            return RTResult ().Success (Number (len (Value.Elements)))

        else:
            return RTResult ().Success (Number (len (Value.Value)))
    ExecuteLength.TakenArgs = ['Value']

    def ExecuteEval (self, ExecuteContext):
        Value = ExecuteContext.SymbolTable.Get ('Value')

        if not isinstance (Value, String):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be a string',
                ExecuteContext
            ))

        return RTResult ().Success (Number (eval (str (Value.Value))))
    ExecuteEval.TakenArgs = ['Value']

    def ExecuteSquareRoot (self, ExecuteContext):
        Value = ExecuteContext.SymbolTable.Get ('Value')

        if not isinstance (Value, Number):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be a number',
                ExecuteContext
            ))

        return RTResult ().Success (Number (math.sqrt (Value.Value)))
    ExecuteSquareRoot.TakenArgs = ['Value']

    def ExecuteType (self, ExecuteContext):
        Type = type (ExecuteContext.SymbolTable.Get ('Value')).__name__

        return RTResult ().Success (String (str (Type)))
    ExecuteType.TakenArgs = ['Value']

    def ExecuteRound (self, ExecuteContext):
        Value = ExecuteContext.SymbolTable.Get ('Value')

        if not isinstance (Value, Number):
            return RTResult ().Failure (RTError (
                self.StartPosition,
                self.EndPosition,
                'First argument must be a number',
                ExecuteContext
            ))

        return RTResult ().Success (Number (round (float (Value.Value))))
    ExecuteRound.TakenArgs = ['Value']

BuiltInFunction.Import      = BuiltInFunction ('Import')
BuiltInFunction.Print       = BuiltInFunction ('Print')
BuiltInFunction.Input       = BuiltInFunction ('Input')
BuiltInFunction.InputPrompt = BuiltInFunction ('InputPrompt')
BuiltInFunction.Clear       = BuiltInFunction ('Clear')
BuiltInFunction.IsNumber    = BuiltInFunction ('IsNumber')
BuiltInFunction.IsString    = BuiltInFunction ('IsString')
BuiltInFunction.IsList      = BuiltInFunction ('IsList')
BuiltInFunction.IsFunction  = BuiltInFunction ('IsFunction')
BuiltInFunction.Append      = BuiltInFunction ('Append')
BuiltInFunction.Pop         = BuiltInFunction ('Pop')
BuiltInFunction.Extend      = BuiltInFunction ('Extend')
BuiltInFunction.Get         = BuiltInFunction ('Get')
BuiltInFunction.ToInt       = BuiltInFunction ('ToInt')
BuiltInFunction.ToString    = BuiltInFunction ('ToString')
BuiltInFunction.IsOdd       = BuiltInFunction ('IsOdd')
BuiltInFunction.IsEven      = BuiltInFunction ('IsEven')
BuiltInFunction.Lower       = BuiltInFunction ('Lower')
BuiltInFunction.Upper       = BuiltInFunction ('Upper')
BuiltInFunction.Read        = BuiltInFunction ('Read')
BuiltInFunction.Write       = BuiltInFunction ('Write')
BuiltInFunction.Split       = BuiltInFunction ('Split')
BuiltInFunction.Join        = BuiltInFunction ('Join')
BuiltInFunction.Length      = BuiltInFunction ('Length')
BuiltInFunction.Eval        = BuiltInFunction ('Eval')
BuiltInFunction.SquareRoot  = BuiltInFunction ('SquareRoot')
BuiltInFunction.Type        = BuiltInFunction ('Type')
BuiltInFunction.Round       = BuiltInFunction ('Round')



#######################################
# CONTEXT
#######################################
"""
class ShexContext:
    def __init__ (self, DisplayName, Parent = None, ParentEntryPosition = None):
        self.DisplayName = DisplayName
        self.Parent = Parent
        self.ParentEntryPosition = ParentEntryPosition
        self.SymbolTable = None
"""



#######################################
# SYMBOL TABLE
#######################################
"""
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
"""


#######################################
# INTERPRETER
#######################################

class ShexInterpreter:
    def Visit (self, Node, Context):
        MethodName = f'Visit{type (Node).__name__}'
        Method = getattr (self, MethodName, self.NoVisitMethod)

        return Method (Node, Context)

    def NoVisitMethod (self, Node, Context):
        Logs.Error (f'No Visit{type (Node).__name__} method defined')

        return None

    def VisitNumberNode (self, Node, Context):
        return RTResult ().Success (
          Number (Node.Token.Value).SetContext (Context).SetPosition (Node.StartPosition, Node.EndPosition)
        )

    def VisitStringNode (self, Node, Context):
        return RTResult ().Success (
          String (Node.Token.Value).SetContext (Context).SetPosition (Node.StartPosition, Node.EndPosition)
        )

    def VisitEmbedNode (self, Node, Context):
        Global = GlobalSymbolTable.Symbols
        Local = Context.SymbolTable.Symbols

        Result = None
        for Line in Node.Token.Value.split ('\n'):
            try:
                Result = eval (Line)

            except:
                Result = exec (Line)

        if Result in (None, False):
            Result = 0

        elif Result == True:
            Result = 1

        if isinstance (Result, str):
            return RTResult ().Success (
                String (Result).SetContext (Context).SetPosition (Node.StartPosition, Node.EndPosition)
            )

        elif isinstance (Result, int):
            return RTResult ().Success (
                Number (Result).SetContext (Context).SetPosition (Node.StartPosition, Node.EndPosition)
            )

        elif isinstance (Result, list):
            def Check (Items):
                Elements = []
                for Item in Items:
                    if isinstance (Item, str):
                        Elements.append (String (Item))

                    elif isinstance (Item, int):
                        Elements.append (Number (Item))

                    elif isinstance (Item, list):
                        Elements.append (Check (Item))

                return Elements

            return RTResult ().Success (
                List (Check (Result)).SetContext (Context).SetPosition (Node.StartPosition, Node.EndPosition)
            )

    def VisitConfigNode (self, Node, Context):
        Name, Value = Node.Token.Value.split (' ')

        if Name in Keywords:
            Keywords[Name] = str (Value)

        #print (123, Keywords)

        return RTResult ().Success (
            Number (Number.Null).SetContext (Context).SetPosition (Node.StartPosition, Node.EndPosition)
        )

    def VisitListNode (self, Node, Context):
        Result = RTResult ()
        Elements = []

        for ElementNode in Node.ElementNodes:
            Elements.append (Result.Register (self.Visit (ElementNode, Context)))

            if Result.Error:
                return Result

        return Result.Success (
          List (Elements).SetContext (Context).SetPosition (Node.StartPosition, Node.EndPosition)
        )

    def VisitVarAccessNode (self, Node, Context):
        Result = RTResult ()
        VarName = Node.VarNameToken.Value
        Value = Context.SymbolTable.Get (VarName)

        if not Value:
            return Result.Failure (RTError (
              Node.StartPosition,
              Node.EndPosition,
              f"'{VarName}' is not defined",
              Context
            ))

        Value = Value.Copy ().SetPosition (Node.StartPosition, Node.EndPosition).SetContext (Context)
        return Result.Success (Value)

    def VisitVarAssignNode (self, Node, Context):
        Result = RTResult ()
        VarName = Node.VarNameToken.Value
        Value = Result.Register (self.Visit (Node.ValueNode, Context))

        if Result.Error:
            return Result

        Context.SymbolTable.Set (VarName, Value)

        return Result.Success (Value)

    def VisitBinOpNode (self, Node, Context):
        Result = RTResult ()
        Left = Result.Register (self.Visit (Node.LeftNode, Context))

        if Result.Error:
            return Result

        Right = Result.Register (self.Visit (Node.RightNode, Context))

        if Result.Error:
            return Result

        if Node.OperatorToken.Type == TokenPlus:
            _Result, Error = Left.AddedTo (Right)

        elif Node.OperatorToken.Type == TokenMinus:
            _Result, Error = Left.SubtractedBy (Right)

        elif Node.OperatorToken.Type == TokenMultiply:
            _Result, Error = Left.MultipliedBy (Right)

        elif Node.OperatorToken.Type == TokenDivide:
            _Result, Error = Left.DividedBy (Right)

        elif Node.OperatorToken.Type == TokenPower:
            _Result, Error = Left.PoweredBy (Right)

        elif Node.OperatorToken.Type == TokenModulo:
            _Result, Error = Left.ModulodBy (Right)

        elif Node.OperatorToken.Type == TokenMinusAssign:
            _Result, Error = Left.SubtractedByAssign (Right)

        elif Node.OperatorToken.Type == TokenMultiplyAssign:
            _Result, Error = Left.MultipliedByAssign (Right)

        elif Node.OperatorToken.Type == TokenDivideAssign:
            _Result, Error = Left.DividedByAssign (Right)

        elif Node.OperatorToken.Type == TokenPowerAssign:
            _Result, Error = Left.PoweredByAssign (Right)

        elif Node.OperatorToken.Type == TokenPlusAssign:
            _Result, Error = Left.ModulodByAssign (Right)

        elif Node.OperatorToken.Type == TokenEqualsEquals:
            _Result, Error = Left.GetComparisonEqual (Right)

        elif Node.OperatorToken.Type == TokenNotEquals:
            _Result, Error = Left.GetComparisonNotEqual (Right)

        elif Node.OperatorToken.Type == TokenLessThan:
            _Result, Error = Left.GetComparisonLessThan (Right)

        elif Node.OperatorToken.Type == TokenGreaterThan:
            _Result, Error = Left.GetComparisonGreaterThan (Right)

        elif Node.OperatorToken.Type == TokenLessThanEquals:
            _Result, Error = Left.GetComparisonLessThanEquals (Right)

        elif Node.OperatorToken.Type == TokenGreaterThanEquals:
            _Result, Error = Left.GetComparisonGreaterThanEquals (Right)

        elif Node.OperatorToken.Matches (TokenKeyword, 'and'):
            _Result, Error = Left.AndedBy (Right)

        elif Node.OperatorToken.Matches (TokenKeyword, 'or'):
            _Result, Error = Left.OredBy (Right)

        if Error:
            return Result.Failure (Error)

        else:
            return Result.Success (_Result.SetPosition (Node.StartPosition, Node.EndPosition))

    def VisitUnaryOpNode (self, Node, Context):
        Result = RTResult ()
        NumberValue = Result.Register (self.Visit (Node.Node, Context))

        if Result.Error:
            return Result

        Error = None

        if Node.OperatorToken.Type == TokenMinus:
            NumberValue, Error = NumberValue.MultipliedBy (Number (-1))

        elif Node.OperatorToken.Matches (TokenKeyword, 'not'):
            NumberValue, Error = NumberValue.Notted ()

        if Error:
            return Result.Failure (Error)

        else:
            return Result.Success (NumberValue.SetPosition (Node.StartPosition, Node.EndPosition))

    def VisitIfNode(self, Node, Context):
        Result = RTResult ()

        for Condition, Expr, ShouldReturnNull in Node.Cases:
            ConditionValue = Result.Register (self.Visit (Condition, Context))

            if Result.Error:
                return Result

            if ConditionValue.IsTrue ():
                ExprValue = Result.Register (self.Visit (Expr, Context))

                if Result.Error:
                    return Result

                return Result.Success (Number.Null if ShouldReturnNull else ExprValue)

        if Node.ElseCase:
            Expr, ShouldReturnNull = Node.ElseCase
            ExprValue = Result.Register (self.Visit (Expr, Context))

            if Result.Error:
                return Result

            return Result.Success (Number.Null if ShouldReturnNull else ExprValue)

        return Result.Success (Number.Null)

    def VisitForNode (self, Node, Context):
        Result = RTResult ()
        Elements = []

        StartValue = Result.Register (self.Visit (Node.StartValueNode, Context))

        if Result.Error:
            return Result

        EndValue = Result.Register (self.Visit (Node.EndValueNode, Context))

        if Result.Error:
            return Result

        if Node.StepValueNode:
            StepValue = Result.Register (self.Visit (Node.StepValueNode, Context))

            if Result.Error:
                return Result

        else:
            StepValue = Number (1)

        I = StartValue.Value

        if StepValue.Value >= 0:
            Condition = lambda: I < EndValue.Value

        else:
            Condition = lambda: I > EndValue.Value

        while Condition ():
            Context.SymbolTable.Set (Node.VarNameToken.Value, Number (I))
            I += StepValue.Value

            Elements.append (Result.Register (self.Visit (Node.BodyNode, Context)))

            if Result.Error:
                return Result

        return Result.Success (
            Number.Null if Node.ShouldReturnNull else
            List (Elements).SetContext (Context).SetPosition (Node.StartPosition, Node.EndPosition)
        )

    def VisitWhileNode (self, Node, Context):
        Result = RTResult ()
        Elements = []

        while True:
            Condition = Result.Register (self.Visit (Node.ConditionNode, Context))

            if Result.Error:
                return Result

            if not Condition.IsTrue ():
                break

            Elements.append (Result.Register (self.Visit (Node.BodyNode, Context)))

            if Result.Error:
                return Result

        return Result.Success (
            Number.Null if Node.ShouldReturnNull else
            List (Elements).SetContext (Context).SetPosition (Node.StartPosition, Node.EndPosition)
        )

    def VisitFunctionDefinitionNode (self, Node, Context):
        Result = RTResult ()

        FunctionName = Node.VarNameToken.Value if Node.VarNameToken else None
        BodyNode = Node.BodyNode
        TakenArgs = [TakenArg.Value for TakenArg in Node.ArgNameTokens]
        FunctionValue = Function (FunctionName, BodyNode, TakenArgs, Node.ShouldReturnNull).SetContext (Context).SetPosition (Node.StartPosition, Node.EndPosition)

        if Node.VarNameToken:
            Context.SymbolTable.Set (FunctionName, FunctionValue)

        return Result.Success (FunctionValue)

    def VisitCallNode (self, Node, Context):
        Result = RTResult ()
        Args = []

        ValueToCall = Result.Register (self.Visit (Node.NodeToCall, Context))

        if Result.Error:
            return Result

        ValueToCall = ValueToCall.Copy ().SetPosition (Node.StartPosition, Node.EndPosition)

        for ArgNode in Node.ArgNodes:
            Args.append (Result.Register (self.Visit (ArgNode, Context)))

            if Result.Error:
                return Result

        ReturnValue = Result.Register (ValueToCall.Execute (Args))

        if Result.Error:
            return Result

        ReturnValue = ReturnValue.Copy ().SetPosition (Node.StartPosition, Node.EndPosition).SetContext (Context)

        return Result.Success (ReturnValue)



#######################################
# RUN
#######################################

GlobalSymbolTable = SymbolTable ()
GlobalSymbolTable.Set ('null', Number.Null)
GlobalSymbolTable.Set ('false', Number.FalseValue)
GlobalSymbolTable.Set ('true', Number.TrueValue)
GlobalSymbolTable.Set ('pi', Number.Pi)
GlobalSymbolTable.Set ('imp', BuiltInFunction.Import)
GlobalSymbolTable.Set ('say', BuiltInFunction.Print)
GlobalSymbolTable.Set ('in', BuiltInFunction.Input)
GlobalSymbolTable.Set ('inp', BuiltInFunction.InputPrompt)
GlobalSymbolTable.Set ('clear', BuiltInFunction.Clear)
GlobalSymbolTable.Set ('cls', BuiltInFunction.Clear)
GlobalSymbolTable.Set ('isnum', BuiltInFunction.IsNumber)
GlobalSymbolTable.Set ('isstr', BuiltInFunction.IsString)
GlobalSymbolTable.Set ('islist', BuiltInFunction.IsList)
GlobalSymbolTable.Set ('istask', BuiltInFunction.IsFunction)
GlobalSymbolTable.Set ('append', BuiltInFunction.Append)
GlobalSymbolTable.Set ('pop', BuiltInFunction.Pop)
GlobalSymbolTable.Set ('extend', BuiltInFunction.Extend)
GlobalSymbolTable.Set ('get', BuiltInFunction.Get)
GlobalSymbolTable.Set ('int', BuiltInFunction.ToInt)
GlobalSymbolTable.Set ('str', BuiltInFunction.ToString)
#GlobalSymbolTable.Set ('isodd', BuiltInFunction.IsOdd)
#GlobalSymbolTable.Set ('iseven', BuiltInFunction.IsEven)
GlobalSymbolTable.Set ('low', BuiltInFunction.Lower)
GlobalSymbolTable.Set ('up', BuiltInFunction.Upper)
GlobalSymbolTable.Set ('read', BuiltInFunction.Read)
GlobalSymbolTable.Set ('write', BuiltInFunction.Write)
GlobalSymbolTable.Set ('split', BuiltInFunction.Split)
GlobalSymbolTable.Set ('join', BuiltInFunction.Join)
GlobalSymbolTable.Set ('len', BuiltInFunction.Length)
GlobalSymbolTable.Set ('eval', BuiltInFunction.Eval)
#GlobalSymbolTable.Set ('sqr', BuiltInFunction.SquareRoot)
GlobalSymbolTable.Set ('typ', BuiltInFunction.Type)
#GlobalSymbolTable.Set ('rnd', BuiltInFunction.Round)

def Run (FileName, Code):
    # Fix the code (Removes comments and none lines)
    Lines = Code.split ('\n')
    Finished = []

    for Line in Lines:
        if not Line.strip () or Line.isspace () or Line.strip ().startswith ('--'):
            continue

        Line = Line.split ('--')[0]

        Finished.append (Line)

    Code = '\n'.join (Finished)

    # Generate tokens
    Lexer = ShexLexer (FileName, Code)
    Tokens, Error = Lexer.Tokenize ()

    if Error:
        Logs.Error (Error.AsString ())

        return None, Error

    # Generate AST
    Parser = ShexParser (Tokens)
    AST = Parser.Parse ()

    if AST.Error:
        Logs.Error (AST.Error.AsString ())

        return None, AST.Error

    # Run program
    Interpreter = ShexInterpreter ()
    Context = ShexContext ('<program>')
    Context.SymbolTable = GlobalSymbolTable
    Result = Interpreter.Visit (AST.Node, Context)

    if Result.Error:
        Logs.Error (Result.Error.AsString ())

    return Result.Value, Result.Error
