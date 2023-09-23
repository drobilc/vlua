from luaparser.astnodes import *
from luaparser.utils.visitor import *
from dominate.tags import *

def generate_html(ast):
    visitor = HtmlGenerator()
    return visitor.visit(ast).render()

class HtmlGenerator:

    @visitor(Chunk)
    def visit(self, node) -> html_tag:
        return div(self.visit(node.body), _class='chunk')

    @visitor(Block)
    def visit(self, node: Block) -> html_tag:
        return div(
            *[div(self.visit(statement), _class='statement') for statement in node.body],
            _class='block'
        )

    @visitor(Assign)
    def visit(self, node: Assign) -> html_tag:
        return div(
            self.visit(node.targets),
            ' = ',
            self.visit(node.values),
            _class='assignment'
        )

    @visitor(LocalAssign)
    def visit(self, node: LocalAssign) -> html_tag:
        return "local " + self.visit(node.targets) + " = " + self.visit(node.values)

    @visitor(While)
    def visit(self, node: While) -> html_tag:
        return (
            "while " + self.visit(node.test) + " do\n" + self.visit(node.body) + "\nend"
        )

    @visitor(Do)
    def visit(self, node: Do) -> html_tag:
        return "do\n" + self.visit(node.body) + "\nend"

    @visitor(If)
    def visit(self, node: If) -> html_tag:
        output = (
            "if " + self.visit(node.test) + " then\n" + self.visit(node.body)
        )
        if isinstance(node.orelse, ElseIf):
            output += "\n" + self.visit(node.orelse)
        elif node.orelse:
            output += "\nelse\n" + self.visit(node.orelse)
        output += "\nend"
        return output

    @visitor(ElseIf)
    def visit(self, node: ElseIf) -> html_tag:
        output = (
            "elseif " + self.visit(node.test) + " then\n" + self.visit(node.body)
        )
        if isinstance(node.orelse, ElseIf):
            output += "\n" + self.visit(node.orelse)
        elif node.orelse:
            output += "\nelse\n" + self.visit(node.orelse)
        return output

    @visitor(Label)
    def visit(self, node: Label) -> html_tag:
        return "::" + self.visit(node.id) + "::"

    @visitor(Goto)
    def visit(self, node: Goto) -> html_tag:
        return "goto " + self.visit(node.label)

    @visitor(Break)
    def visit(self, node: Break) -> html_tag:
        return "break"

    @visitor(Return)
    def visit(self, node: Return) -> html_tag:
        return "return " + self.visit(node.values)

    @visitor(Fornum)
    def visit(self, node: Fornum) -> html_tag:
        output = " ".join(
            [
                "for",
                self.visit(node.target),
                "=",
                ", ".join([self.visit(node.start), self.visit(node.stop)]),
            ]
        )
        if node.step != 1:
            output += ", " + self.visit(node.step)
        output += " do\n" + self.visit(node.body) + "\nend"
        return output

    @visitor(Forin)
    def visit(self, node: Forin) -> html_tag:
        return (
            " ".join(
                ["for", self.visit(node.targets), "in", self.visit(node.iter), "do"]
            )
            + "\n"
            + self.visit(node.body)
            + "\nend"
        )

    @visitor(Call)
    def visit(self, node: Call) -> html_tag:
        return self.visit(node.func) + "(" + self.visit(node.args) + ")"

    @visitor(Invoke)
    def visit(self, node: Invoke) -> html_tag:
        return (
            self.visit(node.source)
            + ":"
            + self.visit(node.func)
            + "("
            + self.visit(node.args)
            + ")"
        )

    @visitor(Function)
    def visit(self, node: Function) -> html_tag:
        return (
            "function "
            + self.visit(node.name)
            + "("
            + self.visit(node.args)
            + ")\n"
            + self.visit(node.body)
            + "\nend"
        )

    @visitor(LocalFunction)
    def visit(self, node) -> html_tag:
        return (
            "local function "
            + self.visit(node.name)
            + "("
            + self.visit(node.args)
            + ")\n"
            + self.visit(node.body)
            + "\nend"
        )

    @visitor(Method)
    def visit(self, node: Method) -> html_tag:
        return (
            "function "
            + self.visit(node.source)
            + ":"
            + self.visit(node.name)
            + "("
            + self.visit(node.args)
            + ")\n"
            + self.visit(node.body)
            + "\nend"
        )

    @visitor(Nil)
    def visit(self, node) -> html_tag:
        return "nil"

    @visitor(TrueExpr)
    def visit(self, node) -> html_tag:
        return span("true", _class='boolean')

    @visitor(FalseExpr)
    def visit(self, node) -> html_tag:
        return span("false", _class='boolean')

    @visitor(Number)
    def visit(self, node) -> html_tag:
        return self.visit(node.n)

    @visitor(String)
    def visit(self, node: String) -> html_tag:
        if node.delimiter == StringDelimiter.SINGLE_QUOTE:
            return "'" + self.visit(node.s) + "'"
        elif node.delimiter == StringDelimiter.DOUBLE_QUOTE:
            return '"' + self.visit(node.s) + '"'
        else:
            return "[[" + self.visit(node.s) + "]]"

    @visitor(Table)
    def visit(self, node: Table):
        output = "{\n"
        for field in node.fields:
            output += indent(self.visit(field) + ",\n", " " * self._indent_size)
        output += "}"
        return output

    @visitor(Field)
    def visit(self, node: Field):
        output = "[" if node.between_brackets else ""
        output += self.visit(node.key)
        output += "]" if node.between_brackets else ""
        output += " = "
        output += self.visit(node.value)
        return output

    @visitor(Dots)
    def visit(self, node) -> html_tag:
        return "..."

    @visitor(AnonymousFunction)
    def visit(self, node: AnonymousFunction) -> html_tag:
        return (
            "function("
            + self.visit(node.args)
            + ")\n"
            + self.visit(node.body)
            + "\nend"
        )

    @visitor(AddOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " + " + self.visit(node.right)

    @visitor(SubOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " - " + self.visit(node.right)

    @visitor(MultOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " * " + self.visit(node.right)

    @visitor(FloatDivOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " / " + self.visit(node.right)

    @visitor(FloorDivOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " // " + self.visit(node.right)

    @visitor(ModOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " % " + self.visit(node.right)

    @visitor(ExpoOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " ^ " + self.visit(node.right)

    @visitor(BAndOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " & " + self.visit(node.right)

    @visitor(BOrOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " | " + self.visit(node.right)

    @visitor(BXorOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " ~ " + self.visit(node.right)

    @visitor(BShiftROp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " >> " + self.visit(node.right)

    @visitor(BShiftLOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " << " + self.visit(node.right)

    @visitor(LessThanOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " < " + self.visit(node.right)

    @visitor(GreaterThanOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " > " + self.visit(node.right)

    @visitor(LessOrEqThanOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " <= " + self.visit(node.right)

    @visitor(GreaterOrEqThanOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " >= " + self.visit(node.right)

    @visitor(EqToOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " == " + self.visit(node.right)

    @visitor(NotEqToOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " ~= " + self.visit(node.right)

    @visitor(AndLoOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " and " + self.visit(node.right)

    @visitor(OrLoOp)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + " or " + self.visit(node.right)

    @visitor(Concat)
    def visit(self, node) -> html_tag:
        return self.visit(node.left) + ".." + self.visit(node.right)

    @visitor(UMinusOp)
    def visit(self, node) -> html_tag:
        return "-" + self.visit(node.operand)

    @visitor(UBNotOp)
    def visit(self, node) -> html_tag:
        return "~" + self.visit(node.operand)

    @visitor(ULNotOp)
    def visit(self, node) -> html_tag:
        return "not " + self.visit(node.operand)

    @visitor(ULengthOP)
    def visit(self, node) -> html_tag:
        return "#" + self.visit(node.operand)

    @visitor(Name)
    def visit(self, node: Name) -> html_tag:
        return span(str(node.id), _class='name')

    @visitor(Index)
    def visit(self, node: Index) -> html_tag:
        if node.notation == IndexNotation.DOT:
            return self.visit(node.value) + "." + self.visit(node.idx)
        else:
            return self.visit(node.value) + "[" + self.visit(node.idx) + "]"

    @visitor(Varargs)
    def visit(self, node) -> html_tag:
        return span("...", _class='variable-args')

    @visitor(Repeat)
    def visit(self, node: Repeat) -> html_tag:
        return "repeat\n" + self.visit(node.body) + "\nuntil " + self.visit(node.test)

    @visitor(SemiColon)
    def visit(self, node) -> html_tag:
        return span(";", _class='semicolon')
    
    # Convert Python data types to strings
    @visitor(str)
    def visit(self, node) -> str:
        return str(node)

    @visitor(float)
    def visit(self, node) -> str:
        return str(node)

    @visitor(int)
    def visit(self, node) -> str:
        return str(node)

    @visitor(list)
    def visit(self, node: List) -> html_tag:
        return div(*[self.visit(n) for n in node], _clas='list')

    @visitor(type(None))
    def visit(self, node) -> str:
        return ''