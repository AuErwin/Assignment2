"""
问题 4 单元测试: MeetingRoom

说明：
使用 Python 的 unittest 框架补全下面的单元测试方法。
你的测试方法必须断言 MeetingRoom 对象上的多个属性
（例如 bookings 列表、total_hours_booked、free slots、utilization rate）
以验证会议室状态和冲突管理。

运行测试：
    python -m unittest test_problem4.py -v
"""
import unittest
from problem4 import MeetingRoom


class TestMeetingRoom(unittest.TestCase):

    def setUp(self):
        """
        在每个测试方法执行前设置测试夹具。
        """
        self.room = MeetingRoom("Conference-A", capacity=10)

    def test_initial_state_multi_attributes(self):
        """
        验证空会议室的初始状态。
        """
        # TODO: 验证 room_id、capacity、bookings、total_hours_booked、is_maintenance
        r=self.room
        self.assertEqual(r.room_id, "Conference-A")
        self.assertEqual(r.capacity, 10)
        self.assertEqual(r.bookings, [])
        self.assertEqual(r.total_hours_booked, 0)
        self.assertFalse(r.is_maintenance)
        self.assertEqual(r.get_free_slots(), [(8, 18)])
        self.assertEqual(r.get_utilization_rate(), 0.0)

        pass

    def test_single_booking_multi_attributes(self):
        """
        测试创建一个有效预订。
        验证 bookings 列表、total_hours_booked、utilization rate 和 free slots。
        """
        # TODO: 预订会议 'B01'，时间为 10 到 12，参与人数为 5
        r=self.room
        self.assertTrue(r.book("B01", "Planning", 10, 12, 5))
        self.assertEqual(r.bookings, [{
            "booking_id": "B01", "title": "Planning", "start_time": 10,
            "end_time": 12, "attendees": 5,
        }])
        self.assertEqual(r.total_hours_booked, 2)
        self.assertAlmostEqual(r.get_utilization_rate(), 0.2)
        self.assertEqual(r.get_free_slots(), [(8, 10), (12, 18)])
        self.assertEqual(r.get_free_slots(11, 13), [(12, 13)])
        self.assertFalse(r.is_maintenance)
        pass

    def test_back_to_back_meetings_allowed(self):
        """
        测试有效的连续/背靠背会议 (例如 9-10 和 10-12) 不会引发冲突错误。
        验证两个预订成功后的多属性状态。
        """
        # TODO: 预订 'B01'，时间为 9 到 10
        r=self.room
        self.assertTrue(r.book("B01", "r1", 9, 10, 5))
        self.assertTrue(r.book("B02", "r2", 10, 12, 5))
        self.assertTrue(r.book("B00", "r3", 8, 9, 10))
        self.assertEqual([b["booking_id"] for b in r.bookings], ["B00", "B01", "B02"])
        self.assertEqual(r.total_hours_booked, 4)
        self.assertAlmostEqual(r.get_utilization_rate(), 0.4)
        self.assertEqual(r.get_free_slots(), [(12, 18)])
        pass

    def test_overlapping_booking_rejected(self):
        """
        测试重叠预订（例如 9-11 与 10-12, 或完全包含在 9-12 与 10-11 之间）
        应抛出 ValueError, 并保持会议室状态不变。
        """
        # TODO: 使用 self.assertRaises(ValueError) 实现测试
        r = self.room
        r.book("B01", "M1", 9, 12, 5)
        for start, end in [(10, 13), (10, 11), (8, 13)]:
            with self.assertRaises(ValueError):
                r.book("B02", "Overlap", start, end, 5)

            self.assertEqual(
                [b["booking_id"] for b in r.bookings],
                ["B01"]
            )
            self.assertEqual(r.total_hours_booked, 3)
            self.assertAlmostEqual(r.get_utilization_rate(), 0.3)
            self.assertEqual(
                r.get_free_slots(),
                [(8, 9), (12, 18)]
            )
        pass

    def test_cancel_booking_updates_all_attributes(self):
        """
        测试取消预订是否能正确从 bookings 中移除，
        减少 total_hours_booked, 并恢复 free slots。
        """
        # TODO: 预订两场会议，取消其中一场，并验证所有属性
        r=self.room
        r = self.room
        r.book("B01", "M1", 9, 11, 5)
        r.book("B02", "M2", 13, 14, 5)

        self.assertEqual(r.total_hours_booked, 3)
        self.assertTrue(r.cancel("B01"))
        self.assertEqual(
            [b["booking_id"] for b in r.bookings],
            ["B02"]
        )
        self.assertEqual(r.total_hours_booked, 1)
        self.assertAlmostEqual(r.get_utilization_rate(), 0.1)
        self.assertEqual(
            r.get_free_slots(),
            [(8, 13), (14, 18)]
        )
        self.assertTrue(r.cancel("B02"))
        self.assertEqual(r.bookings, [])
        self.assertEqual(r.total_hours_booked, 0)
        self.assertEqual(r.get_utilization_rate(), 0.0)
        self.assertEqual(r.get_free_slots(), [(8, 18)])
        pass

    def test_capacity_and_validation_exceptions(self):
        """
        测试边界情况和异常：
        - 参与人数超过容量 (ValueError)
        - 开始时间 >= 结束时间 (ValueError)
        - 预订 ID 重复 (ValueError)
        - 会议室处于维护状态时预订 (RuntimeError)
        - 取消不存在的预订 (KeyError)
        """
        # TODO: 使用 self.assertRaises() 实现异常测试
        r=self.room
        for capacity in (0, -1):
            with self.subTest(capacity=capacity), self.assertRaises(ValueError):
                MeetingRoom("BAD", capacity)
        self.assertTrue(r.book("B01", "Valid", 9, 10, 10))
        for start, end in [(-1, 1), (11, 11), (12, 11)]:
            with self.assertRaises(ValueError):
                r.book("B02", "Invalid time", start, end, 5)
        for attendees in [0, -1, 11]:
            with self.assertRaises(ValueError):
                r.book("B02", "Invalid attendees", 11, 12, attendees)
        with self.assertRaises(ValueError):
            r.book("B01", "Duplicate", 11, 12, 5)
        r.is_maintenance = True

        with self.assertRaises(RuntimeError):
            r.book("B02", "Maintenance", 13, 14, 5)

        self.assertTrue(r.is_maintenance)

        with self.assertRaises(KeyError):
            r.cancel("MISSING")

        self.assertRaises(ValueError, r.get_free_slots, 18, 8)
        self.assertRaises(ValueError, r.get_free_slots, 8, 8)

        for hours in [0, -1]:
            self.assertRaises(ValueError, r.get_utilization_rate, hours)

        self.assertEqual(
            [b["booking_id"] for b in r.bookings],
            ["B01"]
        )
        self.assertEqual(r.total_hours_booked, 1)
        self.assertAlmostEqual(r.get_utilization_rate(), 0.1)
        self.assertEqual(r.get_free_slots(), [(8, 9), (10, 18)])
        pass


if __name__ == "__main__":
    unittest.main()
