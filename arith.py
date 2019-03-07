from __future__ import division
import re


class Arith:

    def __init__(self, expression=None, op=None, precise_mode=False):
        self.precise_mode = precise_mode
        self._update(expression, op)

    # 加法运算
    def add(self, obj):

        other_expression, other_op = self._refine(obj)

        if self.expression:
            op = r'+'
            expression = self.expression + op
            expression += other_expression
        else:
            expression, op = other_expression, other_op

        self._update(expression, op)
        return self

    # 减法运算
    def sub(self, obj):

        other_expression, other_op = self._refine(obj)

        if self.expression:
            op = r'-'
            expression = self.expression + op
            other_expression, other_op = self._refine(obj)
            if self.precise_mode:
                other_expression = self._format(other_expression, other_op)
            expression += other_expression
        else:
            expression, op = other_expression, other_op

        self._update(expression, op)
        return self

    # 乘法运算
    def mul(self, obj):

        other_expression, other_op = self._refine(obj)

        if self.expression:
            op = r'*'
            expression = self._format(self.expression, self.op) + op
            other_expression, other_op = self._refine(obj)
            expression += self._format(other_expression, other_op)
        else:
            expression, op = other_expression, other_op

        self._update(expression, op)
        return self

    # 除法运算
    def div(self, obj):

        other_expression, other_op = self._refine(obj)

        if self.expression:
            op = r'/'
            expression = self._format(self.expression, self.op) + op
            other_expression, other_op = self._refine(obj)
            expression += self._format(other_expression, other_op, self.precise_mode)
        else:
            expression, op = other_expression, other_op

        self._update(expression, op)
        return self

    # 分析表达式的符号
    def _analyze(self, expression):
        if expression.isdigit() or not self._calc(expression):
            return None
        else:
            patterns = [
                {
                    'pattern': r'([\*\/](\(.+?\)|\d+))',
                    'op': r'*'
                },
                {
                    'pattern': r'([\+\-]((\(.+\)|\d+)[\*\/](\(.+\)|\d+)|\d+))',
                    'op': r'+'
                }
            ]
            for p in patterns:
                expression = p['op'] + expression
                results = re.findall(p['pattern'], expression)
                if len(results) == 1:
                    continue
                if ''.join([i[0] for i in results]) == expression:
                    return p['op']
        return r'+'

    # 计算表达式的值
    @staticmethod
    def _calc(expression):
        result = None
        try:
            result = eval(expression)
        finally:
            return result

    # 根据需要为表达式添加相应的括号
    @staticmethod
    def _format(expression, op, is_necessary=False):

        if op:
            # 如果上一计算步骤的运算符号为加号或减号，则需加括号
            if is_necessary or op in r'+-':
                return '(' + expression + ')'
            else:
                return expression
        else:
            return expression

    def _refine(self, obj):
        if isinstance(obj, Arith):
            return obj.expression, obj.op
        elif isinstance(obj, int) or isinstance(obj, float):
            return str(obj), None
        elif isinstance(obj, str):
            return obj, self._analyze(obj)
        return None, None

    @staticmethod
    def _sort(expression, op):
        if not expression:
            return None
        if not op or op in r'+-':
            pattern = r'([\+\-]((\(.+\)|\d+)[\*\/](\(.+\)|\d+)|\d+))'
            expression = r'+' + expression
        else:
            pattern = r'([\*\/](\(.+?\)|\d+))'
            expression = r'*' + expression
        result = ''.join(sorted([i[0] for i in re.findall(pattern, expression)]))
        if len(result) != len(expression):
            result = expression
        return result[1:]

    def _update(self, expression, op):
        self.op = op
        if isinstance(expression, int) or isinstance(expression, float):
            expression = str(expression)
        self.expression = self._sort(expression, self.op)
        self.value = self._calc(expression)
