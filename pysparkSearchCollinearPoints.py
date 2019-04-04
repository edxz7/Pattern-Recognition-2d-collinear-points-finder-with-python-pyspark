from pyspark import SparkContext, SparkConf   
from pyspark.rdd import RDD
import Point
import LineSegment
import randomPointsGenerator
import numpy
import stddraw

#*****************************************************************************
#  Execution:    spark-submit pysparkSearchCollinearPoints.py file_name
#  Dependencies: pyspark, pathlib, sys, numpy, pygame
#
#  Pattern recognition algorithm. Finds all the unique line segments build with
#  at leat k collinear 2D points from an arbitrary array of points expressed in
#  cartessian coordinates. k must be greater or equal to 3
#
#  Complexity: (n^2) where n is the size of the array of points
#
#  @author Eduardo Ch. Colorado
#******************************************************************************/

# *Introduction
# Unlike other computational paradigmas like OOP, distribuite computing requires impose certain 
# restriction in the way we do programs. For example, we can't make explicit reference  to any 
# element of an array (indexing) because we don't known how the data was split and ordered.
# For this reason a different approach respect to the fast search will be taken to write this code. 
#
# * Selected parametrization
# A line is as the set of points (x,y) that can be expressed as y=mx+b for some fixed real values 
# (m, b) where m is the slope and is the y-intercept (the value of y when x = 0)
#
# * Corner cases assumptions
# if    x1 = x2 => (inf, int)
# else  (m, b) is such that y1 = mx1 + b and y2 = mx2 +b
#
# * Algorithm
# 1. Compute the cartesian product of the input lit of coordinates with itself.
# 2. The resulting list wil be a list of pairs pair of points from which all duplicates, 
#    like ((5,0),(5,0)) are removed, and for the rest we calculate its paramters (m,b) of the line connecting them
# 3. Group all the point pairs with the same parameters. If two pairs have the same (m,b) values, 
#    they lie on the same line. Only goups contaning more or equal (k -1) elements represent k collinear points 
# 4. Unpack the point-pairs to identify the individual points.
# 5. Output the sets of k or more colinear points.   

# *CODE

#We can create a SparkConf() object and use it to initialize the spark context
conf = SparkConf().setAppName("Collinear Points").setMaster("local[2]") #Initialize spark context using 4 local cores as workers
sc = SparkContext(conf=conf)    

# set of functions require to do the computations
def format_result(x):
    x[1].append(x[0][0])
    return tuple(x[1])

def to_sorted_points(x):
    """
    Sorts and returns a tuple of points for further processing.
    """
    return tuple(sorted(x))

# transform the string '1 1' to the tuple (1,1)
def to_tuple(x):
    return tuple(map(int,x.split()))

def non_duplicates(x):
    """ 
    Use this function inside the get_cartesian() function to 'filter' out pairs with duplicate points
    """
    temp = sorted(x)
    temp_p = None
    for p in temp:
        if p == temp_p:
            return False
        temp_p = p
    return True

def get_cartesian(rdd):
    """ 
    Compute the cartesian product
    """
    a = rdd.cartesian(rdd)
    return a.filter(non_duplicates)

def find_slope(x):
    if(x[0][0] == x[1][0]):
        return ((x[0],'inf'), x[1])
    slope = (x[1][1] - x[0][1])/(x[1][0] - x[0][0])
    return ((x[0], slope), x[1])

def find_collinear(rdd, k):
    a = rdd.map(lambda x: find_slope(x))                                # find the slope of each element
    b = a.groupByKey().mapValues(lambda x: [a for a in x])
    c = b.filter(lambda x: len(x[1]) >= (k - 1))                        # only keys with list lenght bigger or equal than (k-1) represent k collinear points
    d = c.map(format_result).map(to_sorted_points).map(lambda x: (x, 1))
    e = d.reduceByKey(lambda x, y: x + y).map(lambda x: x[0])           # duplicates are summed, we ignored the counts
    return e

def build_collinear_set(rdd, k):
    rdd = rdd.map(to_tuple)          # trannsform the read data into tuples 
    rdd = get_cartesian(rdd)         # compute the cartesian product
    rdd = find_collinear(rdd, k)     # find the collinear points
    rdd = rdd.map(to_sorted_points)  # sort the result
    return rdd

def process(rdd, k):
    """
    This is the process function used for finding collinear points using inputs from different files
    Input: rdd containing the input points
    Output: Set of collinear points
    """
    # Search the set of collinear points
    rdd = build_collinear_set(rdd, k)
    # Collecting the collinear points RDD in a set to remove duplicate sets of collinear points. 
    res = set(rdd.collect()) 
    return res

def points_from_file(file):
    '''
    Read the the input from a file
    '''
    data = open(file)
    n = int(data.readline())
    points_to_draw = numpy.empty(n, dtype=object)  # set of points for drawing purposes
    pts = []                                       # set pf poinrs for the calculations
    i = 0
    for line in data:
        pts.append(line)
        x, y = line.split()
        x, y = int(x), int(y)
        # print(x, " , ", y)
        points_to_draw[i] = Point.Point(x, y)
        i += 1
    return (pts, points_to_draw)

def points_from_random(n):
    '''
    Create the input using a random generator
    '''
    points_to_draw = randomPointsGenerator.random_points(n)
    pts = []                                     # set pf poinrs for the calculations
    for p in points_to_draw:
        x, y = p._x, p._y
        pts.append(str(x) + " " + str(y))
    return (pts, points_to_draw)

# Read the data 
# Note: the same data is stored in two lists: points_to_draw for drawing and the pts for calculations
k = 5
file_path = "data/input20.txt"
pts, points_to_draw = points_from_file(file_path)

# * Random points generator
# Instead of read the data from a file, uncomment the line below to generate them randomly
# k = 4
# pts, points_to_draw = points_from_random(200)

# set canvas size
screen_width_max  = max(points_to_draw,key=lambda a:a._x)._x
screen_high_max   = max(points_to_draw,key=lambda a:a._y)._y
screen_width_min  = min(points_to_draw,key=lambda a:a._x)._x
screen_high_min   = min(points_to_draw,key=lambda a:a._y)._y
width_buffer      = int(screen_width_max*0.01)
high_buffer       = int(screen_high_max*0.01)
stddraw.setCanvasSize(800, 800)
stddraw.setXscale(screen_width_min - width_buffer, screen_width_max + width_buffer)
stddraw.setYscale(screen_high_min  - high_buffer , screen_high_max  + high_buffer)
stddraw.setPenRadius(0.005)

#find the collinear points
points = sc.parallelize(pts)        
collinear_points = process(points, k)  # list of all collinear points found

# collect all the segments joining collinear points with at least 
collinear_segments = []
for col_pts in collinear_points:
    collinear_segments.append(LineSegment.LineSegment(Point.Point(col_pts[0][0],col_pts[0][1]), Point.Point(col_pts[-1][0], col_pts[-1][1])))


for segment in collinear_segments:
    print(segment)
    segment.draw()

# draw the points
stddraw.setPenRadius(0.01)
stddraw.setPenColor(stddraw.RED)
for p in points_to_draw:
    p.draw()

# number of lines
print(len(collinear_segments))

stddraw.show()