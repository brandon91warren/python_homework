import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other):
        if not isinstance(other, Point):
            raise TypeError("Distance must be computed between Points.")
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


class Vector(Point):

    def __str__(self):
        return f"Vector<{self.x}, {self.y}>"

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Can only add Vector to Vector")
        return Vector(self.x + other.x, self.y + other.y)


# -------------------------
# DEMONSTRATION
# -------------------------
if __name__ == "__main__":
    # Points
    p1 = Point(3, 4)
    p2 = Point(6, 8)
    p3 = Point(3, 4)

    print("Points:")
    print(p1)               # Point(3, 4)
    print(p2)               # Point(6, 8)
    print("p1 == p2?", p1 == p2)  # False
    print("p1 == p3?", p1 == p3)  # True
    print("Distance p1 → p2:", p1.distance_to(p2))

    print("\nVectors:")
    v1 = Vector(1, 2)
    v2 = Vector(3, 5)

    print(v1)               # Vector<1, 2>
    print(v2)               # Vector<3, 5>

    v3 = v1 + v2
    print("v1 + v2 =", v3)  # Vector<4, 7>
