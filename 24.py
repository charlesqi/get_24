# coding: utf-8

from __future__ import division
from itertools import combinations
from re import findall
from random import randint


class Solver:

    def __init__(self):

        # precise_mode为精准模式，若开启，则减号及除号后开启括号
        self.precise_mode = False

        # 设置是随机出题模式，还是解题模式
        self.is_random = False

        # 设置目标值
        self.target = 24

        # 设置数字的个数
        self.number_count = 4

        # 设置数字的范围下限
        self.minimum = 1

        # 设置数字的范围上限
        self.maximum = 20

        # 初始化存放最终的解法
        self.solutions = None

        # 四则运算符号定义，其中，a -- b = b - a，a // b = b / a
        self.ops = [r'+', r'-', r'*', r'/', r'--', r'//']

    # 输出最终结果
    def output(self, debug_mode=False):
        if self.is_random or debug_mode:
            nums = self.question(debug_mode)
        else:
            nums = []
            for i in range(self.number_count):
                nums.append(' ' + str(input('请输入第' + str(i + 1) + '个数字：')))

        solutions = self.solution(nums)

        print([int(i) for i in nums])
        if len(solutions) == 0:
            print('No solutions')
        else:
            for exp in solutions:
                print(exp.replace(r'*', '×').replace(r'/', '÷'))

    # 出题模式，随机生成题目，如果是debug模式，则不校验是否有解法，否则，校验解法，若无解法则重新出题
    def question(self, debug_mode):
        is_solvable = False
        while not is_solvable:
            result = []
            for i in range(self.number_count):
                result.append(' ' + str(randint(self.minimum, self.maximum)))
            solutions = self.solution(result)
            if debug_mode:
                return result
            if len(solutions) != 0:
                is_solvable = True
                self.solutions = solutions
        return result

    # 解题模式
    def solution(self, nums):
        if self.solutions is None:
            result = []
            groups = self.dimensionality_reduction(nums)
            for group in groups:
                for op in self.ops:
                    exp = self.assemble(group[0], group[1], op)
                    if exp is not None and eval(exp[1:]) == self.target and exp[1:] not in result:
                        result.append(exp[1:])
            return [exp + '=' + str(self.target) for exp in result]
        else:
            return self.solutions

    # 对需要处理的数字或表达式组合进行降维，降低到二维
    def dimensionality_reduction(self, nums):
        result = []

        # 如果维数大于2，则选出两个表达式组合成一个，从而降低一个维度，通过递归降低到二维
        if len(nums) > 2:
            for group1, group2 in self.group(nums, 2):
                for op in self.ops:
                    new_exp = self.assemble(group1[0], group1[1], op)
                    if new_exp is not None:
                        result += self.dimensionality_reduction([new_exp] + group2)
        else:
            result = [nums]
        return result

    # 将两个表达式组合成一个新表达式
    def assemble(self, exp1, exp2, op):

        # 如果运算符为'--'或者'//'，则交换数字顺序重新计算
        if op == r'--' or op == r'//':
            return self.assemble(exp2, exp1, op[0])

        if eval(exp2[1:]) == 0:
            return None

        operators = {
            r'+': 'add',
            r'-': 'subtract',
            r'*': 'multiply',
            r'/': 'divide'
        }

        exp1, exp2 = getattr(self, operators[op])(exp1, exp2)
        return self.convert(op + exp1 + op + exp2)

    # 加法运算
    @staticmethod
    def add(exp1, exp2):
        return exp1[1:], exp2[1:]

    # 减法运算
    def subtract(self, exp1, exp2):
        if self.precise_mode and exp2[0] in r'+-':
            exp2 = self.parenthesis(exp2)
        else:
            exp2 = exp2[1:]
        return exp1[1:], exp2

    # 乘法运算
    def multiply(self, exp1, exp2):
        return self.parenthesis(exp1), self.parenthesis(exp2)

    # 除法运算
    def divide(self, exp1, exp2):
        return self.parenthesis(exp1), self.parenthesis(exp2, self.precise_mode)

    # 根据需要为表达式添加相应的括号
    @staticmethod
    def parenthesis(exp, is_necessary=False):

        # 如果上一计算步骤的运算符号为加号或减号，则需加括号
        if (is_necessary and not exp[1:].isdigit()) or exp[0] in r'+-':
            result = '(' + exp[1:] + ')'
        else:
            result = exp[1:]
        return result

    # 将表达式各项重新排序成为等价标准表达式
    @staticmethod
    def convert(exp):
        if exp[0] in r'+-':
            pattern = r'([\+\-]((\(.+\)|\d+)[\*\/](\(.+\)|\d+)|\d+))'
            exp = r'+' + exp[1:]
        else:
            pattern = r'([\*\/](\(.+?\)|\d+))'
            exp = r'*' + exp[1:]
        result = ''.join(sorted([i[0] for i in findall(pattern, exp)]))
        if len(result) != len(exp):
            result = exp
        return exp[0] + result[1:]

    # 对表达式列表进行分组，返回列表，[[[n1, n2], [n3, n4]], [[n1, n3], [n2, n4]], ...]
    @staticmethod
    def group(exp_list, counter):

        # 生成以下标号为元素的列表
        index_list = [i for i in range(len(exp_list))]

        # 以下标号列表取出不重复的组合
        combination = list(combinations(index_list, counter))

        # 使用下标得到原表达式并组成最终的结果数组
        for group1 in combination:
            group2 = list(set(index_list) - set(group1))
            yield [
                [exp_list[g1] for g1 in group1],
                [exp_list[g2] for g2 in group2]
            ]


Solver().output()
