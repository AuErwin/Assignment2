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
import unittest
from problem3 import Order


class TestOrder(unittest.TestCase):

    def setUp(self):
        """
        在每个测试方法执行前设置测试夹具。
        """
        self.regular_order = Order("ORD100", customer_tier="regular")
        self.silver_order = Order("ORD200", customer_tier="silver")
        self.gold_order = Order("ORD300", customer_tier="gold")

    # TODO: 为 Order 类开发 5 个测试方法 develop 5 test methods for Order class
    def test_rename_it(self):
        """
        TODO: 在此描述你的测试。
        """
        #验证初始状态和添加、删除商品
        def test_add_and_remove(self):
            for order in [
                self.regular_order,
                self.silver_order,
                self.gold_order]:
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
            self.assertEqual(self.silver_order.order_id, "ORD200")
            self.assertEqual(self.silver_order.customer_tier, "silver")
            self.assertEqual(self.gold_order.order_id, "ORD300")
            self.assertEqual(self.gold_order.customer_tier, "gold")

            a=self.regular_order
            a.add_item("book", 10.00, 2)
            a.add_item("book", 5.00)
            self.assertEqual(a.items["book"]["quantity"], 3)
            self.assertEqual(a.get_summary(),{
                "order_id": "ORD100", "tier": "regular", "status": "PENDING", "item_count": 1,
                "subtotal": 25.0, "discount_amount": 0.0, "tax_amount": 2.0,
                "shipping_fee": 5.99, "final_total": 32.99,
                 "applied_coupon": None})

            a.remove_item("book", 1)
            self.assertEqual(a.items["book"]["quantity"], 2)
            self.assertEqual(a.get_summary(),{
                "order_id": "ORD100", "tier": "regular", "status": "PENDING", "item_count": 1,
                "subtotal": 20.0, "discount_amount": 0.0, "tax_amount": 1.6,
                "shipping_fee": 5.99, "final_total": 27.59,
                 "applied_coupon": None})

        #会员折扣、优惠卷使用
        def test_discounts(self):
            a=self.silver_order
            b=self.gold_order
            c=self.regular_order
            for order in [a, b, c]:
                order.add_item("book", 50.0, 2)
                self.assertEqual(order.subtotal, 100.0)
                self.assertEqual(order.shipping_fee, 0.0)
            
            self.assertEqual(a.discount_amount, 5.0)
            self.assertAlmostEqual(a.tax_amount, 7.6)
            self.assertAlmostEqual(a.final_total, 102.6)
                        
            self.assertEqual(b.discount_amount, 10.0)
            self.assertAlmostEqual(b.tax_amount, 7.2)
            self.assertAlmostEqual(b.final_total, 97.2)
    
            self.assertEqual(c.discount_amount, 0.0)
            self.assertAlmostEqual(c.tax_amount, 8.0)
            self.assertAlmostEqual(c.final_total, 108.0)
    
            b.apply_coupon("SAVE10")
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

            
        
        #邮费和税费计算
        def test_shipping_and_tax(self):
            a=self.regular_order
            a.add_item("book", 20.0, 2)
            self.assertEqual(a.subtotal, 40.0)
            self.assertAlmostEqual(a.tax_amount, 3.2)
            self.assertAlmostEqual(a.shipping_fee, 5.99)
            self.assertAlmostEqual(a.final_total, 49.19)
            self.assertEqual(a.subtotal, 50.0)
            self.assertAlmostEqual(a.tax_amount, 4.0)
            self.assertEqual(a.shipping_fee, 0.0)
            self.assertAlmostEqual(a.final_total, 54.0)

            a.add_item("apple", 10.0, 2, category="grocery")
            self.assertEqual(a.subtotal, 70.0)
            self.assertAlmostEqual(a.tax_amount, 4.0)
            self.assertEqual(a.shipping_fee, 0.0)
            self.assertAlmostEqual(a.final_total, 74.0)

        # 结账、取消，以及状态改变后不能修改订单
        def test_order_status(self):
            a=self.regular_order
            b=self.silver_order

            for order in[a, b]:
                order.add_item("book", 20.0, 2)

            a.checkout()
            self.assertEqual(a.status, "PAID")

            b.cancel()
            self.assertEqual(b.status, "CANCELLED")
            self.assertRaises(RuntimeError, a.cancel)

           
            for order in[a, b]:
                self.assertRaises(RuntimeError, order.add_item, "pen", 5.0)
                self.assertRaises(RuntimeError, order.remove_item, "book")
                self.assertRaises(RuntimeError, order.apply_coupon, "SAVE10")
                self.assertRaises(RuntimeError, order.checkout)
                self.assertEqual(order.items["book"]["quantity"], 2)
                self.assertEqual(order.subtotal, 40.0)

        # 测试异常
        def test_invalid_operations(self):
            a=self.regular_order

            self.assertRaises(ValueError, Order, "ORD400", "invalid")
            self.assertRaises(ValueError, a.checkout)

            for value in [0, -1]:
                self.assertRaises(ValueError, a.add_item, "book", value, 1)
                self.assertRaises(ValueError, a.add_item, "book", 20.0, value)

            self.assertRaises(KeyError, a.remove_item, "missing")
            self.assertRaises(ValueError, a.apply_coupon, "INVALID")

            a.add_item("book", 20.0, 2)

            for quantity in [0, -1]:
                self.assertRaises(ValueError, a.remove_item, "book", quantity)
            self.assertEqual(a.items["book"]["quantity"], 2)
            self.assertEqual(a.subtotal, 40.0)
            self.assertIsNone(a.applied_coupon)
        pass


if __name__ == "__main__":
    unittest.main()
