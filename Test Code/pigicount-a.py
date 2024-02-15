import math, time, random, gc

num = int(input("p9 size: "))
t0 = time.time()
list1 = [random.randint(0,num) for x in range(0,num)]
t1 = time.time()
ta = t1-t0
print(ta, "ss list creation")
#print(list1)
print("list loaded with length")
print(len(list1))
print("sorting...")
t00 = time.time()


def sort(list1):
	
	#-- find min max
	llen = len(list1)
	t0 = time.time()
	
	maxi = max(list1)
	mini = min(list1)
	print(f"min {mini}")
	print(f"max {maxi}")
	
	t1 = time.time()
	ta = t1-t0
	print(ta, "ss min max python")
		
	#-- detect outliers
	t0 = time.time()	
	midavg = (mini+maxi)//2
	
	sampler = int((len(list1)**0.5))
	tot = 0
	tot = sum(list1[:sampler])
	savg = tot//sampler
	
	uavg = int((maxi+midavg+savg*2)//2)
	davg = int((mini+midavg+savg*2)//8)
	print(midavg, uavg, davg, savg, sampler)
	
	gc.disable()
	#print(len(list1))
	
	midmaxi = davg
	dmaxi = mini
	outliers = [[],[],[]]
	
	for a in list1:
		if a < davg:
			outliers[0].append(a)
			if a > dmaxi:
				dmaxi = a
		elif a >= uavg:
			outliers[2].append(a)
		else:
			outliers[1].append(a)
			if a > midmaxi:
				midmaxi = a

	gc.enable()
	list1=[]
	
	t1 = time.time()
	ta = t1-t0
	print(ta, "ss outliers sorted")
	
	#print(outliers)
	#-- create partioned buckets
	
	t0 = time.time()
	buckets = []
	minis = [mini,davg,uavg]
	maxis = [dmaxi,midmaxi,maxi]
	gc.disable()
	for y in range(0,3):
		if outliers[y]:
			buckets.append([0]* (maxis[y]+1-minis[y]))
			for x in range(0,len(outliers[y])):
				buckets[y][outliers[y][x]-minis[y]]+=1
		else:
			print(f"bucket {y} empty")
			buckets.append([])
	print("minis & maxis",minis,maxis)		
	#print(buckets)
	t1 = time.time()
	ta = t1-t0
	print(ta, "ss buckets counted")
	gc.enable()
	
	t0 = time.time()
	gc.disable()
	for y in range(0,3):
		c=2-y
		bk = len(buckets[-1])-1
		while bk >=0:    
			if buckets[-1][bk]!=0:
				list1.extend([bk+minis[c]]*buckets[-1][bk])
				buckets[-1][bk]=0
			bk-=1
		buckets.pop()
	list1.reverse()
	gc.enable()

	print(list1[-1])
	#print(list1)
	buckets = []
	t1 = time.time()
	ta = t1-t0
	print(ta, "ss reassembled")

	t0 = time.time()
	list1=[] #this is just to clean up RAM from lists for benchmarking
	buckets=[]
	outliers=[]
	t1 = time.time()
	ta = t1-t0
	print(ta, "ss lists cleared")
	return list1

sort(list1)



t10 = time.time()
ta = t10-t00
print(ta, "ss total")
'''
from line_profiler import LineProfiler

lp = LineProfiler()
lp_wrapper = lp(sort)
lp_wrapper(list1)
lp.print_stats()
#'''

#-- sorted() below --#
print("now running sorted() ...")
list1 = [random.randint(0,num) for x in range(0,num)]
print("running")
t0 = time.time()
list1= sorted(list1)
print(list1[-1])
t1 = time.time()
ta = t1-t0
print(ta, "ss")
input("")
