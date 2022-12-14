from typing import List, Optional,Union, Tuple
import math

AnyNumber = Union[int, float]
FloatIterable = Union[List[float], Tuple[float, ...]]
IntIterable = Union[List[int], Tuple[int, ...]]
AnyNumberIterable = Union[List[AnyNumber], Tuple[AnyNumber, ...]]

class AxisAlignedBoundingBox2D():
    """Contains data for an Axis Aligned Bounding Box"""
    def __init__(self) -> None:
        self.bInitialized: bool = False
        self.minX: AnyNumber = 0
        self.minY: AnyNumber = 0

        self.maxX: AnyNumber = 0
        self.maxY: AnyNumber = 0

    def add_point(self, vertex: AnyNumberIterable):
        """Adds a point to be considered for this AABB. This expands the AABB dimensions immediately."""
        #If not initialized, set the limits to match this point
        if self.bInitialized is False:
            self.bInitialized = True
            self.minX = vertex[0]
            self.maxX = vertex[0]
            self.minY = vertex[1]
            self.maxY = vertex[1]
            return

        if self.minX > vertex[0]:
            self.minX = vertex[0]
        if self.maxX < vertex[0]:
            self.maxX = vertex[0]

        if self.minY > vertex[1]:
            self.minY = vertex[1]
        if self.maxY < vertex[1]:
            self.maxY = vertex[1]

    def get_center_position(self) -> List[AnyNumber]:
        """Returns a point which is exactly in the center of this AABB. Useful for working out offsets, pivots etc"""
        size = self.get_size()
        X_size = size[0]
        X = self.minX + (X_size / 2)

        Y_size = size[1]
        Y = self.minY + (Y_size / 2)

        position = [X, Y]
        return position
    
    def get_min(self) -> List[AnyNumber]:
        return [self.minX, self.minY]
    
    def get_max(self) -> List[AnyNumber]:
        return [self.maxX, self.maxY]

    def merge(self, other: Optional['AxisAlignedBoundingBox2D']) -> Optional['AxisAlignedBoundingBox2D']:
        """Creates a new AABB which has a size that encompasses both self and other"""
        if self.bInitialized is False and other.bInitialized is False:
            return self

        if self.bInitialized is False:
            return other

        newAABB = AxisAlignedBoundingBox2D()
        newAABB.bInitialized = True

        if self.minX > other.minX:
            newAABB.minX = other.minX
        else:
            newAABB.minX = self.minX

        if self.minY > other.minY:
            newAABB.minY = other.minY
        else:
            newAABB.minY = self.minY

        if self.maxX < other.maxX:
            newAABB.maxX = other.maxX
        else:
            newAABB.maxX = self.maxX

        if self.maxY < other.maxY:
            newAABB.maxY = other.maxY
        else:
            newAABB.maxY = self.maxY

        return newAABB

    def get_size(self) -> List[AnyNumber]:
        """Returns a list containing the extents/magnitudes of X,Y and Z."""
        newSize = []
        newSize.append(abs(self.maxX - self.minX))
        newSize.append(abs(self.maxY - self.minY))
        return newSize

class Point2D:
    def __init__(self,x: AnyNumber = 0, y: AnyNumber = 0) -> None:
        self.point: List[AnyNumber] = [x,y]

    @property
    def x(self):
        return self.point[0]
    
    @x.setter
    def x(self, value: AnyNumber):
        self.point[0] = value

    @property
    def y(self):
        return self.point[1]
    
    @y.setter
    def y(self, value: AnyNumber):
        self.point[1] = value
    
    @property
    def size(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def add(self, other: Optional['Point2D']) -> Optional['Point2D']: 
        NewPoint = Point2D(self.x + other.x, self.y + other.y)
        return NewPoint

    def multiply(self, other: Optional['Point2D']) -> Optional['Point2D']: 
        NewPoint = Point2D(self.x * other.x, self.y * other.y)
        return NewPoint
