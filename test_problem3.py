"""
问题 3 单元测试: Order

说明：
使用 Python 的 unittest 框架补全下面的单元测试方法。
你的测试方法必须断言 Order 对象上的多个属性
（例如 subtotal、discount_amount、tax_amount、shipping_fee、final_total、status）
以验证在各种条件下的状态一致性。

运行测试：
    python -m unittest test_problem3.py -v
"""
import copy
import unittest
from problem3 import Order


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.regular_order = Order("ORD100", customer_tier="regular")
        self.silver_order = Order("ORD200", customer_tier="silver")
        self.gold_order = Order("ORD300", customer_tier="gold")

    # 1. 验证初始状态、商品的添加、减少和删除
    def test_add_and_remove(self):
        for order in [self.regular_order, self.silver_order, self.gold_order]:
            self.assertEqual(order.items, {})
            self.assertEqual(order.status, "PENDING")
            self.assertIsNone(order.applied_coupon)
            self.assertEqual(order.subtotal, 0.0)
            self.assertEqual(order.discount_amount, 0.0)
            self.assertEqual(order.tax_amount, 0.0)
            self.assertEqual(order.shipping_fee, 0.0)
            self.assertEqual(order.final_total, 0.0)

        self.assertEqual(self.regular_order.order_id, "ORD100")
        self.assertEqual(self.regular_order.customer_tier, "regular")
        self.assertEqual(self.silver_order.customer_tier, "silver")
        self.assertEqual(self.gold_order.customer_tier, "gold")

        a = self.regular_order
        a.add_item("book", 10.0, 2)
        a.add_item("book", 10.0, 1)
        self.assertEqual(a.items["book"]["quantity"], 3)
        self.assertEqual(a.get_summary(), {
            "order_id": "ORD100", "tier": "regular", "status": "PENDING",
            "item_count": 3, "subtotal": 30.0, "discount_amount": 0.0,
            "tax_amount": 2.4, "shipping_fee": 5.99, "final_total": 38.39,
        })

        a.remove_item("book", 1)
        self.assertEqual(a.items["book"]["quantity"], 2)
        self.assertEqual(a.get_summary(), {
            "order_id": "ORD100", "tier": "regular", "status": "PENDING",
            "item_count": 2, "subtotal": 20.0, "discount_amount": 0.0,
            "tax_amount": 1.6, "shipping_fee": 5.99, "final_total": 27.59,
        })

        a.remove_item("book")
        self.assertEqual(a.items, {})
        self.assertEqual(a.get_summary(), {
            "order_id": "ORD100", "tier": "regular", "status": "PENDING",
            "item_count": 0, "subtotal": 0.0, "discount_amount": 0.0,
            "tax_amount": 0.0, "shipping_fee": 0.0, "final_total": 0.0,
        })

    # 2. 验证会员折扣、优惠券
    def test_discounts(self):
        a = self.silver_order
        b = self.gold_order
        c = self.regular_order

        for order in [a, b, c]:
            order.add_item("book", 50.0, 2)
            self.assertEqual(order.subtotal, 100.0)
            self.assertEqual(order.shipping_fee, 0.0)
            self.assertEqual(order.status, "PENDING")

        self.assertAlmostEqual(a.discount_amount, 5.0)
        self.assertAlmostEqual(a.tax_amount, 7.6)
        self.assertAlmostEqual(a.final_total, 102.6)
        self.assertAlmostEqual(b.discount_amount, 10.0)
        self.assertAlmostEqual(b.tax_amount, 7.2)
        self.assertAlmostEqual(b.final_total, 97.2)
        self.assertAlmostEqual(c.discount_amount, 0.0)
        self.assertAlmostEqual(c.tax_amount, 8.0)
        self.assertAlmostEqual(c.final_total, 108.0)

        b.apply_coupon(" save10 ")
        self.assertEqual(b.applied_coupon, "SAVE10")
        self.assertAlmostEqual(b.discount_amount, 19.0)
        self.assertAlmostEqual(b.tax_amount, 6.48)
        self.assertEqual(b.shipping_fee, 0.0)
        self.assertAlmostEqual(b.final_total, 87.48)

        a.apply_coupon("FLAT15")
        self.assertEqual(a.applied_coupon, "FLAT15")
        self.assertAlmostEqual(a.discount_amount, 20.0)
        self.assertAlmostEqual(a.tax_amount, 6.4)
        self.assertEqual(a.shipping_fee, 0.0)
        self.assertAlmostEqual(a.final_total, 86.4)

        small_order = Order("ORD400")
        small_order.add_item("pen", 10.0)
        small_order.apply_coupon("FLAT15")
        self.assertAlmostEqual(small_order.discount_amount, 10.0)
        self.assertAlmostEqual(small_order.tax_amount, 0.0)
        self.assertAlmostEqual(small_order.shipping_fee, 5.99)
        self.assertAlmostEqual(small_order.final_total, 5.99)

    # 3. 验证运费、免税
    def test_shipping_and_tax(self):
        a = self.regular_order
        a.add_item("book", 20.0, 2)
        self.assertAlmostEqual(a.subtotal, 40.0)
        self.assertAlmostEqual(a.tax_amount, 3.2)
        self.assertAlmostEqual(a.shipping_fee, 5.99)
        self.assertAlmostEqual(a.final_total, 49.19)

        a.add_item("pen", 10.0)
        self.assertAlmostEqual(a.subtotal, 50.0)
        self.assertAlmostEqual(a.tax_amount, 4.0)
        self.assertEqual(a.shipping_fee, 0.0)
        self.assertAlmostEqual(a.final_total, 54.0)

        a.add_item("apple", 10.0, 2, category="grocery")
        self.assertAlmostEqual(a.subtotal, 70.0)
        self.assertAlmostEqual(a.tax_amount, 4.0)
        self.assertEqual(a.shipping_fee, 0.0)
        self.assertAlmostEqual(a.final_total, 74.0)
        self.assertEqual(a.get_summary()["item_count"], 5)

        # 重新收取运费
        boundary_order = Order("ORD500")
        boundary_order.add_item("rice", 20.0, category="grocery")
        boundary_order.add_item("book", 30.0)
        boundary_order.apply_coupon("SAVE10")
        self.assertAlmostEqual(boundary_order.subtotal, 50.0)
        self.assertAlmostEqual(boundary_order.discount_amount, 5.0)
        self.assertAlmostEqual(boundary_order.tax_amount, 2.16)
        self.assertAlmostEqual(boundary_order.shipping_fee, 5.99)
        self.assertAlmostEqual(boundary_order.final_total, 53.15)

    # 4. 验证结账、取消，以及状态改变后的修改限制
    def test_order_status(self):
        a = self.regular_order
        b = self.silver_order
        for order in [a, b]:
            order.add_item("book", 20.0, 2)

        self.assertTrue(a.checkout())
        self.assertEqual(a.status, "PAID")
        self.assertEqual(a.get_summary()["status"], "PAID")
        self.assertAlmostEqual(a.final_total, 49.19)

        self.assertTrue(b.cancel())
        self.assertEqual(b.status, "CANCELLED")
        self.assertEqual(b.get_summary()["status"], "CANCELLED")
        self.assertAlmostEqual(b.discount_amount, 2.0)
        self.assertAlmostEqual(b.tax_amount, 3.04)
        self.assertAlmostEqual(b.final_total, 47.03)

        with self.assertRaises(RuntimeError):
            a.cancel()
        self.assertEqual(a.status, "PAID")

        for order in [a, b]:
            before = copy.deepcopy(order.__dict__)
            with self.assertRaises(RuntimeError):
                order.add_item("pen", 5.0)
            with self.assertRaises(RuntimeError):
                order.remove_item("book")
            with self.assertRaises(RuntimeError):
                order.apply_coupon("SAVE10")
            with self.assertRaises(RuntimeError):
                order.checkout()
            self.assertEqual(order.__dict__, before)

    # 5. 验证异常
    def test_invalid_operations(self):
        a = self.regular_order
        with self.assertRaises(ValueError):
            Order("BAD", "invalid")
        with self.assertRaises(ValueError):
            a.checkout()
        self.assertEqual(a.status, "PENDING")
        self.assertEqual(a.items, {})

        for value in [0, -1]:
            with self.assertRaises(ValueError):
                a.add_item("book", value, 1)
            with self.assertRaises(ValueError):
                a.add_item("book", 20.0, value)
        self.assertEqual(a.items, {})
        self.assertAlmostEqual(a.final_total, 0.0)

        a.add_item("book", 20.0, 2)
        before = copy.deepcopy(a.__dict__)
        with self.assertRaises(KeyError):
            a.remove_item("missing")
        with self.assertRaises(ValueError):
            a.apply_coupon("INVALID")
        for quantity in [0, -1]:
            with self.assertRaises(ValueError):
                a.remove_item("book", quantity)
        self.assertEqual(a.__dict__, before)


if __name__ == "__main__":
    unittest.main()
