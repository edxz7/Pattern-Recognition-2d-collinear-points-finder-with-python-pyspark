from Point import * 
from LineSegment import *
import sys
from pathlib import Path
import numpy
import stddraw

#*****************************************************************************
#  Execution:    python fastSearchCollinearPoints.py k file_name
#  Dependencies: pathlib, sys, numpy, pygame
#
#  Pattern recognition algorithm. Finds all the unique line segments build with
#  at leat k collinear 2D points from an arbitrary array of points expressed in
#  cartesian coordinates. k must be greater or equal to 3
#
#  Complexity: (n ln (n)) where n is the size of the array of points
#
#  @author Eduardo Ch. Colorado
#******************************************************************************/

class fastSearchCollinearPoints(object):
    """
    * This code search all the unique segments build with at least 4 collinear points 
    * from an array of 2D points (expresses in cartesian coordinates), draw them and 
    * print the start and end points of each segment.
    * 
    * If we have the collinear points  s -> p -> q -> r -> t -> u the printed segment 
    * is s -> u. The sub-segments can also be printed with minimal modifications to the 
    * code, but the ouput could be overwhelming for big arrays
    """
    
    def __init__(self, points, k):
        n = points.size
        # for i in range(n):
        #     if points[i] == None:
        #         raise AssertionError("a null element was passed")
        spoints = sorted(points)
        # uncommennt to detect inputs with duplicates points
        # for i in range(n):   
        #     if(i-1 > n and spoints[i] == spoints[i-1]): 
        #         raise AssertionError("duplicate points")

        self.numOfLineSegments = 0
        self.lineSegments = numpy.empty(n*n, dtype=object)
        
        if None in points: raise AssertionError()

        # main loop. unbelievable this complex task can bbe achieve usinng
        # two stable sortings of the array 
        for o in range(0, n):
            count = 0
            segLength = 0
            spoints.sort()       # array sorted with respect the natural order
            origin = spoints[o]
             # array sorted with respect to the slope of the current selected point (origin)
             # and the rest of the array
            spoints.sort(key=lambda p: origin.slopeTo(p)) 
            for i in range(0, n):
                if(i-1>0 and origin.slopeTo(spoints[i]) == origin.slopeTo(spoints[i-1])):
                    count += 1
                    segLength += 1
                else:
                    count = 0
                    segLength = 0
                if(count > (k - 3)): # 0 three collinear points, 1 for four collinear points and so on
                    if(origin > spoints[i - segLength]): count = 0
                    elif(count > (k - 2)): self.lineSegments[self.numOfLineSegments-1] = LineSegment(origin, spoints[i])
                    else:
                        self.lineSegments[self.numOfLineSegments] = LineSegment(origin, spoints[i])
                        self.numOfLineSegments += 1

            #     print(str(o) + "  " + str(spoints[i]) +  " -- " +  str(origin.slopeTo(spoints[i])))
            # print("----")

    def numberOfSegments(self):
        # the number of line segments
        return self.numOfLineSegments

    def segments(self):
        # the line segments
        idx = 0
        segments = numpy.empty(self.numOfLineSegments, dtype=object)
        for i in range(0, self.numOfLineSegments) :
            if(self.lineSegments[i] !=None): 
                segments[idx] = self.lineSegments[i]
                idx += 1

        return  segments

import randomPointsGenerator

def main():
    # Open file from the command liness
    try:
        k         = sys.argv[1]              # number of collinear points to search
        file_name = sys.argv[2]              # file name
        path      = Path.cwd()
        file_path = path / 'data' / file_name
        if k <= 2: raise AssertionError("We neead at least search for three collinear points")
    except:
        k = 4
        file_name = 'input20.txt'           # defaul file
        path      = Path.cwd()
        file_path = path / 'data' / file_name

    data = open(file_path)
    n = data.readline()
    points = numpy.empty(int(n), dtype=object)
    i = 0
    # print("n = ",points.size)
    for line in data:
        x, y = line.split()
        x = int(x)
        y = int(y)
        # print(x, " , ", y)
        points[i] = Point.Point(x, y)
        i += 1

    # * Random points generator
    # Instead of read the data from files, uncomment the lines below to generate them randomly
    # and set k to search for at leat k collinear points
    k = 4
    points = randomPointsGenerator.random_points(2000)

    # set canvas size
    screen_width_max  = max(points,key=lambda a:a._x)._x
    screen_high_max   = max(points,key=lambda a:a._y)._y
    screen_width_min  = min(points,key=lambda a:a._x)._x
    screen_high_min   = min(points,key=lambda a:a._y)._y
    width_buffer = int(screen_width_max*0.01)
    high_buffer = int(screen_high_max*0.01)
    stddraw.setCanvasSize(800, 800)
    stddraw.setXscale(screen_width_min - width_buffer, screen_width_max + width_buffer)
    stddraw.setYscale(screen_high_min  - high_buffer , screen_high_max  + high_buffer)
    stddraw.setPenRadius(0.01)

    #print and draw the line segments
    collinear_points = fastSearchCollinearPoints(points, k)

    for segment in collinear_points.segments():
        print(segment)
        segment.draw()

    stddraw.setPenRadius(0.005)
    stddraw.setPenColor(stddraw.RED)
    for p in points:
        p.draw()


    print(collinear_points.numberOfSegments())

    stddraw.show()

    # Insert Manualy the points 
    # p1 = Point.Point(100,1)
    # p2 = Point.Point(9,200)
    # p3 = Point.Point(9,2)
    # points = [p1, p2, p3] 
    # fastSearchCollinearPoints(points)

if __name__ == '__main__':
    main()