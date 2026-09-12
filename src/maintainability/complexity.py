"""Sonar/Campbell cognitive complexity on an AST unit."""

from __future__ import annotations

import ast


def cognitive_complexity(node: ast.AST) -> int:
    visitor = _Cog(self_names=_defined_functions(node))
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        for child in node.body:
            visitor.visit(child)
    elif isinstance(node, ast.ClassDef):
        return 0
    else:
        visitor.visit(node)
    return visitor.score


def _defined_functions(node: ast.AST) -> set[str]:
    names: set[str] = set()
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        names.add(node.name)
    return names


class _Cog(ast.NodeVisitor):
    def __init__(self, self_names: set[str]) -> None:
        self.score = 0
        self.nesting = 0
        self.self_names = self_names

    def _inc(self, extra_nest: bool = True) -> None:
        self.score += 1 + (self.nesting if extra_nest else 0)

    def visit_If(self, node: ast.If) -> None:
        self._inc()
        self.nesting += 1
        for s in node.body:
            self.visit(s)
        self.nesting -= 1
        orelse = node.orelse
        while orelse and len(orelse) == 1 and isinstance(orelse[0], ast.If):
            # elif: +1, no added nest from the if (Sonar else-if)
            self.score += 1
            inner = orelse[0]
            self.nesting += 1
            for s in inner.body:
                self.visit(s)
            self.nesting -= 1
            orelse = inner.orelse
        if orelse:
            self.score += 1
            self.nesting += 1
            for s in orelse:
                self.visit(s)
            self.nesting -= 1

    def visit_For(self, node: ast.For) -> None:
        self._loop(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self._loop(node)

    def visit_While(self, node: ast.While) -> None:
        self._loop(node)

    def _loop(self, node) -> None:
        self._inc()
        self.nesting += 1
        for s in node.body:
            self.visit(s)
        self.nesting -= 1
        if node.orelse:
            self.score += 1
            for s in node.orelse:
                self.visit(s)

    def visit_Try(self, node: ast.Try) -> None:
        for s in node.body:
            self.visit(s)
        for h in node.handlers:
            self._inc()
            self.nesting += 1
            for s in h.body:
                self.visit(s)
            self.nesting -= 1
        for s in node.orelse:
            self.visit(s)
        for s in node.finalbody:
            self.visit(s)

    def visit_Match(self, node: ast.Match) -> None:
        self._inc()
        self.nesting += 1
        for case in node.cases:
            self.score += 1
            for s in case.body:
                self.visit(s)
        self.nesting -= 1

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self._inc()
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        for iff in node.ifs:
            self._inc()
            self.visit(iff)
        self.visit(node.iter)
        self.visit(node.target)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        extra = len(node.values) - 1
        if extra > 0:
            self.score += extra
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        name = None
        if isinstance(func, ast.Name):
            name = func.id
        elif isinstance(func, ast.Attribute):
            name = func.attr
        if name and name in self.self_names:
            self.score += 1
        self.generic_visit(node)
