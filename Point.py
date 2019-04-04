import stddraw
class Point(object):
    """
    Initializes a new point
    
    @param  x-coordinate of the point
    @param  y-coordinate of the point    
    """
    def __init__(self, x, y):
        self._x = x
        self._y = y
        
    """
    Initializes a new point
    
    @param  x-coordinate of the point
    @param  y-coordinate of the point    
    """
    def __str__(self):
        return "(" + str(self._x) + " , " + str(self._y) + ")"

    """
    Draw a line segment from this point to the other
    """
    def drawTo(self, other):
        stddraw.line(self._x, self._y, other._x, other._y)

    """
    Draws this point to standard draw
    """
    def draw(self):
        stddraw.point(self._x, self._y)

    """
    Returns the slope between this point and the other point.
    Formally, if we have the points (x0, y0) and (x1, y1), the slope
    is defined as (y1 - y0) / (x1 - x0). For completeness, the slope 
    is 0 if the line segment connecting the two points is horizontal
    "inf" if the line segment is vertical and "-inf" if (x0, y0) and 
    (x1, y1) are equal.
    
    @param  the other point
    @return the slope between this point and the specified point
    """
    def slopeTo(self,other):
        if(self._x == other._x and self._y == other._y): return float("-inf")
        elif (self._x == other._x): return float("inf")
        elif (self._y == other._y): return 0
        return (other._y - self._y)/(other._x - self._x)

    #----------------------------------------------------------------------
    #  In this sectrion all the magic methods required to allow comparisons
    #  between two points are defined. The comparison is achieve as follows
    #  * Compares two points by y-coordinate, breaking ties by x-coordinate.
    #  * Formally, the self point (x0, y0) is less than the argument point
    #    (x1, y1) if and only if either y0 < y1 or if y0 = y1 and x0 < x1.
    #  
    #    @param  the other point
    #    @return the value 0 if this point is equal to the argument
    #            point (x0 = x1 and y0 = y1);
    #            a negative integer if this point is less than the argument
    #            point; and a positive integer if this point is greater than the
    #            argument point   

    def __lt__(self,other):
        if isinstance(other, Point):
            if (self._y != other._y): return self._y < other._y 
            elif (self._y == other._y): return self._x < other._x

    def __gt__(self,other):
        if isinstance(other, Point):
            if (self._y != other._y): return self._y > other._y 
            elif (self._y == other._y): return self._x > other._x

    def __eq__(self,other):
        if isinstance(other, Point):
            return self._y == other._y and self._x == other._x

    def __le__(self,other):
        if isinstance(other, Point):
            if(self._y != other._y): return self._y < other._y
            elif(self._y == other._y): return self._x <= other._x

    def __ge__(self,other):
        if isinstance(other, Point):
            if(self._y != other._y): return self._y > other._y
            elif(self._y == other._y): return self._x >= other._x

    #---------------------------------------------------------------------

# p1 = Point(100,1)
# p2 = Point(9,200)
# p3 = Point(9,2)
# lst = [p1, p2, p3] 
# sorted(lst,key = lambda p: lst[0].slopeTo(p))
# origin = lst[0]
# lst.sort(key = lambda p: origin.slopeTo(p))
# lst.sort()
# for i in range(len(lst)):
#     print(str(lst[i]))

# print(p1 >= p2)