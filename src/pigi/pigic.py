import math, time, random, gc, numpy_minmax

import numpy as np
from numba import prange
import ctypes

#@profile
def sort(list1):
	contains_float=False
	if isinstance(list1,np.ndarray)!=True:
		list1=np.array(list1,dtype=np.int64)
	#-- find min max
	llen = len(list1)
	mini,maxi = numpy_minmax.minmax(list1)
	typy = np.int64
	if maxi < 2**31:
		typy = np.int32
		list1=list1.astype(typy)
	
	#-- better outlier method ~O(1) time
	slist = [np.random.choice(list1) for x in range(7)]
	solist= [slist[0]]
	lso = len(solist)
	for x in range(1,7):
		s = slist[x]
		spot = 0
		while spot < lso and s > solist[spot]:
			spot += 1
		solist.insert(spot, s)
	del slist
	midavg = int((solist[2]+solist[3]+solist[4])//3)
	davg = int(((solist[0]+solist[1]+mini)/3 + midavg)//2)
	uavg = int(((solist[5]+solist[6]+maxi)/3 + midavg)//2)
	del solist

	#--- split outliers into buckets
	
	gc.disable()
	key = list1 <= davg
	outliers0,arr = list1[key]-mini,list1[~key]
	key = arr <= uavg
	outliers1,outliers2 = arr[key]-davg,arr[~key]-uavg
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
		
	gc.enable()		
	list1=np.empty((1,),dtype=typy)

	#-- create partioned buckets
	buckets = []
	maxis = [dmaxi,midmaxi,maxi]
	minis = [mini,davg,uavg]
	gc.disable()	
	
	bt = [ np.empty((maxis[0]+1,),dtype=typy), np.empty((maxis[1]+1,),dtype=typy), np.empty((maxis[2]+1,),dtype=typy) ]
	for y in prange(3):
		bt[y] = np.bincount(outliers[y])
	del outliers
	
	lbz=np.array([np.sum(bt[0],dtype=typy),np.sum(bt[1],dtype=typy),np.sum(bt[2],dtype=typy)])
	lb3=lbz[0]+lbz[1]
	lbs = [0, lbz[0], lb3]
	lbe = [lbz[0], lb3, lb3+lbz[2]]
	del lbz
	list1=np.empty((llen,),dtype=typy)
	for y in prange(3):
		miy = minis[y]
		arr = np.array(bt[y])
		arr = np.repeat(np.arange(np.size(bt[y]))+miy,arr)
		list1[lbs[y]:lbe[y]] = arr
	del bt
	del arr
	gc.enable()

	return list1

if __name__ == "__main__":
	#from memory_profiler import profile, memory_usage

	num = int(input("p17 size: "))
	t0 = time.perf_counter_ns()
	#list1 = [random.randint(0,num) for x in range(0,num)]
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

	
	sort(list1)


	'''
	from line_profiler import LineProfiler

	lp = LineProfiler()
	lp_wrapper = lp(sort)
	lp_wrapper(list1)
	lp.print_stats()
	#'''
	t10 = time.perf_counter_ns()
	ta = t10-t00
	print("Custom completed in: ",ta/1_000_000_000, "seconds total")

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
