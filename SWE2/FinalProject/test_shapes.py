import unittest
import math
import sys, os
from unittest.mock import MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shapes import (
    Rectangle, Circle, TriangleBuilder, Square,
    Ellipse, OldCircleSystem, OldCircleAdapter,
    PrinterManager, TextPrinter, LoggingShapeDecorator
)


class TestShapesUnit(unittest.TestCase):

    # ===============================
    # Rectangle Tests
    # ===============================
    def test_rectangle_area(self):
        r = Rectangle(5, 3)
        self.assertEqual(r.area(), 15)

    def test_rectangle_perimeter(self):
        r = Rectangle(5, 3)
        self.assertEqual(r.perimeter(), 16)

    def test_rectangle_zero_values(self):
        r = Rectangle(0, 0)
        self.assertEqual(r.area(), 0)
        self.assertEqual(r.perimeter(), 0)

    # ===============================
    # Circle Tests
    # ===============================
    def test_circle_area(self):
        c = Circle(2)
        self.assertAlmostEqual(c.area(), math.pi * 4, places=7)

    def test_circle_perimeter(self):
        c = Circle(2)
        self.assertAlmostEqual(c.perimeter(), 2 * math.pi * 2, places=7)

    def test_circle_zero_radius(self):
        c = Circle(0)
        self.assertEqual(c.area(), 0)
        self.assertEqual(c.perimeter(), 0)

    # ===============================
    # Triangle Builder Tests
    # ===============================
    def test_triangle_builder_perimeter(self):
        t = TriangleBuilder().set_a(3).set_b(4).set_c(5).build()
        self.assertEqual(t.perimeter(), 12)

    def test_triangle_builder_area(self):
        t = TriangleBuilder().set_a(3).set_b(4).set_c(5).build()
        self.assertAlmostEqual(t.area(), 6.0, places=7)

    # ===============================
    # Square Tests
    # ===============================
    def test_square_area(self):
        s = Square(4)
        self.assertEqual(s.area(), 16)

    def test_square_perimeter(self):
        s = Square(4)
        self.assertEqual(s.perimeter(), 16)

    # ===============================
    # Ellipse Tests
    # ===============================
    def test_ellipse_area(self):
        e = Ellipse(5, 3)
        self.assertAlmostEqual(e.area(), math.pi * 15, places=7)

    def test_ellipse_perimeter_positive(self):
        e = Ellipse(5, 3)
        self.assertTrue(e.perimeter() > 0)

    # ===============================
    # Adapter Pattern Tests
    # ===============================
    def test_old_circle_adapter_area(self):
        old = OldCircleSystem(4)
        adapted = OldCircleAdapter(old)
        self.assertEqual(adapted.area(), old.calc_area())

    def test_old_circle_adapter_perimeter(self):
        old = OldCircleSystem(4)
        adapted = OldCircleAdapter(old)
        self.assertEqual(adapted.perimeter(), old.calc_perimeter())

    # ===============================
    # Decorator Pattern Tests
    # ===============================
    def test_logging_decorator_area(self):
        s = LoggingShapeDecorator(Square(5))
        self.assertEqual(s.area(), 25)

    def test_logging_decorator_perimeter(self):
        s = LoggingShapeDecorator(Square(5))
        self.assertEqual(s.perimeter(), 20)

    # ===============================
    # Singleton + Observer Tests
    # ===============================
    def test_printer_manager_singleton(self):
        m1 = PrinterManager()
        m2 = PrinterManager()
        self.assertIs(m1, m2)

    def test_printer_manager_notifies_observer(self):
        manager = PrinterManager()
        mock_obs = MagicMock()
        manager.subject.attach(mock_obs)

        printer = TextPrinter()
        rect = Rectangle(2, 2)

        manager.print(printer, rect)

        mock_obs.update.assert_called_with(rect)

    # ===============================
    # Negative / Failing Scenario (Intentional)
    # ===============================
    def test_rectangle_area_fail_example(self):
        r = Rectangle(5, 3)
        # Wrong expected value (intentional failure for discussion)
        self.assertNotEqual(r.area(), 16)


if __name__ == "__main__":
    unittest.main()
