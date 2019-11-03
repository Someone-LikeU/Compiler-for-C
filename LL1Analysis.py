# encoding=utf-8
'''
@author:   pip install zjj =_=
@software: Pycharm
@time:     2019/10/11 16:31
@filename: LL1Analysis.py
@contact:  1326632773@qq.com
'''

from tkinter.filedialog import askopenfilename
import tkinter.messagebox as messagebox
from tkinter import *
import random

class LL1GUI:
	
	#初始化，包括窗体，按钮等,要用到文法，所以给一个文法参数
	def __init__(self):
		self.window = Tk()  # 创建一个窗口
		self.window.title('LL(1)分析')# 标题
		self.LL1Grammar = None # 文法对象先初始化为None，待打开文件后再初始化 todo 先在GUI上打开文件，再把传递给这个文法对象
		self.program = "" # 待分析的程序段
		self.grammarLabels = []  # 记录展示的文法和对应的first和follow的标签
		self.predictTableLabels = [] # 同理，记录预测分析表的标签
		frame =  Frame(self.window) # 这个框架放介绍文字
		frame1 = Frame(self.window) # 这个框架放提示输入文法
		frame2 = Frame(self.window) # 这个框架放读取文法程序
		self.frame3 = Frame(self.window) # 这个框架放文法，first集，follow集
		frame4 = Frame(self.window) # 这个框架放输入程序段的位置
		frame5 = Frame(self.window, width = 100, height = 40)# 放分析结果
		self.frame6 = Frame(self.window) #放分析表，框架3和6是在选择文法和产生分析表后才显示，所以定义成self形式
		
		frame.pack()
		frame1.pack()
		frame2.pack()
		self.frame3.pack()
		frame4.pack()
		frame5.pack()
		self.frame6.pack()
		
		self.v1 = StringVar() # 获取文本文件的输入框
		self.v2 = StringVar() # 获取输入程序段的文本框
		#添加标签，输入框，按钮等组件
		welcome = Label(frame, text = 'LL(1)文法分析器', font = ('KaiTi', 15), anchor = 'center')
		promptEnterFile = Label(frame1, text = '请输入一个文法文本名：', font = ('KaiTi', 13))
		entryLL1Grammar = Entry(frame1, textvariable = self.v1, justify = LEFT, width = 15, font = ('KaiTi', 13))
		btConfirm = Button(frame1, text = '确定', font = ('KaiTi', 13), command = self.__getFileByEntry)
		anotherChoose = Label(frame1, text = '或点击按钮选择文件:', font = ('KaiTi', 13))
		btChoose = Button(frame1, text = '打开', command = self.__getFileByInteract, font = ('KaiTi', 13))
		promptLable = Label(frame2, text = '请输入一个程序段:', font = ('KaiTi', 13))
		entryProgram = Entry(frame2, textvariable = self.v2, justify = LEFT, width = 30, font = ('KaiTi', 13))
		analysisButton = Button(frame2, text = '执行分析', command = self.analysis, font = ('KaiTi', 13))
		exitButton = Button(frame2, text = '退出', command = self.exitPro, font = ('KaiTi', 13))
		welcome.grid()
		promptEnterFile.grid(row = 1, column = 1)
		entryLL1Grammar.grid(row = 1, column = 2)
		btConfirm.grid(row = 1, column = 3)
		anotherChoose.grid(row = 1, column = 4)
		btChoose.grid(row = 1, column = 5)
		promptLable.grid(row = 2, column = 1)
		entryProgram.grid(row = 2, column = 2)
		analysisButton.grid(row = 2, column = 3)
		exitButton.grid(row = 2, column = 4)
		# 放frame4里的东西
		words = ['步骤', '分析栈', '剩余输入串', '所用产生式', '动作']
		for i in range(len(words)):
			Label(frame4, text = words[i], font = ('KaiTi', 14), borderwidth = 2, relief = 'ridge',
			      width = 15, background = 'grey').grid(row = 1, column = i + 1)
		
		# 设置一个滑动条, 再添加到text控件中
		scrollBar = Scrollbar(frame5)
		scrollBar.pack(side = RIGHT, fill = Y)
		self.text = Text(frame5, width = 110, height = 20, wrap = WORD,
		                 yscrollcommand = scrollBar.set)  # 创建一个文本框组件
		self.text.pack()
		scrollBar.config(command = self.text.yview) # 滚动条和text绑定
		
		self.window.mainloop()  # 事件循环
	
	# 交互式选择文法文件
	def __getFileByInteract(self):
		fileName = askopenfilename()
		self.LL1Grammar = LL1Grammar(fileName) # 初始化文法对象
		self.__showLL1Grammar()  #然后展示文法
		if self.predictTableLabels:   # 把前面的文法的分析表删除掉，如果有的话
			for lable in self.predictTableLabels:
				lable.destroy()
		self.text.delete('1.0', END)  # 删掉之前的分析结果
	
	# 在GUI上展示文法和文法的first集，follow集
	def __showLL1Grammar(self):
		if self.grammarLabels :    #每次展示前先把前面一个文法的所有标签删掉
			for label in self.grammarLabels:
				label.destroy()
		self.grammarLabels = []
		r = 1
		col = 1
		l = Label(self.frame3, text = '所选文法如下：', font = ('KaiTi', 14))
		l.grid(row = r, column = col)
		self.grammarLabels.append(l)
		col += 1
		l = Label(self.frame3, text = 'FIRST集与FOLLOW集：', font = ('KaiTi', 14))
		l.grid(row = r, column = col)
		self.grammarLabels.append(l)
		r += 1
		
		for key in self.LL1Grammar.grammar.keys():
			col = 1
			string = key + '->'    # 先展示文法
			tmp = self.LL1Grammar.grammar[key]
			if '' in tmp:  # 展示的时候把空字''替换为'ε'
				tmp[tmp.index('')] = 'ε'
			string += '|'.join(tmp)
			l = Label(self.frame3, text = string, font = ('KaiTi', 12),width = 20,justify = LEFT)
			l.grid(row = r, column = col)
			self.grammarLabels.append(l)
			col = 2
			string = 'FIRST(' + key + '):{'   # 再展示first和follow
			tmp = self.LL1Grammar.First[key]
			if '' in tmp:
				tmp[tmp.index('')] = 'ε'
			string += ','.join(tmp) + '}'
			l = Label(self.frame3, text = string, font = ('KaiTi', 12), width = 25, justify = LEFT)
			l.grid(row = r, column = col)
			self.grammarLabels.append(l)
			col = 3
			string = 'FOLLOW(' + key + '):{'
			string += ','.join(self.LL1Grammar.Follow[key]) + '}'
			l = Label(self.frame3, text = string, font = ('KaiTi', 12), width = 25, justify = LEFT)
			l.grid(row = r, column = col)
			self.grammarLabels.append(l)
			r += 1
	
	def __showPredictTable(self):
		if self.predictTableLabels:   # 每次先把前面的文法的分析表删除掉
			for lable in self.predictTableLabels:
				lable.destroy()
		self.predictTableLabels = []
		r = col = 1
		l = Label(self.frame6, text = '预测分析表', font = ('KaiTi', 14), anchor = 'center')
		l.grid(row = r)
		self.predictTableLabels.append(l)
		r = 2
		l = Label(self.frame6, text = '', width = 8, background = 'grey')
		l.grid(row = r, column = col)
		self.predictTableLabels.append(l)
		col += 1
		for T in self.LL1Grammar.tableTerminater:
			l = Label(self.frame6, text = T, width = 8, background = 'grey',
			      borderwidth = 2, relief = 'ridge')
			l.grid(row = r, column = col)
			self.predictTableLabels.append(l)
			col += 1
		
		r += 1
		for nT in self.LL1Grammar.NonTerminater:
			l = Label(self.frame6, text = nT, width = 8, background = 'grey',
			      borderwidth = 2, relief = 'ridge')
			l.grid(row = r, column = 1)
			self.predictTableLabels.append(l)
			col = 2
			for T in self.LL1Grammar.tableTerminater:
				l = Label(self.frame6, text = self.LL1Grammar.PredictTable[nT][T], width = 8,
				      borderwidth = 2, relief = 'ridge')
				l.grid(row = r, column = col)
				self.predictTableLabels.append(l)
				col += 1
				
			r += 1
		
	# 输入文法名字，打开文法文件
	def __getFileByEntry(self):
		fileName = self.v1.get()
		if fileName != "": # 确保有输入
			try:
				self.LL1Grammar = LL1Grammar(fileName)
				self.__showLL1Grammar()
				if self.predictTableLabels:  # 每次先把前面的文法的分析表删除掉
					for lable in self.predictTableLabels:
						lable.destroy()
				self.text.delete('1.0', END)  # 删掉之前的分析结果
			except IOError:
				self.LL1Grammar = None # 重新赋值文法对象为None
				messagebox.showinfo("错误！", "文件 " + fileName + " 不存在！")
		else:
			messagebox.showinfo("警告！", "未输入文法文件名，请输入！")
		
	
	#获取输入程序段
	def __getProgram(self):
		tmpStr = self.v2.get()
		if tmpStr == '':  # 如果没有输入，就提示错误
			messagebox.showinfo("错误", "请输入程序段！")
		else:  # 有输入,将该字符串返回
			return tmpStr
	
	#执行分析,有错提示错误信息
	def analysis(self):
		if self.LL1Grammar is None:
			messagebox.showinfo("错误!", "未读取文法！请先选择一个文法！")
			return
		self.__showPredictTable()# 展示预测分析表
		self.text.delete('1.0', END)  # 删掉现有的
		stack = Stack() # 先创建一个栈
		index = 0  # 输入程序段的下标
		step = 0 # 计数步骤
		flag = True # 分析结束标志
		success = True
		self.program = self.__getProgram()# 获取输入程序段
		if self.program[-1] != '#': # 如果输入最后不是#，就给它加上个#,防止用户忘记
			self.program += '#'
		while self.program == '':
			self.program = self.__getProgram()
			
		stack.push('#')
		stack.push(self.LL1Grammar.beginChar) # 文法开始符号入栈
		self.text.tag_config('tag', font = ('KaiTi', 13))
		template = "{0:^20}{1:<15}{2:>16}{3:^17}{4:^16}\n"  # 设置展示的格式模板
		sContent = stack.toString()
		self.text.insert(END, template.format(step, sContent, self.program, '', '初始化'), 'tag')
		step += 1
		a = self.program[index]
		while flag:                                     #主控程序
			X = stack.pop() # 取栈顶元素
			print('第', step, '步时，X =', X, 'a =', a)
			if X in self.LL1Grammar.tableTerminater:
				if X == a:
					if X == '#' and a == '#': #先判断是不是分析完了
						flag = False
					elif X == '#' and a != '#':
						messagebox.showinfo("Error", "失败！程序段语法错误！")
						success = False
						break
					else:
						index += 1
						a = self.program[index]
						sContent = stack.toString()
						remain = self.program[index:]
						gen = ''
						action = 'GETNEXT(I)'
						self.text.insert(END, template.format(step, sContent, remain,
						                                      gen, action), 'tag')
						step += 1
				else:
					messagebox.showinfo("Error", "失败！程序段语法错误！")
					success = False
					break
					
			elif self.LL1Grammar.PredictTable[X][a] != '':
				gen = self.LL1Grammar.PredictTable[X][a]
				pos = self.LL1Grammar.PredictTable[X][a].index('>')
				de = self.LL1Grammar.PredictTable[X][a][pos + 1:]
				
				if de != 'ε': # 如果候选不是空字
					tmp = ''
					for i in range(len(de) - 1, -1, -1):  # 把推导倒序入栈
						stack.push(de[i])
						tmp += de[i]
					action = 'POP,PUSH(' + tmp + ')'  # 当前步骤的动作
				else:
					action = 'POP'
				remain = self.program[index:]  # 剩余输入串
				sContent = stack.toString() # 栈内容
				self.text.insert(END, template.format(step, sContent, remain,
				                                      gen, action), 'tag')
				step += 1
			
			else:
				messagebox.showinfo("Error", "失败！程序段语法错误！")
				success = False
				break
		
		if success:
			messagebox.showinfo("Success!", "分析成功！")
	
	def exitPro(self):
		exit(0)
	
# 自定义一个栈类
class Stack:
	
	def __init__(self):
		self.__length = 0   # 记录栈内元素数量
		self.__data = []    # 用一个列表来表示栈
		
	#进栈
	def push(self, x):
		if x == '':
			messagebox.showinfo("Error", "进栈元素不能为空!")
		else:
			self.__data.append(x)
			self.__length += 1
	
	# 弹栈
	def pop(self):
		self.__length = len(self.__data)
		if self.__length == 0:
			messagebox.showinfo("Error", "栈已空，不能pop!")
		else:
			self.__length -= 1
			res = self.__data.pop(self.__length)
			return res
			
	# 栈的所有内容以字符串形式返回
	def toString(self):
		res = ''
		for value in self.__data:
			res += value
		return res
	
	# 查看栈顶元素
	def top(self):
		self.__length = len(self.__data)
		if self.__length == 0:
			messagebox.showinfo("警告", "栈已空!")
		else:
			print()

# 定义文法类
class LL1Grammar:

	def __init__(self, file):
		self.grammar = {} # 创建一个空字典，用于保存文法
		self.First = {}  # 同样用一个字典来保存所有first集
		self.Follow = {} # 所有Follow集
		self.Terminater = [] # 终结符列表
		self.tableTerminater = []
		self.NonTerminater = [] # 非终结符
		self.PredictTable = None
		self.beginChar = None
		# 读取文法，保存成字典
		try:
			f = open(file, 'r')
			for line in f:
				subStr = line[3:].replace('\n', '')   # 提取每个推导的右边推导式并将换行符去掉
				derivation = subStr.split('|')  # 将右边的推导式按'|'分割成多个单个推导，并形成一个列表
				# print(derivation)
				# 处理乱码情况，将 蔚 替换为空串，如果程序采用另一种编码方式，蔚 字可能就变成了其他的，需要修改
				for i in range(len(derivation)):
					if derivation[i] == '蔚':
						derivation[i] = ''
				self.grammar[line[0]] = derivation # 向字典中添加一个推导
		except: # 打开文件失败就抛出异常，待GUI处理
			raise IOError
			
		self.__calTerAndNonTer() # 调用方法，求终结符和非终结符
		self.beginChar = self.NonTerminater[0]
		# 判断是不是左递归
		if self.__judgeLeftRecursion():
			messagebox.showinfo('提示', '该文法是左递归文法，已将其修改！')
			self.modifyLeftRecusion()  # 是左递归的话，就修改
			print('在修改左递归后，文法如下')
			for key in self.grammar.keys():
				print(key, '->', self.grammar[key])
		
		# 再求first集和follow集,再判断是否是LL1文法，再生成预测分析表
		self.__first()
		self.__follow()
		self.judgeLL1()
		self.genAnalysisTable()
		
	# 求终结符和非终结符
	def __calTerAndNonTer(self):
		for key in self.grammar.keys():
			# 每个推导式的左边就是非终结符
			if key not in self.NonTerminater:
				self.NonTerminater.append(key)
			# 终结符
			for value in self.grammar[key]:
				# 先判断是否为空字，是则加入终结符集
				if value == '':
					if value not in self.Terminater:
						self.Terminater.append(value)
				# 如果每个可能推导的第一个字符是除大写字母以外的字符，就放到终结符集合里
				elif not value[0].isupper():
					if value[0] not in self.Terminater:
						self.Terminater.append(value[0])
		
		print('非终结符集合：', self.NonTerminater)
		print('终结符集合:', self.Terminater)
		
	# 求一个文法的所有first集,定义成私有方法，只在创建对象时由初始化函数调用
	def __first(self):
		for nT in self.NonTerminater: #先赋值一个空列表
			self.First[nT] = []
		# 后面要用到递归，所以分开两个循环
		for T in self.Terminater: # 终结符的first集就是他自己
			self.First[T] = [T]
		for nT in self.NonTerminater:
			self.__subFirst(nT)
		
	# 求first集的递归子方法
	def __subFirst(self, X):
		tmpSize = len(self.First[X]) # 求之前的大小
		if X in self.Terminater and X not in self.First[X]: #如果X在终结符里， 则X属于first(X)
			self.First[X].append(X)
		else : # else X就不是终结符，对X的每个推导，依次判断推导的字符是什么
			for derivation in self.grammar[X]:
				# 先判断是不是空字，是空字就加入
				if derivation == '':
					if '' not in self.First[X]:
						self.First[X].append('')
				# 再判断每个推导的第一个字符是不是终结符，是则加入
				elif derivation[0] in self.Terminater:
					if derivation[0] not in self.First[X]:
						self.First[X].append(derivation[0])
				else:
					# else，就全是非终结符，
					# 再遍历他们，递归的求每个字符的first集
					for subDe in derivation:
						self.__subFirst(subDe)
			# 对每个推导都处理完后，把每个推导的first集放到first（x）中
			for derivation in self.grammar[X]:
				if derivation == '' or derivation[0] in self.Terminater:
					continue
				# 找每个推导串中第一个不能推导出空字的非终结符
				location = -1
				for i in range(len(derivation)):
					if '' not in self.grammar[derivation[i]]:
						location = i
						break
				if location == -1: # 如果都能推出空字,
					# 就把所有推导式子字符的first集加入first(X)
					for subDe in derivation:
						for ele in self.First[subDe]:
							if ele not in self.First[X]:
								self.First[X].append(ele)
				else : # 否则从第一个不能推导出空字的非终结符开始
					for i in range(location + 1):
						# print('将', derivation[i], '的first集加入', X, '的')
						for ele in self.First[derivation[i]]:
							if ele != '' and ele not in self.First[X]:
								self.First[X].append(ele)
					
		if len(self.First[X]) == tmpSize:  # 长度不变就返回
			return
			
	# 求一个文法的一个非终结符的follow集，定义成私有方法，只在创建对象时由初始化函数调用
	def __follow(self):
		for nT in self.NonTerminater:
			self.Follow[nT] = []  # 同样赋值一个空列表
		self.Follow[self.NonTerminater[0]].append('#') # 将’#‘加入开始符号的follow集中
		for nT in self.NonTerminater:
			self.__subFollow(nT)
			
	# 求follow集的递归子程序
	def __subFollow(self, X):
		for key in self.grammar.keys(): # 遍历每个推导式子
			for derivation in self.grammar[key]: # 对每个推导式，遍历子字符
				lenOfDe = len(derivation)
				for i in range(lenOfDe):
					if X == derivation[i]: # 在产生式中找到要求的
						if i == lenOfDe - 1: # 如果他在推导式的最后一个字符
							for f in self.Follow[key]:
								if f not in self.Follow[X] and f is not '':
									self.Follow[X].append(f)
						# 否则如果他后面跟的不是非终结符，就把这个符号放到follow(X)里
						elif derivation[i + 1] not in self.NonTerminater:
							# print(X, '后面是', derivation[i + 1])
							if derivation[i + 1] not in self.Follow[X]:
								self.Follow[X].append(derivation[i + 1])
						# 如果后面跟了一个非终结符Y
						elif derivation[i + 1] in self.NonTerminater:
							# 就把first(Y)给它
							for f in self.First[derivation[i + 1]]:
								if f not in self.Follow[X] and f is not '':
									self.Follow[X].append(f)
							# 再额外判断空字是否属于first(Y)
							if '' in self.First[derivation[i + 1]]:
								for f in self.Follow[key]:
									if f not in self.Follow[X] and f is not '':
										self.Follow[X].append(f)
	
	# 判断一个文法是否左递归
	def __judgeLeftRecursion(self):
		# 包括直接左递归和间接左递归
		# 先判断直接左递归
		isRecursion = self.__subRecursion(self.grammar)
		if isRecursion:
			print('该文法是直接左递归')
		# 再判断间接左递归，修改文法，从后往前，依次将后面的非终结符的推导替换到前面相应位置
		if isRecursion is False: # 不是直接左递归，判断是否是间接
			tmpLL1Grammar = self.modify() # 是的话就执行替换
			isRecursion = self.__subRecursion(tmpLL1Grammar)# 再判断修改后的文法是否含直接左递归
			if isRecursion:
				print('该文法是间接左递归')
				self.grammar = tmpLL1Grammar
		return isRecursion
		
	# 修改文法，将后面的非终结符的推导放到前面出现的位置上，可能得到直接左递归
	def modify(self):
		tmpLL1Grammar = self.grammar.copy()
		tmp2 = self.grammar.copy()
		# 从后往前，依次把后面的所有候选替换到前面出现的位置处
		keys = list(tmpLL1Grammar.keys())  # 把键转换为列表类型
		keys.reverse()  # 将键倒序，方便后面代码编写
		keylen = len(keys)
		for i in range(1, keylen):
			tmpDe = tmpLL1Grammar[keys[i]].copy()
			toBeMoved = []
			for de in tmp2[keys[i]]:
				# 如果是空字或者首字是终结符，则这个key推出的产生式就没有左递归
				if de == '' or de[0] in self.Terminater:
					continue
				else:
					deLen = len(de)
					for j in range(deLen):
						if de[j] in self.Terminater:
							continue
						elif de[j] in self.NonTerminater and i > keys.index(de[j]):
							# print('碰到非终结符，把', de[j], '的推导加入')
							for x in tmpLL1Grammar[de[j]]:
								t = x + de[j + 1:]
								if t not in tmpDe:
									tmpDe.append(t)
							toBeMoved.append(de)  # 这个含非终结符的推导要删掉，所以先暂时存放着
			
			for moved in toBeMoved:
				if moved in tmpDe:
					tmpDe.remove(moved)
			
			tmpLL1Grammar[keys[i]] = tmpDe
		return tmpLL1Grammar
		
	# # 判断左递归的子程序，判断是否是直接左递归
	def __subRecursion(self, grammar):
		isRecursion = False
		for key in grammar.keys():
			for derivation in grammar[key]:
				if derivation == '': # 推出空字，就继续判断后面的推导
					continue
				elif derivation[0] == key:
					isRecursion = True
					break
			if isRecursion is True:
				break
		
		return isRecursion
	
	# 判断一个文法是否是LL（1）文法
	def judgeLL1(self):
		# 初始化文法时已经判断了是否左递归，
		# 因此只用判断剩下两个规则，对每个非终结符，调用firstA，求它的每个产生式的first集
		# 调用修改文法，再进行判断
		tmpLL1Grammar = self.grammar.copy()
		isLL1 = True
		for key in tmpLL1Grammar.keys():
			isLL1 = True
			derivation = tmpLL1Grammar[key]
			alpha = []
			for de in derivation:
				if de == '':
					alpha.append('')
				else:
					alpha.append(de[0])
			alphaLen = len(alpha)
			for i in range(alphaLen - 1):
				for j in range(i + 1, alphaLen):
					if self.First[alpha[i]] == self.First[alpha[j]]:
						isLL1 = False
					break
				if not isLL1:
					break
		
		if not isLL1:
			messagebox.showinfo('错误！', '该文法不是LL（1）文法，无法执行分析！')
			return
		#再看每个文法的所有候选首符集，
		for key in self.grammar.keys():
			derivation = self.grammar[key]
			if '' in derivation: #如果有空字
				if self.__intersection(key): # 如果非终结符key的first集和follow集的交集不为空
					isLL1 = True
					break
		
		if isLL1 is False:
			messagebox.showinfo('错误！', '该文法不是LL（1）文法，无法执行分析！')
		else:
			print('该文法是LL(1)文法')
	
	# 求非终结符A的first集和follow集的交集
	def __intersection(self, A):
		res = [x for x in self.First[A] if x in self.Follow[A]]
		return res
	
	# 消除直接左递归的算法
	def modifyLeftRecusion(self):
		# 先创建一个候选字母表
		toBeChoosed = [chr(ord('A') + x) for x in range(26)]
		toBeChoosed = [x for x in toBeChoosed if x not in self.grammar.keys()]# 去掉已经有的字母
		tmpLL1Grammar = self.grammar.copy()
		for key in tmpLL1Grammar.keys():
			derivation = tmpLL1Grammar[key]
			tmpDe = tmpLL1Grammar[key].copy()
			isModify = False
			toBeMoved = []
			stay = []
			newNT = ''
			for de in derivation:
				if de == '':
					continue
				if de[0] == key: #找到直接左递归的推导
					toBeMoved.append(de)
					stay.append(de[1:])
					newNT = random.choice(toBeChoosed)
					isModify = True
			if isModify: # 根据标志判断是否进行修改
				for move in toBeMoved: # 把非终结符开头的推导删掉
					tmpDe.remove(move)
				for i in range(len(tmpDe)): # 其余推导在末尾加上新的非终结符号
					tmpDe[i] += newNT
				self.NonTerminater.append(newNT)
				newDe = [s + newNT for s in stay] # 原来那个要被替换掉的产生式的非终结符
				newDe.append('') # 加入空字
				self.grammar[key] = tmpDe
				self.grammar[newNT] = newDe
		# 修改完后，把不会出现的推导去掉
		occurTimes = {} # 创建一个空字典，存放每个非终结符的出现次数
		for value in self.grammar.values():
			for t in value:
				for subT in t:
					if subT == '':
						continue
					elif subT in self.NonTerminater:
							occurTimes[subT] = occurTimes.get(subT, 0) + 1
		popKeys = [key for key in self.grammar.keys() if key not in occurTimes.keys()]
		for k in popKeys:
			self.grammar.pop(k)
			self.NonTerminater.remove(k)
		
		self.__calTerAndNonTer() #更新终结符和非终结符,first集和follow集
		self.__first()
		self.__follow()
		
	# 求预测分析表
	def genAnalysisTable(self):
		# 用一个二维字典来表示分析表，这样索引的时候好查
		self.PredictTable = {}
		# 先定义一个分析表终结符
		self.tableTerminater = self.Terminater.copy()
		for first in self.First.values():
			for f in first:
				if f not in self.tableTerminater:
					self.tableTerminater.append(f)
		
		for follow in self.Follow.values():
			for f in follow:
				if f not in self.tableTerminater:
					self.tableTerminater.append(f)
		if '' in self.tableTerminater:   # 把空字去掉，因为空字不能出现在follow集中
			self.tableTerminater.remove('')
			
		# print('预测分析表如下:')
		for nT in self.NonTerminater:
			self.PredictTable[nT] = {}
			for T in self.tableTerminater:
				derivation = self.grammar[nT]
				if T in derivation: # 先判断是不是能直接推导
					self.PredictTable[nT][T] = nT + '->' + T
				elif T in self.First[nT]: # 否则再判是不是在first集中
					find = False
					for de in derivation:
						if T in de:
							self.PredictTable[nT][T] = nT + '->' + de
							find = True
							break
					if not find:
						for de in derivation:
							for subDe in de:
								if T in self.First[subDe]:
									self.PredictTable[nT][T] = nT + '->' + de
									find = True
									break
							if find:
								break
				elif T in self.Follow[nT]:  # 如果出现在follow集中，再看空子是不是他的推导式其中之一
					if '' in derivation:
						for fo in self.Follow[nT]:
							self.PredictTable[nT][fo] = nT + '->ε'
					else:
						self.PredictTable[nT][T] = ''
				else:
					self.PredictTable[nT][T] = ''
		
	#提取公共左因子，思想是对每个推导的首字符进行计数，对那些出现次数多于1的进行操作
	def extractCommonLeftFactor(self):
		tmpLL1Grammar = self.grammar.copy()
		for key in tmpLL1Grammar.keys(): #计数产生式的每个候选的第一个字符出现次数
			occurTimes = {}  # 一个字典存放每个推导式子的第一个字符出现次数
			derivation = tmpLL1Grammar[key]
			for de in derivation:
				if de == '': # 如果是空字，就跳过
					continue
				occurTimes[de[0]] = occurTimes.get(de[0], 0) + 1

			occurOver1time = []  # 先记录所有出现次数超过1的字符
			for k in occurTimes.keys():
				if occurTimes[k] > 1:
					occurOver1time.append(k)
			
			toBeOperated = [] # 一个推导中可能有多个出现多次的符号，先记录下来，再统一操作它们
			for de in derivation:
				if de == '': # 跳过空字
					continue
				elif de[0] in occurOver1time and de[0] not in toBeOperated: # 没有and后面的条件，就会重复添加
					toBeOperated.append(de[0])
			if len(toBeOperated) > 0: # 如果待操作的字符数至少有1个才操作
				self.__subExtract(key, toBeOperated)
	
	# 提取左公因子的子程序，执行相当于对一个产生式进行操作
	def __subExtract(self, key, toBeOperated):
		toBeChoosed = [chr(ord('A') + x) for x in range(26)]
		toBeChoosed = [x for x in toBeChoosed if x not in self.grammar.keys()]  # 去掉已经有的字母
		for op in toBeOperated:  # 遍历每个要被操作的符号，
			toBeRemoved = []      # 原推导中要被移除的推导式
			derivation = self.grammar[key].copy()
			tmp = []
			newNT = random.choice(toBeChoosed) #选择一个新非终结符
			toBeChoosed.remove(newNT) # 在列表中去掉已选的新非终结符，避免有几个op时可能会选中同一个非终结符
			for de in derivation:
				if de == '':
					continue
				if de[0] == op and len(de) > 1:         # 将要丢掉的推导暂存，并用于新产生式
					toBeRemoved.append(de)
			
			for move in toBeRemoved:   #把要丢掉的候选式去掉第一个字符后放到tmp列表
				tmp.append(move[1:])
				self.grammar[key].remove(move)
			
			self.grammar[key].append(op + newNT)  # 新的候选式
			self.grammar[newNT] = tmp # 把新的产生式放到文法字典