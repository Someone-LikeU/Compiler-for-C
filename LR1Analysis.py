# encoding=utf-8
'''
@author:   pip install zjj =_=
@software: Pycharm
@time:     2019/10/19 21:21
@filename: LR1Analysis.py
@contact:  1326632773@qq.com
'''
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as messagebox
from tkinter import *

class Stack:
	
	def __init__(self):
		self.__length = 0  # 记录栈内元素数量
		self.__data = []  # 用一个列表来表示栈
	
	# 进栈
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
			res += str(value)
		return res
	
	# 查看栈顶元素
	def top(self):
		self.__length = len(self.__data)
		if self.__length == 0:
			messagebox.showinfo("警告", "栈已空!")
		else:
			return self.__data[self.__length - 1]
# 文法类
class LR1Grammar:
	
	def __init__(self, filename):
		self.grammar = [] # 用列表放文法，每个推导以一个元组表示
		self.grammar2 = {}
		self.Terminater = []
		self.NonTerminater = []
		self.Terminater = []
		self.First = {}
		self.projectSetFamily = [] # 项目集族，用列表存，一个项目集是一个列表
		self.actionTable = {} # action表
		self.GOTOtable = {} # goto表
		# 一个元组，（T， n， p） T表示一个产生式编号，n表示右边圆点的位置，p表示展望符，是一个列表
		try:
			f = open(filename, 'r')
			for line in f:
				nT = line[0] # 一个推导的非终结符
				derivation = line[3:].replace('\n', '')  # 右边的产生式
				self.grammar.append((nT, derivation.replace('蔚', 'ε')))
			f.close()
			print('第一种文法表示法：', self.grammar)
		except: # 打开文件失败就抛出异常，待GUI处理
			raise IOError('文件打开失败!')
		 
		self.__CalnTandT()  # 求终结符和非终结符
		for nT in self.NonTerminater:
			self.grammar2[nT] = []
		for item in self.grammar:
			self.grammar2[item[0]].append(item[1])
		print('第二种文法表示法:')
		for key in self.grammar2.keys():
			print(key, '->', self.grammar2[key])
		print('非终结符集合：', self.NonTerminater)
		print('终结符集合:', self.Terminater)
		self.allFirst()
		self.calProjectSetFamily()
		self.calActionAndGOTOTable()
	
	# 计算终结符和非终结符
	def __CalnTandT(self):
		for item in self.grammar:
			if item[0] not in self.NonTerminater:
				self.NonTerminater.append(item[0])
		for item in self.grammar:
			for subDe in item[1]:
				if subDe not in self.NonTerminater \
						and subDe not in self.Terminater:
					self.Terminater.append(subDe)
	
	# 求first集
	def allFirst(self):
		for T in self.Terminater: # 终结符的first集就是他自己
			self.First[T] = [T]
		for nT in self.NonTerminater:# 先循环给非终结符的first集一个空列表
			self.First[nT] = []
		if 'ε' in self.First.keys(): # 空字不是终结符，得去掉
			self.First.pop('ε')
		for nT in self.NonTerminater:
			derivation = self.grammar2[nT]
			if 'ε' in derivation:   # 空字在推导中，就把空字也加入它的first集中
				self.First[nT].append('ε')
		for item in self.grammar:
			derivation = item[1]
			if derivation == 'ε':
				continue
			if derivation[0] in self.Terminater:
				self.First[item[0]].append(derivation[0])
		# 再倒着来，从最后一个文法开始往前推
		for i in range(len(self.grammar) - 1, -1, -1):
			if self.grammar[i][1] == 'ε':
				continue
			de = self.grammar[i][1]
			allHaveNone = True
			for subDe in de:
				if subDe in self.NonTerminater: # 如果一个产生式右边第一个字符是非终结符
					for f in self.First[subDe]:# 就把这个非终结符的first集给推出它的非终结符
						if f not in self.First[self.grammar[i][0]]:
							self.First[self.grammar[i][0]].append(f)
					if 'ε' not in self.First[subDe]:
						allHaveNone = False
						break
				elif subDe in self.Terminater: # 产生式中有一个终结符，就退出for
					break
			# for正常执行完，说明一个产生式右边全是非终结符
			else:
				if allHaveNone: # 再看这个全部是非终结符的标记是否为真
					self.First[self.grammar[i][0]].append('ε')
	
	# 求一个符号串X的first集
	def first(self, X):
		if self.First == {}:
			print('请先调用allFirst方法求出所有first集!')
			return
		# 符号串，所以默认没有空字，就不用考虑空字
		res = []
		for subX in X:
			if subX in self.NonTerminater: #如果字符是非终结符
				res += self.First[subX]
				if 'ε' not in self.First[subX]: # 如果这个非终结符的first集没有空字，就退出
					break   # 有空字，就能继续往后看
			elif subX in self.Terminater and subX not in res: # 终结符就加入结果列表并退出循环
				res.append(subX)
				break
		return res
	
	# 求文法的项目集族
	def calProjectSetFamily(self):
		# 元组（T，n，p）
		T = 0 # 第一个产生式标号为0
		n = 1 # 第一个项目右边圆点位置是第一个
		p = '#' # 第一个项目的展望符肯定是#
		I0 = self.__closure([(T, n, p)])  # 先求第一个项目的闭包
		self.projectSetFamily.append(I0) # 加入项目集族
		allChar = self.NonTerminater + self.Terminater # 文法的所有符号
		allChar.remove(self.NonTerminater[0]) #去掉拓广文法的最开始符
		for projectset in self.projectSetFamily: # 对每个项目集和每个文法，求
			for char in allChar:
				J = self.__J(projectset, char)
				if not J:
					continue
				tmp = self.__closure(J)
				if tmp not in self.projectSetFamily:
					self.projectSetFamily.append(tmp)
		# 输出所有项目集
		for i in range(len(self.projectSetFamily)):
			print('项目集', i, ':')
			for item in self.projectSetFamily[i]:
				print(item)
		
	# 求一个项目的闭包
	def __closure(self, project):
		# project是一个项目，是一个三个元素的元组
		res = project
		for item in project:
			T = item[0] # 产生式编号
			n = item[1] # 右边圆点位置，用来索引圆点右边那个符号
			p = item[2] # 当前项目item的展望符
			sizeOfProduct = len(self.grammar[T][1])
			if n == sizeOfProduct + 1:  # 如果圆点的位置在产生式的最后，那么就跳过当前这个产生式，看下一个
				continue
			X = self.grammar[T][1][n - 1] # 索引圆点右边那个符号
			if X in self.NonTerminater: # 如果X是非终结符
				# 先求这个X后面的符号连接上展望符的first集
				if n == sizeOfProduct:
					first = p
				else:
					# 再求展望符
					first = self.first(self.grammar[T][1][n] + p)
					
				prods = []    # 求X作为产生式左边的推导的编号
				for i in range(len(self.grammar)):
					if self.grammar[i][0] == X:
						prods.append(i)
				# 把不在原项目集中的项目加到当前项目集中
				for prod in prods:
					for f in first:
						if (prod, 1, f) not in res:
							res.append((prod, 1, f))
			# else就是终结符，就不管
		
		return res
	
	# 求一个项目集J
	def __J(self, I, X):
		res = []
		for project in I:
			T = project[0] # 项目的产生式的标号
			n = project[1] # 右边圆点位置
			p = project[2] # 项目的展望符
			product = self.grammar[T][1] # 产生式右边的字符串
			# 遍历这个推导，由于字符串的特性，因此这里用下标的方式来遍历
			for i in range(len(product)):
				if product[i] == X: # 第i个字符是X，
					if i == n - 1: # 如果它在圆点右边，就把它加入res
						res.append((T, n + 1, p))
		return res
		
	# 定义Go函数,返回一个项目集在项目集族中的标号
	def __GO(self, I, X):
		J = self.__J(self.projectSetFamily[I], X)
		closureJ = self.__closure(J)
		res = -1
		for i in range(len(self.projectSetFamily)):
			if closureJ == self.projectSetFamily[i]:
				res = i
				break
		
		return res
	
	# 求action表	和goto表,
	def calActionAndGOTOTable(self):
		statusNum = len(self.projectSetFamily) # 状态数
		Terminater = self.Terminater.copy()
		Terminater.append('#')
		# 先把所有项目集放到一个列表里
		allProject = []
		for projectSet in self.projectSetFamily:
			allProject += [x for x in projectSet if x not in allProject]
		for k in range(statusNum):   # 遍历每个项目集
			self.actionTable[k] = {}# 初始，给每个状态一个空字典，这样就能通过双重字典来实现两个字符索引
			self.GOTOtable[k] = {}
			for T in self.Terminater:
				self.actionTable[k][T] = '' # 先给表中每个元素赋值空字
			self.actionTable[k]['#'] = ''   # 把’#‘也给加上
			for NT in self.NonTerminater:
				self.GOTOtable[k][NT] = ''
		
		for project in allProject: # 遍历每个项目
			T = project[0]  # 项目的产生式的标号
			n = project[1]  # 右边圆点位置
			p = project[2]  # 项目的展望符
			sizeOfProduct = len(self.grammar[T][1])
			for k in range(statusNum):
				if project not in self.projectSetFamily[k]: # 某项目不在某项目集，continue
					continue
				# 执行到这说明该项目在某项目集中
				if (0, 2, '#') == project:  # 先判断第三个规则，符合的话直接退出当前循环
					self.actionTable[k]['#'] = 'acc'
				else:
					if n == sizeOfProduct + 1:  # 第二个规则，因为如果先判断第一个的话要用到n-1，而n-1可能会越界，所以先判第二
						self.actionTable[k][p] = 'r' + str(T)
					else:
						a = self.grammar[T][1][n - 1]  # 索引圆点右边那个符号,判断第一个规则
						if a in Terminater:
							j = self.__GO(k, a)
							self.actionTable[k][a] = 's' + str(j) if j != -1 else ''
						A = self.grammar[T][0]  # 第四个规则
						j = self.__GO(k, A)
						self.GOTOtable[k][A] = j if j != -1 else ''
						
class LR1GUI:
	
	# 初始化，包括窗体，按钮等,要用到文法，所以给一个文法参数
	def __init__(self):
		self.window = Tk()  # 创建一个窗口
		self.window.title('LR(1)分析')  # 标题
		self.Grammar = None  # 文法对象先初始化为None，待打开文件后再初始化 todo 先在GUI上打开文件，再把传递给这个文法对象
		self.program = ""  # 待分析的程序段
		self.grammarLabels = []  # 记录展示的文法和对应的first和follow的标签
		self.anaTableWin = None  # 定义一个分析表窗口的“窗口句柄"
		self.oldSize = None
		frame = Frame(self.window)  # 这个框架放介绍文字
		frame1 = Frame(self.window)  # 这个框架放提示输入文法
		frame2 = Frame(self.window)  # 这个框架放读取文法程序
		self.frame3 = Frame(self.window)  # 这个框架放文法，first集，follow集
		frame4 = Frame(self.window)  # 这个框架放输入程序段的位置
		frame5 = Frame(self.window, width = 100, height = 40)  # 放分析结果
		self.frame6 = Frame(self.window)  # 放分析表，框架3和6是在选择文法和产生分析表后才显示，所以定义成self形式
		
		frame.pack()
		frame1.pack()
		frame2.pack()
		self.frame3.pack()
		frame4.pack()
		frame5.pack()
		self.frame6.pack()
		
		self.v1 = StringVar()  # 获取文本文件的输入框
		self.v2 = StringVar()  # 获取输入程序段的文本框
		# 添加标签，输入框，按钮等组件
		welcome = Label(frame, text = 'LR(1)文法分析器', font = ('KaiTi', 15), anchor = 'center')
		promptEnterFile = Label(frame1, text = '请输入一个文法文本名：', font = ('KaiTi', 13))
		entryGrammar = Entry(frame1, textvariable = self.v1, justify = LEFT, width = 15, font = ('KaiTi', 13))
		btConfirm = Button(frame1, text = '确定', font = ('KaiTi', 13), command = self.__getFileByEntry)
		anotherChoose = Label(frame1, text = '或点击按钮选择文件:', font = ('KaiTi', 13))
		btChoose = Button(frame1, text = '打开', command = self.__getFileByInteract, font = ('KaiTi', 13))
		promptLable = Label(frame2, text = '请输入一个程序段:', font = ('KaiTi', 13))
		entryProgram = Entry(frame2, textvariable = self.v2, justify = LEFT, width = 30, font = ('KaiTi', 13))
		analysisButton = Button(frame2, text = '执行分析', command = self.analysis, font = ('KaiTi', 13))
		exitButton = Button(frame2, text = '退出', command = self.exitPro, font = ('KaiTi', 13))
		welcome.grid()
		promptEnterFile.grid(row = 1, column = 1)
		entryGrammar.grid(row = 1, column = 2)
		btConfirm.grid(row = 1, column = 3)
		anotherChoose.grid(row = 1, column = 4)
		btChoose.grid(row = 1, column = 5)
		promptLable.grid(row = 2, column = 1)
		entryProgram.grid(row = 2, column = 2)
		analysisButton.grid(row = 2, column = 3)
		exitButton.grid(row = 2, column = 4)
		# 放frame4里的东西
		words = ['步骤', '状态栈', '符号栈', '输入串', '动作说明']
		widths = [8, 15, 15, 15, 24]
		for i in range(len(words)):
			Label(frame4, text = words[i], font = ('KaiTi', 14), borderwidth = 2, relief = 'ridge',
			      width = widths[i], background = 'grey').grid(row = 1, column = i + 1)
		
		# 设置一个滑动条, 再添加到text控件中
		scrollBar = Scrollbar(frame5)
		scrollBar.pack(side = RIGHT, fill = Y)
		self.text = Text(frame5, width = 120, height = 20, wrap = WORD,
		                 yscrollcommand = scrollBar.set)  # 创建一个文本框组件
		self.text.pack()
		scrollBar.config(command = self.text.yview)  # 滚动条和text绑定
		self.window.mainloop()  # 事件循环
	
	# 交互式选择文法文件
	def __getFileByInteract(self):
		fileName = askopenfilename()
		self.Grammar = LR1Grammar(fileName)  # 初始化文法对象
		self.__showGrammar()  # 然后展示文法
		self.text.delete('1.0', END)  # 删掉之前的分析结果
		self.oldSize = len(self.Grammar.grammar)
	
	# 在GUI上展示文法和文法的first集
	def __showGrammar(self):
		if self.grammarLabels:  # 每次展示前先把前面一个文法的所有标签删掉
			for label in self.grammarLabels:
				label.destroy()
		self.grammarLabels = []
		r = 1
		col = 1
		l = Label(self.frame3, text = '所选文法如下：', font = ('KaiTi', 14))
		l.grid(row = r, column = col)
		self.grammarLabels.append(l)
		col += 1
		l = Label(self.frame3, text = 'FIRST集：', font = ('KaiTi', 14))
		l.grid(row = r, column = col)
		self.grammarLabels.append(l)
		r = 2
		col = 1
		for key in self.Grammar.grammar2.keys():
			string = key + '->'  # 先展示文法
			tmp = self.Grammar.grammar2[key]
			string += '|'.join(tmp)
			l = Label(self.frame3, text = string, font = ('KaiTi', 12), width = 20, justify = LEFT)
			l.grid(row = r, column = col)
			r += 1
			self.grammarLabels.append(l)
		r = 2
		col = 2
		for key in self.Grammar.grammar2.keys():
			string = 'FIRST(' + key + '):{'  # 再展示first
			tmp = self.Grammar.First[key]
			string += ','.join(tmp) + '}'
			l = Label(self.frame3, text = string, font = ('KaiTi', 12), width = 25, justify = LEFT)
			l.grid(row = r, column = col)
			self.grammarLabels.append(l)
			r += 1
	
	# 输入文法名字，打开文法文件
	def __getFileByEntry(self):
		pass
		fileName = self.v1.get()
		if fileName != "":  # 确保有输入
			try:
				self.Grammar = LR1Grammar(fileName)
				self.__showGrammar()
				self.text.delete('1.0', END)  # 删掉之前的分析结果
				self.oldSize = len(self.Grammar.grammar)
			except IOError:
				self.Grammar = None  # 重新赋值文法对象为None
				messagebox.showinfo("错误！", "文件 " + fileName + " 不存在！")
		else:
			messagebox.showinfo("警告！", "未输入文法文件名，请输入！")
	
	# 获取输入程序段
	def __getProgram(self):
		tmpStr = self.v2.get()
		if tmpStr == '':  # 如果没有输入，就提示错误
			messagebox.showinfo("错误", "请输入程序段！")
		else:  # 有输入,将该字符串返回
			return tmpStr
	
	# 展示LR1分析表
	def showLR1analysisTable(self):
		self.anaTableWin = Tk()
		self.anaTableWin.title('LR（1）分析表')
		tableTerminater = self.Grammar.Terminater.copy()
		tableTerminater.append('#')
		tableNonTer = self.Grammar.NonTerminater.copy()
		tableNonTer.remove(self.Grammar.NonTerminater[0])
		frame = Frame(self.anaTableWin)
		frame2 = Frame(self.anaTableWin)
		frame3 = Frame(self.anaTableWin)
		frame.pack()
		frame2.pack()
		frame3.pack()
		statusLabel = Label(frame, text = '状态', width = 5, height = 2, font = ('KaiTi', 13), anchor = 'center',
		                    borderwidth = 2, relief = 'ridge')
		statusLabel.grid(row = 1, column = 1)
		actionLabel = Label(frame, text = 'ACTOIN（动作）', width = 5 * len(tableTerminater) - 3, height = 2,
		                    font = ('KaiTi', 13), anchor = 'center',borderwidth = 2, relief = 'ridge',)
		actionLabel.grid(row = 1, column = 2)
		gotoLabel = Label(frame, text = 'GOTO（转换）', width = 5 * len(tableNonTer), height = 2, borderwidth = 2, relief = 'ridge',
		                    font = ('KaiTi', 13), anchor = 'center')
		gotoLabel.grid(row = 1, column = 3)
		Label(frame2, text = '  ', width = 5, height = 2).grid(row = 1, column = 1)
		col = 2
		for t in tableTerminater:
			Label(frame2, text = t, width = 4, height = 2, font = ('KaiTi', 13),borderwidth = 2, relief = 'ridge',
			      anchor = 'center').grid(row = 1, column = col)
			col += 1
		for nT in tableNonTer:
			Label(frame2, text = nT, width = 4, height = 2, font = ('KaiTi', 13),borderwidth = 2, relief = 'ridge',
			      anchor = 'center').grid(row = 1, column = col)
			col += 1
		row = 1
		for i in range(len(self.Grammar.projectSetFamily)):
			col = 1
			Label(frame3, text = i, width = 4, height = 1, borderwidth = 2, relief = 'ridge',
			      font = ('KaiTi', 13)).grid(row = row, column = col)
			col += 1
			for T in tableTerminater:
				Label(frame3, text = self.Grammar.actionTable[i][T], width = 4, height = 1, borderwidth = 2,
				      relief = 'ridge', font = ('KaiTi', 13)).grid(row = row, column = col)
				col += 1
			for nT in tableNonTer:
				Label(frame3, text = self.Grammar.GOTOtable[i][nT], width = 4, height = 1, borderwidth = 2,
				      relief = 'ridge',font = ('KaiTi', 13)).grid(row = row, column = col)
				col += 1
			row += 1

	# 执行分析,有错提示错误信息
	def analysis(self):
		self.showLR1analysisTable() # 先展示LR1分析表
		# 然后是分析的主控程序
		if self.Grammar is None:
			messagebox.showinfo("错误!", "未读取文法！请先选择一个文法！")
			return
		self.text.delete('1.0', END)  # 删掉前面一个分析过程
		step = 0  # 分析步数
		statusStack = Stack()# 状态栈
		charStack = Stack() # 符号栈
		index = 0  # 输入程序段的下标
		statusStack.push(0) # 一开始先把0状态入栈
		charStack.push('#')# ’#‘入栈
		self.program = self.__getProgram() # 获取待分析程序段
		while self.program == '':
			self.program = self.__getProgram()
		if self.program[-1] != '#': # 如果输入最后不是#，就给它加上个#,防止用户忘记
			self.program += '#'
		
		template = "{0:^14}{1:<16}{2:<15}{3:<19}{4:<20}\n"  # 设置展示的格式模板
		self.text.tag_config('tag', font = ('KaiTi', 13))
		actionTable = self.Grammar.actionTable
		GOTOtable = self.Grammar.GOTOtable
		success = True
		while True:
			a = self.program[index]
			i = statusStack.top()
			action = actionTable[i][a]
			charStContent = charStack.toString()
			statusStContent = statusStack.toString()
			remain = self.program[index:]
			print('第{}步，a = {}, i = {}'.format(step, a, i), end = '')
			print('action = ', action)
			if action == 'acc':  # 接受
				print('接受，index = ', index)
				self.text.insert(END, template.format(step, statusStContent,
				                 charStContent, remain, '接受，分析成功'), 'tag')
				break
			elif action[0] == 's':  # 移进
				j = eval(action[1])  # 要移进的状态
				mess = 'action(' + str(i) + ',' + a + ')=' + action
				mess += ',状态' + str(j) + '入栈'
				self.text.insert(END, template .format(step, statusStContent,
				                                      charStContent, remain, mess), 'tag')
				statusStack.push(j)
				charStack.push(a)
				index += 1 # 输入串指针后移，
				step += 1
			elif action[0] == 'r': # 规约
				# 先从状态栈弹出n个状态，n为规约产生式的长度
				prodNum = eval(action[1])
				prod = self.Grammar.grammar[prodNum][1]
				prodLen = len(prod)
				for _ in range(prodLen): # 把n个字符从状态栈和符号栈弹出
					statusStack.pop()
					charStack.pop()
				# 将用到的规约式的非终结符入栈
				A = self.Grammar.grammar[prodNum][0]
				charStack.push(A)
				i = statusStack.top()
				go = GOTOtable[i][A]
				statusStack.push(go) # 新状态入栈
				mess = action + ':' + self.Grammar.grammar[prodNum][0]
				mess += '->' + prod + ',规约,GOTO({},{})={}'.format(i, A, go)
				self.text.insert(END, template.format(step, statusStContent,
				                                      charStContent, remain, mess), 'tag')
				step += 1
			else:
				messagebox.showinfo('错误！', '输入程序段非法！')
				success = False
				break
		if success:
			messagebox.showinfo('提示', '分析成功!')
	
	def exitPro(self):
		exit(0)