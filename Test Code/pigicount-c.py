import math, time, random, gc

import numpy as np

from numba import njit
#fully in line vectorisation of p12
num = int(input("p14+njit size: "))

list1 = np.random.randint(0, num, num, dtype=np.int64)


print( "ss list creation")
#print(list1)
#checklist=set(list1)                     #used for checking if the list contains original elements
print("list loaded with length")
print(len(list1))
print("sorting...")
t00 = time.time()
gc.disable()

@njit(parallel=True, fastmath=True)
def sort(list1):
	
	#-- find min max
	llen = len(list1)
	
	
	maxi = np.amax(list1)
	mini = np.amin(list1)
	print(f"min {mini}")
	print(f"max {maxi}")
	
	
	
	print( "ss min max numpy")
	
	#-- better outlier method ~O(1) time
	slist = [np.random.choice(list1) for x in range(7)]
	solist= [slist[0]]
	for x in range(1,7):
		s = slist[x]
		spot = 0
		while spot < len(solist) and s > solist[spot]:
			spot += 1
		solist.insert(spot, s)
	slist=np.empty((1,),dtype=np.int64)
	midavg = int((solist[2]+solist[3]+solist[4])//3)
	davg = int(((solist[0]+solist[1]+mini)/3 + midavg)//2)
	uavg = int(((solist[5]+solist[6]+maxi)/3 + midavg)//2)
	solist=np.empty((1,),dtype=np.int64)
	
	#--- split outliers into buckets
	
	arr = list1
	key = arr <= davg
	outliers0 = arr[key]-mini
	arr = arr[~key]
	key = arr <= uavg
	outliers1 = arr[key]-davg
	outliers2 = arr[~key]-uavg
	
	dmaxi=mini
	if len(outliers0)!=0:
		dmaxi = np.amax(outliers0)
		
	midmaxi=davg+1
	if len(outliers1)!=0:
		midmaxi = np.amax(outliers1)
		
	
	#print(outliers)	
	list1=np.empty((1,),dtype=np.int64)
	
	
	
	print( "ss numpy outliers sorted")


	#-- create partioned buckets
	maxis = [dmaxi,midmaxi,maxi]
	minis = [mini,davg,uavg]
	
	
	#3 inhomoguenous arrays
	
	bt0=np.empty((0,),dtype=np.int64)
	if len(outliers0)!=0:
		bt0 = np.bincount(outliers0, minlength=maxis[0]+1, weights=None)
	outliers0=np.empty((1,),dtype=np.int64)
	bt1=np.empty((0,),dtype=np.int64)
	if len(outliers1)!=0:
		bt1 = np.bincount(outliers1, minlength=maxis[1]+1, weights=None)
	outliers1=np.empty((1,),dtype=np.int64)
	bt2=np.empty((0,),dtype=np.int64)
	if len(outliers2)!=0:
		bt2 = np.bincount(outliers2, minlength=maxis[2]+1, weights=None)
	outliers2=np.empty((1,),dtype=np.int64)
	
	print("minis & maxis",minis,maxis)		

	
	
	print( "ss numpy buckets counted")
	
	
	list1=np.empty((llen,),dtype=np.int64)
	lb0=np.sum(bt0,dtype=np.int64)
	lb1=np.sum(bt1,dtype=np.int64)
	lb2=np.sum(bt2,dtype=np.int64)
	lb3=lb0+lb1
	
	miy = minis[0]
	keys = np.arange(len(bt0))
	keys = keys+miy
	arr = np.repeat(keys,bt0)
	list1[0:lb0] = arr
	bt0=np.empty((1,),dtype=np.int64)
	
	miy = minis[1]
	keys = np.arange(len(bt1))
	keys = keys+miy
	arr = np.repeat(keys,bt1)
	list1[lb0:lb3] = arr
	bt1=np.empty((1,),dtype=np.int64)
	
	miy = minis[2]
	keys = np.arange(len(bt2))
	keys = keys+miy
	arr = np.repeat(keys,bt2)
	list1[lb3:lb3+lb2] = arr
	bt2=np.empty((1,),dtype=np.int64)
	
	print(list1[-1])
	#print(list1)
	#print(f"-All elements?----------{set(list1)==checklist}")   #check if the list contains original elements
	#print(f"-Is it sorted?----------{all(list1[i] <= list1[i + 1] for i in range(len(list1)-1))}")   #checking if its sorted
	
	
	print( "ss reassembled")
	list1=np.array([0]) #this is just to clean up RAM from lists for benchmarking
	
	print( "ss lists cleared")
	return list1

sort.__wrapped__(list1)



t10 = time.time()
ta = t10-t00
print("Custom completed in: ", ta, "ss total")
'''
from line_profiler import LineProfiler

lp = LineProfiler()
lp_wrapper = lp(sort.__wrapped__)
lp_wrapper(list1)
lp.print_stats()
#'''

#-- sorted() below --#

'''
#sorted()
print("now running sorted() ...")
list1 =  [random.randint(0, num) for x in range(num)]
print("running")
list1= sorted(list1)
print("Sorted() completed in: ", ta, "ss")
input("Done, enter to end")
'''
#np.sort()
list1 = np.random.randint(0, num, num, dtype="int64")
print("now running np.sort() ...")
t00 = time.time()
list1= np.sort(list1)
t10 = time.time()
ta = t10-t00

print("np.sort() completed in: ", ta, "ss")
input("Done, enter to end")
#'''
