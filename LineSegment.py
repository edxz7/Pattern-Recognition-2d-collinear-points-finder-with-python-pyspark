import Point
class LineSegment(object):
    """
    Initializes a new line segment.
    
    @param  p one endpoint
    @param  q the other endpoint
    @throws NullPointerException if either p or q is null
    """
    def __init__(self, p, q):
        if(p == None or q == None):
            raise ValueError("argument is null")
        self.p = p
        self.q = q
    """
    #  Draws this line segment to standard draw
    """
    def draw(self):
        self.p.drawTo(self.q)

    """
    # Returns a string representation of this line segment
    # This method is provide for debugging;
    # your program should not rely on the format of the string representation.
    #
    # @return a string representation of this line segment
    """
    def __str__(self):
        s = "".join( str(self.p) + " -> " + str(self.q) )
        return s 


