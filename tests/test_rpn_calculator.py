# tests/test_rpn_calculator.py

import unittest
from app.rpn_calculator import evaluate_rpn

class TestRPNCalculator(unittest.TestCase):

    def test_simple_addition(self):
        self.assertEqual(evaluate_rpn("3 4 +"), 7)

    def test_complex_expression(self):
        self.assertEqual(evaluate_rpn("5 1 2 + 4 * + 3 -"), 14)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            evaluate_rpn("4 0 /")

if __name__ == "__main__":
    unittest.main()
