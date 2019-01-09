#testing how passing an undeterminate number of arguments to a class constructor works

class test():
    def __init__(self,dictionary):
    	for (k,v) in dictionary.items():
    		setattr(self,k,v)


l = {"spook":10,"gook":30}

t = test(l)

print(t.spook,t.gook)

class test2():

	def __init__(self):
		self.dick = True
		self.puss = False
		for x in range(3):
			setattr(self,"quadrant_{}".format(x),["spoof"])


	def printOwnAttributes(self):
		print(dir(self))


ta = test2()

for x in {key:value for key,value in ta.__dict__.items() if "quadrant_" in str(key)}:
	#print(x)
	#print(ta.__dict__[str(x)])
	ta.__dict__[str(x)].append("baby")
	print(x,ta.__dict__[str(x)])


"""

#testing how to determine an as symmetrical as possible grid size, given a random number.

import random

grid_size = random.randint(3,30)
print(grid_size)

for num in range(int(grid_size/2),0,-1):
	if num * num <= grid_size:
		print("Number '{n}' fits the bill\n\
			It produces a grid of {n}*{n}={multi}\n\
			The leftover is: {left}".format(n=num, multi=num*num,left=grid_size - (num*num)))

"""