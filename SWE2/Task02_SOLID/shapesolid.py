from abc import ABC, abstractmethod
import math


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius


class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def area(self):
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self):
        return self.a + self.b + self.c


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)


class Ellipse(Shape):
    def __init__(self, a, b):
        self.a, self.b = a, b

    def area(self):
        return math.pi * self.a * self.b

    def perimeter(self):
        h = ((self.a - self.b) ** 2) / ((self.a + self.b) ** 2)
        return math.pi * (self.a + self.b) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))

class ShapePrinter(ABC):
    @abstractmethod
    def print_info(self, shape: Shape):
        pass


class TextShapePrinter(ShapePrinter):
    def print_info(self, shape: Shape):
        print(f"Shape: {shape.__class__.__name__}")
        print(f"Area: {shape.area():.2f}")
        print(f"Perimeter: {shape.perimeter():.2f}")
        print("-" * 30)


class JSONShapePrinter(ShapePrinter):
    def print_info(self, shape: Shape):
        import json
        data = {
            "shape": shape.__class__.__name__,
            "area": round(shape.area(), 2),
            "perimeter": round(shape.perimeter(), 2)
        }
        print(json.dumps(data, indent=2))
        print("-" * 30)


class ShapeFactory:
    def create_shape(self, shape_type, *args):
        shapes = {
            "rectangle": Rectangle,
            "circle": Circle,
            "triangle": Triangle,
            "square": Square,
            "ellipse": Ellipse
        }
        cls = shapes.get(shape_type.lower())
        if not cls:
            raise ValueError(f"Unknown shape type: {shape_type}")
        return cls(*args)


if __name__ == "__main__":
    factory = ShapeFactory()
    printer = TextShapePrinter()

    shapes = [
        factory.create_shape("rectangle", 5, 3),
        factory.create_shape("circle", 4),
        factory.create_shape("triangle", 3, 4, 5),
        factory.create_shape("square", 6),
        factory.create_shape("ellipse", 5, 3)
    ]

    for s in shapes:
        printer.print_info(s)
