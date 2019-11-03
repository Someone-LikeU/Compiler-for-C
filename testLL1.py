# encoding=utf-8
'''
@author:   pip install zjj =_=
@software: Pycharm
@time:     2019/10/15 20:35
@filename: testLL1.py
@contact:  1326632773@qq.com
'''

from LL1Analysis import LL1GUI
from LL1Analysis import LL1Grammar

gui = LL1GUI()
# fileName = 'LL1grammar3.txt'
# gra = Grammar(fileName)
# print('所选文法如下:')
# for key in gra.grammar.keys():
# 	derivation = gra.grammar[key]
# 	if '' in derivation:
# 		derivation[derivation.index('')] = 'ε'
# 	string = key + '->' + '|'.join(derivation)
# 	print(string)
# print('该文法含最公因子')
# gra.extractCommonLeftFactor
# print('提取左公因子后，该文法为')
# for key in gra.grammar.keys():
# 	derivation = gra.grammar[key]
# 	string = key + '->' + '|'.join(derivation)
# 	print(string)
