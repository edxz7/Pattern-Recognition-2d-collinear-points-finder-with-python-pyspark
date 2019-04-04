import random
from timeit import Timer
# import memory_profiler as mem_profile
import pylab
import numpy

def merge_Sort(a):
    if len(a) < 2:
        return a
    mid = len(a)//2
    leftList = merge_Sort(a[:mid])
    rightList = merge_Sort(a[mid:])
    result = []
    while len(leftList)>=1 and len(rightList)>=1:
        if(leftList[0] <= rightList[0]):
            result.append(leftList.pop(0))
        else:
            result.append(rightList.pop(0))
    result += leftList
    result += rightList
    return result
    
# a = list(range(10,-1,-1))
# print(a)

# print(merge_Sort(a))
k=1000
xVals = []
yVals = []
y1Vals = []
a0 = list(range(500,-1,-1))
t0 = Timer("merge_Sort("+str(a0)+"),", "from __main__ import merge_Sort")
prev = min(t0.repeat(5,5)) #t0.timeit(number=1)
for i in range(11):
    a = list(range(k,-1,-1))
    t1 = Timer("merge_Sort("+str(a)+"),", "from __main__ import merge_Sort")
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


degrees = (1,2)

models = genFits(xVals,yVals,degrees)
testFits(models,degrees,xVals,yVals,'exchanges vs array size')


# array size:  16000  time:  0.154  s    ratio:  2.697  coefficient:  1.431
# array size:  32000  time:  0.415  s    ratio:  1.901  coefficient:  0.927
# array size:  64000  time:  0.79  s    ratio:  2.677  coefficient:  1.42
# array size:  128000  time:  2.114  s    ratio:  3.051  coefficient:  1.609
# array size:  256000  time:  6.449  s    ratio:  3.414  coefficient:  1.772
# array size:  512000  time:  22.021  s    ratio:  3.761  coefficient:  1.911
# array size:  1024000  time:  82.817  s    ratio:  4.171  coefficient:  2.06