import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shapes import Rectangle, Circle, TriangleBuilder, PrinterManager, TextPrinter, ConsoleObserver, OldCircleAdapter, OldCircleSystem, Square, LoggingShapeDecorator

manager = PrinterManager()

observer = ConsoleObserver()
manager.subject.attach(observer)

printer = TextPrinter()

rectangle = Rectangle(5, 3)
circle = Circle(2)
triangle = TriangleBuilder().set_a(3).set_b(4).set_c(5).build()
square = LoggingShapeDecorator(Square(4))
old_circle = OldCircleAdapter(OldCircleSystem(3))

shapes = [rectangle, circle, triangle, square, old_circle]

for shape in shapes:
    print("==== Printing Shape ====")
    manager.print(printer, shape)
