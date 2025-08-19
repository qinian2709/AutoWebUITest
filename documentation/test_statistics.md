# 测试结果统计功能

## 概述

新增了测试用例执行结果统计功能，可以自动分析pytest输出并生成统计报告，包含成功、失败、错误、跳过等测试用例数量。

## 功能特性

### 1. 统计指标
- **总计 (total)**: 所有测试用例总数
- **成功 (passed)**: 测试通过的用例数
- **失败 (failed)**: 测试失败的用例数  
- **错误 (error)**: 执行错误的用例数
- **跳过 (skipped)**: 被跳过的用例数

### 2. 输出格式
```
共计8个，成功5个，失败1个，错误1个，跳过1个
```

## 实现架构

### 1. 核心工具 (`utils/test_result_analyzer.py`)
- `analyze_pytest_output()`: 分析pytest输出，提取统计信息
- `get_test_summary()`: 生成格式化的统计摘要
- `save_test_results()`: 保存结果到JSON文件

### 2. 测试执行集成 (`run_tests.py`)
- 修改了`run_command()`函数，返回pytest输出
- 在测试执行后自动分析结果
- 将统计结果以JSON格式输出到控制台，供Jenkins直接读取

### 3. Jenkins集成 (`Jenkinsfile`)
- 在"Run Tests"阶段捕获测试输出
- 从输出中提取JSON格式的测试结果
- 设置环境变量`TEST_SUMMARY`和`TEST_STATS`
- 在企微通知中包含测试结果统计

## 使用流程

### 1. 测试执行
```bash
python run_tests.py --env test --browser chromium --allure --ci
```

### 2. 控制台输出
- pytest的完整输出（在控制台显示）
- JSON格式的测试结果统计（供Jenkins提取）

### 3. Jenkins处理
```groovy
// 从输出中提取测试结果JSON
def testResultMatch = testOutput =~ /TEST_RESULT_JSON: (.+)/
if (testResultMatch) {
    def testResultJson = testResultMatch[0][1]
    def slurper = new groovy.json.JsonSlurper()
    def testResults = slurper.parseText(testResultJson)
    
    // 直接输出所有测试数据
    echo "📊 测试结果统计: ${testResults.summary}"
    echo "📈 详细统计:"
    echo "  - 总计: ${testResults.stats.total}"
    echo "  - 成功: ${testResults.stats.passed}"
    echo "  - 失败: ${testResults.stats.failed}"
    echo "  - 错误: ${testResults.stats.error}"
    echo "  - 跳过: ${testResults.stats.skipped}"
    
    // 设置环境变量
    env.TEST_SUMMARY = testResults.summary
    env.TEST_STATS = testResults.stats.toString()
    env.TEST_TOTAL = testResults.stats.total.toString()
    env.TEST_PASSED = testResults.stats.passed.toString()
    env.TEST_FAILED = testResults.stats.failed.toString()
    env.TEST_ERROR = testResults.stats.error.toString()
    env.TEST_SKIPPED = testResults.stats.skipped.toString()
}
```

### 4. 企微通知
```
### 【TI_WebUI_Test】构建通知
> **状态**: <font color="green">构建成功 ✅</font>
> **测试结果**: 共计8个，成功5个，失败1个，错误1个，跳过1个
> **环境**: test
> **浏览器**: chromium
...
```

## 文件结构

```
utils/
├── test_result_analyzer.py    # 测试结果分析工具
└── send_wechat_notice.py      # 企微通知工具

Jenkinsfile                     # Jenkins流水线配置
run_tests.py                    # 测试执行脚本
```

## 示例输出

### 成功场景
```
📊 测试结果统计: 共计10个，成功10个，失败0个，错误0个，跳过0个
📈 详细统计:
  - 总计: 10
  - 成功: 10
  - 失败: 0
  - 错误: 0
  - 跳过: 0
```

### 失败场景
```
📊 测试结果统计: 共计8个，成功5个，失败1个，错误1个，跳过1个
📈 详细统计:
  - 总计: 8
  - 成功: 5
  - 失败: 1
  - 错误: 1
  - 跳过: 1
```

## 注意事项

1. 测试结果分析依赖于pytest的标准输出格式
2. 统计结果会以JSON格式输出到控制台，供Jenkins直接提取
3. 企微通知会自动包含测试结果统计信息
4. 如果分析失败，会显示"分析失败"作为默认值
5. 完全无文件生成，所有数据都在内存中处理 