# 问题/错误报告 Bug Report

该报告记录了在有错误程序中发现的问题（bugs），包括失败的测试用例、根本原因分析（root cause analysis）以及已应用的修复方案。

---

## 问题/错误报告 1：（示例）

### 1. 测试程序 Program Under Test
- **File:** `problemX.py`
- **Class / Function:** `YourClassName.method_name()`

### 2. 失败的测试用例 Failing Test Case
提供来自 `test_problemX.py` 的单元测试代码，用于暴露该缺问题/错误并在执行过程中失败：

```python
# 在此粘贴失败的测试方法
def test_example_failure(self):
    pass
```

提供从 VS Code 中捕获的测试运行结果。

![alt text](assets/example_test_runs.png)

**测试输出 / 错误信息：**
```text
# 在此粘贴错误追踪 / 断言失败信息（error traceback / assertion failure message）
```

### 3. 根本原因分析 Root Cause Analysis
说明该问题/错误（bug）为何会发生，以及它导致了什么错误行为：
- **预期行为：**（根据规范应发生什么）
- **实际行为：**（起始代码中实际发生了什么）
- **根本原因：**（对代码逻辑中问题/错误的解释）

### 4. 代码修复与差异 Code Fix & Diff
展示对 `problemX.py` 进行修复所做的修改：

```diff
- # Original buggy code line
+ # Corrected code line
```

---

## 问题/错误报告 2：（你的发现）

按上述方式记录你发现的问题/错误及其解决方案。必要时可以添加更多问题报告。