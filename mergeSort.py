import random
from timeit import Timer
# import memory_profiler as mem_profile
import pylab
import numpy

def merge(a,aux, lo, mid, hi):
    # aux = a[:]
    # aux = []
    for i in range(lo,hi+1):
        aux[i] = a[i] 
    # print('left', a[:mid])
    # print('right', a[mid:])
    i, j = lo, mid+1
    for k in range(lo,hi+1):
        if(i > mid): 
            a[k] = aux[j]
            j += 1
        elif(j > hi): 
            a[k] = aux[i]
            i += 1
        elif aux[i] <= aux[j]:
            a[k] = aux[i]
            i += 1
        else:
            a[k] = aux[j]
            j += 1
    # print(a)  

def sort(a,aux,lo,hi):
    if hi <= lo: return
    mid = lo + (hi-lo)//2
    sort(a,aux,lo,mid)
    sort(a,aux,mid +1, hi)
    if (a[mid] < a[mid+1]): return 
    merge(a,aux,lo,mid,hi)


def mergeSort(a):
    aux = a[:]
    sort(a,aux,0,len(a)-1)

a = list(range(5,-1,-1))
print(a)
mergeSort(a)
print(a)

k=1000
xVals = []
yVals = []
y1Vals = []
a0 = list(range(500,-1,-1))
t0 = Timer("mergeSort("+str(a0)+"),", "from __main__ import mergeSort")
prev = min(t0.repeat(5,5)) #t0.timeit(number=1)
for i in range(11):
    a = list(range(k,-1,-1))
    t1 = Timer("mergeSort("+str(a)+"),", "from __main__ import mergeSort")
    time = min(t1.repeat(5,5))
    ratio = time / prev
    xVals.append(k)
    yVals.append(prev)
    y1Vals.append(numpy.log2(ratio))
    print('array size:  ' + str(k) +  '  time:  ' + str(round(prev,3)) + "  s  " + "  ratio:  " + str(round(ratio,3)) + "  coefficient:  " + str(round(y1Vals[i],3)))
    prev = time
    k *= 2

# a = random.sample(range(10000),10000)
# t1 = Timer("mergeSort("+str(a)+"),", "from __main__ import mergeSort")
# print('Memory (Before): ' + str(mem_profile.memory_usage()) + 'MB' )
# print('Merge Sort index',min(t1.repeat(7,1000)))
# print('Memory (After) : ' + str(mem_profile.memory_usage()) + 'MB')

# Memory (Before): [53.90625]MB
# Merge Sort index 42.1490565
# Memory (After) : [54.00390625]MB



def rSquared(observed,predicted):
    error = ((observed-predicted)**2).sum()
    meanError = error/len(observed)
    return 1 -meanError/numpy.var(observed)

def genFits(xVals,yVals,degree):
    models=[]
    for d in degree:
        model = numpy.polyfit(xVals,yVals,d)
        models.append(model)
    return models

def testFits(models,degrees,xVals,yVals,title):
    pylab.plot(xVals,yVals,'o',label ='Data')
    for i in range(len(models)):
        estYvals = pylab.polyval(models[i],xVals)
        error = rSquared(yVals,estYvals)
        pylab.plot(xVals,estYvals,label = 'Fit of degree '\
                   + str(degrees[i])\
                   + ', R2 = ' + str(round(error, 5)))
    pylab.legend(loc = 'best')
    pylab.title(title)
    pylab.show()


degrees = (1,)

models = genFits(xVals,yVals,degrees)
testFits(models,degrees,xVals,yVals,'time vs array size')


# array size:  1000  time:  0.008  s    ratio:  2.305  coefficient:  1.205
# array size:  2000  time:  0.018  s    ratio:  2.15  coefficient:  1.104
# array size:  4000  time:  0.038  s    ratio:  2.011  coefficient:  1.008
# array size:  8000  time:  0.076  s    ratio:  2.053  coefficient:  1.038
# array size:  16000  time:  0.156  s    ratio:  2.378  coefficient:  1.25
# array size:  32000  time:  0.372  s    ratio:  2.197  coefficient:  1.136
# array size:  64000  time:  0.817  s    ratio:  1.742  coefficient:  0.801
# array size:  128000  time:  1.424  s    ratio:  2.083  coefficient:  1.059
# array size:  256000  time:  2.966  s    ratio:  2.247  coefficient:  1.168
# array size:  512000  time:  6.663  s    ratio:  2.034  coefficient:  1.024
# array size:  1024000  time:  13.553  s    ratio:  2.129  coefficient:  1.09