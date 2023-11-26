from luaparser.astnodes import *
from luaparser.utils.visitor import *
from dominate.tags import *

def generate_html(ast):
    visitor = HtmlGenerator()
    return visitor.visit(ast).render()

class HtmlGenerator:

    @visitor(Chunk)
    def visit(self, node) -> html_tag:
        return html(
            head(link(_rel="stylesheet", _href="style.css")),
            body(self.visit(node.body))
        )

    @visitor(Block)
    def visit(self, node: Block) -> html_tag:
        return span(
            *[span(self.visit(statement), _class='statement') for statement in node.body],
            _class='block'
        )

    @visitor(Assign)
    def visit(self, node: Assign) -> html_tag:
        return span(
            self.visit(node.targets),
            ' = ',
            self.visit(node.values),
            _class='assignment'
        )

    @visitor(LocalAssign)
    def visit(self, node: LocalAssign) -> html_tag:
        return span(
		      strong("local "),
		      self.visit(node.targets),
		      " = ",
		      self.visit(node.values)
				)

    @visitor(While)
    def visit(self, node: While) -> html_tag:
        return div(
            header(strong("while "), self.visit(node.test), strong(" do")),
            self.visit(node.body)
        )

    @visitor(Do)
    def visit(self, node: Do) -> html_tag:
        return div(strong("do "), self.visit(node.body), _class="do")

    @visitor(If)
    def visit(self, node: If) -> html_tag:
        output = div(
            header(strong("if" ), self.visit(node.test)),
            self.visit(node.body), 
            _class="if"
        )
        if isinstance(node.orelse, ElseIf):
            output += div(self.visit(node.orelse), _class="ElseIf")
        elif node.orelse:
            output += div(strong("else "), self.visit(node.orelse), _class="else")
        return output

    @visitor(ElseIf)
    def visit(self, node: ElseIf) -> html_tag:
        output = div(
             header(strong("elif"), self.visit(node.test)),
             self.visit(node.body), 
             _class="elseif"
        )
        if isinstance(node.orelse, ElseIf):
            output += div(self.visit(node.orelse), _class="ElseIf")
        elif node.orelse:
            output +=  div(strong("else "), self.visit(node.orelse), _class="else")
        return output

    @visitor(Label)
    def visit(self, node: Label) -> html_tag:
        return span("::", self.visit(node.id), "::")

    @visitor(Goto)
    def visit(self, node: Goto) -> html_tag:
        return span(strong("goto "), self.visit(node.label))

    @visitor(Break)
    def visit(self, node: Break) -> html_tag:
        return strong("break", _class="break")

    @visitor(Return)
    def visit(self, node: Return) -> html_tag:
        return span(strong("return "), self.visit(node.values), _class="return")

    @visitor(Fornum)
    def visit(self, node: Fornum) -> html_tag:
        return div(
            header(
                strong("for "),
                self.visit(node.target),
                " = ",
                self.visit(node.start), ", ", self.visit(node.stop)
            ),
                span(", ", self.visit(node.step)) if node.step != 1 else "",
                strong(" do "), 
                self.visit(node.body)
        )

    @visitor(Forin)
    def visit(self, node: Forin) -> html_tag:
        return div(
            header(strong("for "), self.visit(node.targets), " in ", self.visit(node.iter), " do"),
            self.visit(node.body)
            )

    @visitor(Call)
    def visit(self, node: Call) -> html_tag:
        return span(strong(self.visit(node.func)) , "( ", self.visit(node.args), " )", _class="call")

    @visitor(Invoke)
    def visit(self, node: Invoke) -> html_tag:
        return span(
            self.visit(node.source),
            ":",
            self.visit(node.func),
            "(",
            self.visit(node.args),
            ")"
        )

    @visitor(Function)
    def visit(self, node: Function) -> html_tag:
        return article(
        		header(strong("function "), self.visit(node.name), "(", self.visit(node.args), ")"),
        		self.visit(node.body)
        	)

    @visitor(LocalFunction)
    def visit(self, node) -> html_tag:
        return article(
        		header(strong("local"),self.visit(node.name), "(", self.visit(node.args), ")"),
        		self.visit(node.body)
        )

    @visitor(Method)
    def visit(self, node: Method) -> html_tag:
        return article(
            header(self.visit(node.source),":", self.visit(node.name), "(", self.visit(node.args), ")" ),
            self.visit(node.body),
            _class="method"
        )

    @visitor(Nil)
    def visit(self, node) -> html_tag:
        return strong("nil", _class="nil")

    @visitor(TrueExpr)
    def visit(self, node) -> html_tag:
        return strong("true", _class='boolean')

    @visitor(FalseExpr)
    def visit(self, node) -> html_tag:
        return strong("false", _class='boolean')

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
        return table(
        	*[self.visit(field) for field in node.fields]
        )

    @visitor(Field)
    def visit(self, node: Field):
        return tr(
		      td("[" if node.between_brackets else "", self.visit(node.key)),
		      td("]" if node.between_brackets else "", self.visit(node.value)),
        )

    @visitor(Dots)
    def visit(self, node) -> html_tag:
        return "..."

    @visitor(AnonymousFunction)
    def visit(self, node: AnonymousFunction) -> html_tag:
        return article(
            "(",
            self.visit(node.args),
            ")=>",
            self.visit(node.body),
            _class="anonymousfunction"
        )

    @visitor(AddOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " + ", self.visit(node.right))

    @visitor(SubOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " - ", self.visit(node.right))

    @visitor(MultOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " * ", self.visit(node.right))

    @visitor(FloatDivOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " / ", self.visit(node.right))

    @visitor(FloorDivOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " // ", self.visit(node.right))

    @visitor(ModOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " % ", self.visit(node.right))

    @visitor(ExpoOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " ^ ", self.visit(node.right))

    @visitor(BAndOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " & ", self.visit(node.right))

    @visitor(BOrOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " | ", self.visit(node.right))

    @visitor(BXorOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " ~ ", self.visit(node.right))

    @visitor(BShiftROp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " >> ", self.visit(node.right))

    @visitor(BShiftLOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " << ", self.visit(node.right), _class="BShiftLOp")

    @visitor(LessThanOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " < ", self.visit(node.right), _class="LessThanOp")

    @visitor(GreaterThanOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " > ", self.visit(node.right), _class="LessOrEqThanOp")

    @visitor(LessOrEqThanOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " <= ", self.visit(node.right), _class="LessOrEqThan")

    @visitor(GreaterOrEqThanOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " >= ", self.visit(node.right), _class="greaterOrEqThan")

    @visitor(EqToOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " == ", self.visit(node.right), _class="eqTo")

    @visitor(NotEqToOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " ~= ", self.visit(node.right), _class="notEq")

    @visitor(AndLoOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " and ", self.visit(node.right), _class="and")

    @visitor(OrLoOp)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), " or ", self.visit(node.right), _class="or")

    @visitor(Concat)
    def visit(self, node) -> html_tag:
        return span(self.visit(node.left), "..", self.visit(node.right), _class="concat")

    @visitor(UMinusOp)
    def visit(self, node) -> html_tag:
        return span("-", self.visit(node.operand), _class="minus")

    @visitor(UBNotOp)
    def visit(self, node) -> html_tag:
        return span("~", self.visit(node.operand), _class="not")

    @visitor(ULNotOp)
    def visit(self, node) -> html_tag:
        return span(strong("not "), self.visit(node.operand), _class="not")

    @visitor(ULengthOP)
    def visit(self, node) -> html_tag:
        return span("#", self.visit(node.operand), _class="length")

    @visitor(Name)
    def visit(self, node: Name) -> html_tag:
        return var(str(node.id), _contenteditable="true")

    @visitor(Index)
    def visit(self, node: Index) -> html_tag:
        if node.notation == IndexNotation.DOT:
            return span(self.visit(node.value), ".", self.visit(node.idx))
        else:
            return span(self.visit(node.value), "[", self.visit(node.idx), "]")

    @visitor(Varargs)
    def visit(self, node) -> html_tag:
        return span("...", _class='variable-args')

    @visitor(Repeat)
    def visit(self, node: Repeat) -> html_tag:
        return div(
            strong("repeat"), 
        	self.visit(node.body),
        	header(strong("until ") , self.visit(node.test))
        	)

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
        return ol(*[li(self.visit(n)) for n in node], _class='list')

    @visitor(type(None))
    def visit(self, node) -> str:
        return ''
