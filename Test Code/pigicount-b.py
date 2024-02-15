import math, time, random, gc

import numpy as np

from memory_profiler import profile, memory_usage

num = int(input("p12 size: "))
t0 = time.perf_counter_ns()
list1 = np.random.randint(0, num, num, dtype=np.int64)
t1 = time.perf_counter_ns()
ta = t1-t0
print(ta, "ns list creation")
#print(list1)
#checklist=set(list1)                     #used for checking if the list contains original elements
print("list loaded with length")
print(len(list1))
print("sorting...")
t00 = time.perf_counter_ns()

#@profile
def sort(list1):
	
	#-- find min max
	llen = len(list1)
	t0 = time.perf_counter_ns()
	
	maxi = np.amax(list1)
	mini = np.amin(list1)
	print(f"min {mini}")
	print(f"max {maxi}")
	
	t1 = time.perf_counter_ns()
	ta = t1-t0
	print(ta, "ns min max numpy")
	
	#-- better outlier method ~O(1) time
	slist = [np.random.choice(list1) for x in range(7)]
	solist= [slist[0]]
	for x in range(1,7):
		s = slist[x]
		spot = 0
		while spot < len(solist) and s > solist[spot]:
			spot += 1
		solist.insert(spot, s)
	del slist
	midavg = int((solist[2]+solist[3]+solist[4])//3)
	davg = int(((solist[0]+solist[1]+mini)/3 + midavg)//2)
	uavg = int(((solist[5]+solist[6]+maxi)/3 + midavg)//2)
	del solist
	t0 = time.perf_counter_ns()
	#--- split outliers into buckets
	gc.disable()
	arr = list1
	key = arr <= davg
	outliers0 = arr[key]-mini
	arr = arr[~key]
	key = arr <= uavg
	outliers1 = arr[key]-davg
	outliers2 = arr[~key]-uavg
	del arr
	del key

	outliers = [ outliers0, outliers1, outliers2 ]
	del outliers0
	del outliers1
	del outliers2
	dmaxi=mini
	if len(outliers[0])!=0:
		dmaxi = np.amax(outliers[0])
		
	midmaxi=davg+1
	if len(outliers[1])!=0:
		midmaxi = np.amax(outliers[1])
		
	
	#print(outliers)
	gc.enable()		
	list1=[]
	
	t1 = time.perf_counter_ns()
	ta = t1-t0
	print(ta, "ns numpy outliers sorted")


	#-- create partioned buckets

	t0 = time.perf_counter_ns()
	buckets = []
	maxis = [dmaxi,midmaxi,maxi]
	minis = [mini,davg,uavg]
	gc.disable()
	
	for y in range(3):
		bt=np.empty((0,),dtype=np.int64)
		if len(outliers[y])!=0:
			bt = np.bincount(outliers[y], minlength=maxis[y]+1, weights=None)
		buckets.append(bt)
		del bt
	del outliers
	print("minis & maxis",minis,maxis)		

	t1 = time.perf_counter_ns()
	ta = t1-t0
	print(ta, "ns numpy buckets counted")
	t0 = time.perf_counter_ns()
	
	list1=np.empty((llen,),dtype=np.int64)
	lb0=np.sum(buckets[0],dtype=np.int64)
	lb1=np.sum(buckets[1],dtype=np.int64)
	lb2=np.sum(buckets[2],dtype=np.int64)
	lb3=lb0+lb1
	lbs = [0, lb0, lb3]
	lbe = [lb0, lb3, lb3+lb2]
	for y in range(3):
		miy = minis[y]
		keys = np.arange(len(buckets[y]))
		keys = keys+miy
		arr = np.array(buckets[y])
		arr = np.repeat(keys,arr)
		list1[lbs[y]:lbe[y]] = arr
		#list1.extend(arr)
	del buckets
	del arr
	del keys
	gc.enable()

	print(list1[-1])
	#print(list1)
	#print(f"-All elements?----------{set(list1)==checklist}")   #check if the list contains original elements
	#1print(f"-Is it sorted?----------{all(list1[i] <= list1[i + 1] for i in range(len(list1)-1))}")   #checking if its sorted
	t1 = time.perf_counter_ns()
	ta = t1-t0
	print(ta, "ns reasembled")

	t0 = time.perf_counter_ns()
	list1=np.array([0]) #this is just to clean up RAM from lists for benchmarking
	#buckets=np.array([0])
	#outliers
	t1 = time.perf_counter_ns()
	ta = t1-t0
	print(ta, "ns lists cleared")
	return list1

sort(list1)



t10 = time.perf_counter_ns()
ta = t10-t00
print("Custom completed in: ",ta/1_000_000_000, "seconds total")
'''
from line_profiler import LineProfiler

lp = LineProfiler()
lp_wrapper = lp(sort)
lp_wrapper(list1)
lp.print_stats()
#'''

#-- sorted() below --#

'''
#sorted()
print("now running sorted() ...")
list1 =  [random.randint(0, num) for x in range(num)]
print("running")
t0 = time.perf_counter_ns()
list1= sorted(list1)
t1 = time.perf_counter_ns()
ta = t1-t0
print("Sorted() completed in: ",ta/1_000_000_000, "ss")
input("Done, enter to end")
'''
#np.sort()
list1 = np.random.randint(0, num, num, dtype="int64")
print("now running np.sort() ...")
t0 = time.perf_counter_ns()
list1= np.sort(list1)
t1 = time.perf_counter_ns()
ta = t1-t0
print("np.sort() completed in: ",ta/1_000_000_000, "ss")
input("Done, enter to end")
#'''
