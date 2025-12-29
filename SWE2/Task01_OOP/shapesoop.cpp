#include <iostream>
#include <cmath>
using namespace std;

class Shape {
public:
    virtual double area() = 0;
};

class Circle : public Shape {
    double r;
public:
    Circle(double r) : r(r) {}
    double area() {
        return M_PI * r * r;
    }
};

class Square : public Shape {
    double s;
public:
    Square(double s) : s(s) {}
    double area() {
        return s * s;
    }
};

class Rectangle : public Shape {
    double w, h;
public:
    Rectangle(double w, double h) : w(w), h(h) {}
    double area() {
        return w * h;
    }
};

class Triangle : public Shape {
    double b, h;
public:
    Triangle(double b, double h) : b(b), h(h) {}
    double area() {
        return 0.5 * b * h;
    }
};

class Ellipse : public Shape {
    double a, b;
public:
    Ellipse(double a, double b) : a(a), b(b) {}
    double area() {
        return M_PI * a * b;
    }
};

