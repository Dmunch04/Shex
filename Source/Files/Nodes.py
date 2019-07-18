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
