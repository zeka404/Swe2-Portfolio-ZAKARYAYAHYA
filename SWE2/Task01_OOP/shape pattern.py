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
        self.width, self.height = width, height

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


class TriangleBuilder:
    def __init__(self):
        self.a = self.b = self.c = None

    def set_a(self, a):
        self.a = a
        return self

    def set_b(self, b):
        self.b = b
        return self

    def set_c(self, c):
        self.c = c
        return self

    def build(self):
        return Triangle(self.a, self.b, self.c)


class EllipseBuilder:
    def __init__(self):
        self.a = None
        self.b = None

    def major_axis(self, a):
        self.a = a
        return self

    def minor_axis(self, b):
        self.b = b
        return self

    def build(self):
        return Ellipse(self.a, self.b)


class OldCircleSystem:
    def __init__(self, r):
        self.r = r

    def calc_area(self):
        return 3.14 * self.r * self.r

    def calc_perimeter(self):
        return 2 * 3.14 * self.r


class OldCircleAdapter(Shape):
    def __init__(self, old_circle):
        self.old_circle = old_circle

    def area(self):
        return self.old_circle.calc_area()

    def perimeter(self):
        return self.old_circle.calc_perimeter()


class ShapeDecorator(Shape):
    def __init__(self, shape: Shape):
        self.shape = shape

    def area(self):
        return self.shape.area()

    def perimeter(self):
        return self.shape.perimeter()


class LoggingShapeDecorator(ShapeDecorator):
    def area(self):
        print(f"[LOG] Calculating area of {self.shape.__class__.__name__}")
        return super().area()

    def perimeter(self):
        print(f"[LOG] Calculating perimeter of {self.shape.__class__.__name__}")
        return super().perimeter()


class Observer(ABC):
    @abstractmethod
    def update(self, shape: Shape):
        pass


class ConsoleObserver(Observer):
    def update(self, shape: Shape):
        print(f"[OBSERVER] {shape.__class__.__name__} has been printed.")


class PrintSubject:
    def __init__(self):
        self.observers = []

    def attach(self, obs: Observer):
        self.observers.append(obs)

    def notify(self, shape: Shape):
        for obs in self.observers:
            obs.update(shape)


class PrinterManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("[Singleton] Creating PrinterManager instance...")
            cls._instance = super().__new__(cls)
            cls._instance.subject = PrintSubject()
        return cls._instance

    def print(self, printer, shape: Shape):
        printer.print_info(shape)
        self.subject.notify(shape)


class ShapePrinter(ABC):
    @abstractmethod
    def print_info(self, shape: Shape):
        pass


class TextPrinter(ShapePrinter):
    def print_info(self, shape: Shape):
        print(f"Shape: {shape.__class__.__name__}")
        print(f"Area: {shape.area():.2f}")
        print(f"Perimeter: {shape.perimeter():.2f}")
        print("-" * 30)


class JSONPrinter(ShapePrinter):
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
    manager = PrinterManager()
    manager.subject.attach(ConsoleObserver())
    printer = TextPrinter()

    triangle = TriangleBuilder().set_a(3).set_b(4).set_c(5).build()
    ellipse = EllipseBuilder().major_axis(5).minor_axis(3).build()
    old_circle = OldCircleAdapter(OldCircleSystem(4))
    logged_square = LoggingShapeDecorator(Square(6))

    shapes = [
        factory.create_shape("rectangle", 5, 3),
        triangle,
        ellipse,
        old_circle,
        logged_square
    ]

    for s in shapes:
        manager.print(printer, s)
