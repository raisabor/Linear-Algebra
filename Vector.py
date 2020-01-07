from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):


    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = "No unique orthogonal component"
                                        
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = "No unique parallel component"
                                       
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = "Cross product is only defined for R^2 and R^3"


    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        newCoordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        #newCoordinates = []
        #n = len(self.coordinates)
        #for i in range(n):
        #    newCoordinates.append(self.coorinates[i] + v.coordinates[i])
        return Vector(newCoordinates)

    def minus(self, v):
        newCoordinates = [x-y for x,y in zip(self.coordinates + v.coordinates)]
        return Vector(newCoordinates)

    def timesScalar(self, c):
        newCoordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(newCoordinates)

    def magnitude(self):
        newCoordinates = [(x**2) for x in self.coordinates]
        return sqrt(sum(newCoordinates))

    def normalized(self):
     try:
        magnitude = self.magnitude()
        return self.timesScalar(1.0/magnitude)
    
     except ZeroDivisionError:
        raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dot(self, v):
        newCoordinates = [x*y for x,y in zip(self.coordinates, v.coordinates)]
        return sum(newCoordinates)
    
    def angleWith(self, v, inDegrees = False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angleInRadians = acos(u1.dot(u2))

            if inDegrees:
                degreePerRadians = 180 / pi
                return angleInRadians * degreePerRadians
            else:
                return angleInRadians

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception("Cannot commute an angle with zero vector")
            #else:
                #raise e

    def isParallelTo(self, v):
        return(self.isZero() or v.isZero() or self.angleWith(v) == 0 or self.angleWith(v) == pi)
        
    def isZero(self, tolerance = 1e-10):
        return (self.magnitude() < tolerance)       

    def isOrthogonalTo(self, v, tolerance = 1e-10):
        return abs(self.dot(v)) < tolerance

    def componentParallelTo(self, basis):
        try:
            u = basis.normalized()
            weight= self.dot(u)
            return u.timesScalar(weight)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARRALEL_COMPONENT_MSG)
            else:
                raise e

    
    def componentOrthogonalTo(self, basis):
        try:
            projection = self.componentParallelTo(basis)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
               raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def cross(self, v):
        try:
            x1, y1, z1 = self.coordinates
            x2, y2, z2 = v.coordinates
            
            newCoordinates = [y1*z2 - y2*z1, -(x1*z2 - x2*z1), x1*y2 - x2*y1]

            return Vector(newCoordinates)

        except ValueError as e:
            msg = str(e)
            if msg == "need more than 2 values to unpack":
                selfEmbeddedInR3 = Vector(self.coordinates + ('0',))
                vEmbeddedInR3 = Vector(v.coordinates + ('0', ))
                return selfEmbeddedInR3.cross(vEmbeddedInR3)
            elif (msg == "too many values to unpack " or msg == "need more than 1 value to unpack"):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else: 
                raise e

    def areaOfTriangleWith(self, v):
        return self.areaOfParallelogramWith(v) / Decimal("2.0")                

    def areaOfParallelogramWith(self, v):
        crossProduct = self.cross(v)
        return crossProduct.magnitude()

myVector1 = Vector([3.039, 1.879])
myVector2 = Vector([0.825, 2.036])

myVector3 = Vector([-2.029, 9.97, 4.172])
myVector4 = Vector([-9.231, -6.639, -7.245])

myVector5 = Vector([2.118, 4.827])
myVector6 = Vector([0, 0])

myVector7 = Vector([-2.328, -7.284, -1.214])
myVector8 = Vector([-1.821, 1.072, -2.94])



