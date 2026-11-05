import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    def test_standard_rates(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_standard_explicit(self):
        self.assertEqual(shipping_quote(2, "local", "standard"), 8.0)
        self.assertEqual(shipping_quote(2, "regional", "standard"), 11.0)

    def test_express_local(self):
        self.assertEqual(shipping_quote(2, "local", "express"), 15.0)

    def test_express_regional(self):
        self.assertEqual(shipping_quote(2, "regional", "express"), 18.0)

    def test_express_surcharge_is_seven(self):
        """Express is always $7 more than standard regardless of weight or zone."""
        for zone in ("local", "regional"):
            for weight in (1, 5, 10):
                std = shipping_quote(weight, zone, "standard")
                exp = shipping_quote(weight, zone, "express")
                self.assertAlmostEqual(exp - std, 7.0)

    def test_invalid_weight(self):
        with self.assertRaises(ValueError):
            shipping_quote(0, "local")

    def test_invalid_zone(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "international")

    def test_invalid_service(self):
        with self.assertRaises(ValueError):
            shipping_quote(1, "local", "overnight")
