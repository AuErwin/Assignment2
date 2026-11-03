"""
问题 2单元测试: BankAccount

说明：
使用 Python 的 unittest 框架补全下面的测试方法。
你的测试方法必须断言 BankAccount 对象上的多个属性
（例如 balance、status、transaction_history、summary）以验证状态一致性。

运行测试：
    python -m unittest test_problem2.py -v
"""
import unittest
from problem2 import BankAccount


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        """
        Set up test fixtures before each test method.
        在每个测试方法执行前设置测试夹具（test fixtures）。
        """
        self.account_empty = BankAccount("ACC001", "Alice", initial_balance=0.0, overdraft_limit=100.0)
        self.account_funded = BankAccount("ACC002", "Bob", initial_balance=200.0, overdraft_limit=50.0)

    def test_initial_state_multi_attributes(self):
        """
        验证新创建的账户是否正确初始化所有属性。
        检查 balance、owner、status、overdraft_limit、transaction_history 和 summary。
        """
        # 测试空账户
        # TODO: 在此实现

        # 测试存款账户
        # TODO: 在此实现

        pass

    def test_deposit_updates_multiple_attributes(self):
        """
        测试存款是否正确更新 balance、transaction_history 和 summary
        """
        # TODO: 实现测试：向 self.account_empty 中存入 $150
        pass

    def test_withdrawal_within_balance_multi_attributes(self):
        """
        测试当余额充足时提款是否正确
        """
        # TODO: 实现测试：从 self.account_funded 提取 $50，并附带 $2.50 手续费
        pass

    def test_overdraft_withdrawal_and_status_transition(self):
        """
        测试使用透支保护的提款 (余额变为负数，但仍 >= -overdraft_limit)
        """
        # TODO: 实现测试：从 self.account_empty 提取 $50（当前余额为 0，透支上限为 100）
        pass

    def test_deposit_recovering_from_overdrawn_status(self):
        """
        测试当存款足以使余额 >= 0 时，状态从 OVERDRAWN 转回 ACTIVE。
        """
        # TODO: 实现测试
        pass

    def test_transfer_between_accounts_multi_attributes(self):
        """
        测试两个账户之间的资金转账。
        """
        # TODO: 实现测试：从 account_funded 转账 $50 到 account_empty，并收取 $5 手续费
        pass

    def test_frozen_account_restrictions(self):
        """
        测试 FROZEN 账户在存款、取款和转账时会抛出 RuntimeError。
        """
        # TODO: 实现测试：冻结账户并使用 self.assertRaises(RuntimeError) 验证异常
        pass

    def test_invalid_operations_raise_exceptions(self):
        """
        测试异常处理。
        """
        # TODO: 使用 self.assertRaises() 实现异常测试
        pass


if __name__ == "__main__":
    unittest.main()
