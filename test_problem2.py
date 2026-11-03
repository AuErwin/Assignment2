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
        self.assertEqual(self.account_empty.balance, 0.0)
        self.assertEqual(self.account_empty.owner, "Alice")
        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(self.account_empty.overdraft_limit, 100.0)
        self.assertEqual(len(self.account_empty.transaction_history), 0)
        self.assertEqual(self.account_empty.get_summary(), {
            "account_id": "ACC001", 
            "owner": "Alice",
            "balance": 0.0,
            "status": "ACTIVE",
            "overdraft_limit": 100.0,
            "transaction_count": 0
        })

        # 测试存款账户
        # TODO: 在此实现
        self.assertEqual(self.account_funded.balance, 200.0)
        self.assertEqual(self.account_funded.owner, "Bob")
        self.assertEqual(self.account_funded.status, "ACTIVE")
        self.assertEqual(self.account_funded.overdraft_limit, 50.0)
        self.assertEqual(len(self.account_funded.transaction_history), 1)
        self.assertEqual(self.account_funded.get_summary(), {
            "account_id": "ACC002",
            "owner": "Bob",
            "balance": 200.0,
            "status": "ACTIVE",
            "overdraft_limit": 50.0,
            "transaction_count": 1
        })

        pass

    def test_deposit_updates_multiple_attributes(self):
        """
        测试存款是否正确更新 balance、transaction_history 和 summary
        """
        # TODO: 实现测试：向 self.account_empty 中存入 $150
        a=self.account_empty
        self.assertTrue(a.deposit(150.0))
        self.assertEqual(a.balance, 150.0)
        self.assertEqual(a.transaction_history[-1], {
            "type": "DEPOSIT", "amount": 150.0, "fee": 0.0,
            "balance_after": 150.0, "description": "Deposit of $150.00",
        })
        self.assertEqual(a.get_summary(), {
            "account_id": "ACC001",
            "owner": "Alice",
            "balance": 150.0,           
            "status": "ACTIVE",
            "overdraft_limit": 100.0,
            "transaction_count": 1
        })
        pass

    def test_withdrawal_within_balance_multi_attributes(self):
        """
        测试当余额充足时提款是否正确
        """
        # TODO: 实现测试：从 self.account_funded 提取 $50，并附带 $2.50 手续费
        a=self.account_funded
        self.assertTrue(a.withdraw(50.0, fee=2.5))
        self.assertEqual(a.balance, 147.5)
        self.assertEqual(a.transaction_history[-1], {
            "type": "WITHDRAWAL", "amount": 50.0, "fee": 2.5,
            "balance_after": a.balance, "description": "Withdrawal of $50.00 (Fee: $2.50)"
        })
        self.assertEqual(a.get_summary(), {
            "account_id": "ACC002",
            "owner": "Bob",             
            "balance": 147.5,
            "status": "ACTIVE",
            "overdraft_limit": 50.0,
            "transaction_count": 2
        })
        pass

    def test_overdraft_withdrawal_and_status_transition(self):
        """
        测试使用透支保护的提款 (余额变为负数，但仍 >= -overdraft_limit)
        """
        # TODO: 实现测试：从 self.account_empty 提取 $50（当前余额为 0，透支上限为 100）
        a=self.account_empty
        self.assertTrue(a.withdraw(50.0))
        self.assertEqual(a.balance, -50.0)
        self.assertEqual(a.status, "OVERDRAWN")
        self.assertEqual(a.transaction_history[-1], {
            "type": "WITHDRAWAL", "amount": 50.0, "fee": 0.0,
            "balance_after": -50.0, "description": "Withdrawal of $50.00 (Fee: $0.00)"
        })
        self.assertEqual(a.get_summary(), {
            "account_id": "ACC001",
            "owner": "Alice",           
            "balance": -50.0,
            "status": "OVERDRAWN",
            "overdraft_limit": 100.0,
            "transaction_count": 1
        })

        pass

    def test_deposit_recovering_from_overdrawn_status(self):
        """
        测试当存款足以使余额 >= 0 时，状态从 OVERDRAWN 转回 ACTIVE。
        """
        # TODO: 实现测试
        a=self.account_empty
        self.assertTrue(a.withdraw(50.0))
        self.assertEqual(a.status, "OVERDRAWN")
        self.assertTrue(a.deposit(100.0))
        self.assertEqual(a.status, "ACTIVE")
        self.assertEqual(a.get_summary(), {
            "account_id": "ACC001",
            "owner": "Alice",
            "balance": 50.0,            
            "status": "ACTIVE",
            "overdraft_limit": 100.0,
            "transaction_count": 2
        })
        pass

    def test_transfer_between_accounts_multi_attributes(self):
        """
        测试两个账户之间的资金转账。
        """
        # TODO: 实现测试：从 account_funded 转账 $50 到 account_empty，并收取 $5 手续费
        a=self.account_funded
        b=self.account_empty
        self.assertTrue(a.transfer_to(b, 50.0, transfer_fee=5.0))
        self.assertEqual(a.balance, 145.0)  
        self.assertEqual(b.balance, 50.0)   
        self.assertEqual(a.transaction_history[-1], {
            "type": "WITHDRAWAL", "amount": 50.0, "fee": 5.0,
            "balance_after": 145.0, "description": "Withdrawal of $50.00 (Fee: $5.00)"
        })
        self.assertEqual(b.transaction_history[-1], {
            "type": "DEPOSIT", "amount": 50.0, "fee": 0.0,
            "balance_after": 50.0, "description": "Deposit of $50.00"
        })  
        self.assertEqual(a.get_summary(), {
            "account_id": "ACC002",
            "owner": "Bob",             
            "balance": 145.0,
            "status": "ACTIVE",
            "overdraft_limit": 50.0,
            "transaction_count": 2
        })
        self.assertEqual(b.get_summary(), {
            "account_id": "ACC001",
            "owner": "Alice",
            "balance": 50.0, 
            "status": "ACTIVE",
            "overdraft_limit": 100.0,
            "transaction_count": 1
        })     
        pass

    def test_frozen_account_restrictions(self):
        """
        测试 FROZEN 账户在存款、取款和转账时会抛出 RuntimeError。
        """
        # TODO: 实现测试：冻结账户并使用 self.assertRaises(RuntimeError) 验证异常
        a=self.account_empty
        a.freeze()
        self.assertEqual(a.status, "FROZEN")
        self.assertRaises(RuntimeError, a.deposit, 50.0)
        self.assertRaises(RuntimeError, a.withdraw, 50.0)
        b=self.account_funded
        self.assertRaises(RuntimeError, a.transfer_to, b, 50.0)
      
        pass

    def test_invalid_operations_raise_exceptions(self):
        """
        测试异常处理。
        """
        # TODO: 使用 self.assertRaises() 实现异常测试
        a=self.account_empty
        b=self.account_funded
        #测试存款为负数
        self.assertRaises(ValueError, a.deposit, -10.0)
        #测试取款为负数
        self.assertRaises(ValueError, a.withdraw, -20.0)
        #测试转账为负数
        self.assertRaises(ValueError, a.transfer_to, b, -30.0)
        #测试转账到不是 BankAccount
        self.assertRaises(TypeError, a.transfer_to, "not_a_bank_account", 10.0)
        #测试转账钱不够
        self.assertRaises(ValueError, a.transfer_to, b, 200.0)
        pass


if __name__ == "__main__":
    unittest.main()
