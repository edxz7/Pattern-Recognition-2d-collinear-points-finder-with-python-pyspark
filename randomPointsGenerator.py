from Point import *
import random
import numpy

def random_points(n):
    points = numpy.empty(n, dtype = object)
    for i in range(n):
        points[i] = Point(random.randint(-1000,1000), random.randint(-1000,1000))
    return points