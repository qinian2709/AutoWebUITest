#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试结果分析工具
用于统计测试用例的执行情况
"""

import os
import re
import json
from typing import Dict, Tuple, Any


def analyze_pytest_output(output: str) -> Dict[str, int]:
    """
    分析pytest输出，提取测试结果统计
    
    Args:
        output: pytest命令的输出文本
        
    Returns:
        包含测试统计信息的字典
    """
    stats = {
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'error': 0,
        'total': 0
    }
    
    # 匹配pytest输出中的结果统计
    # 例如: "3 passed, 1 failed, 2 skipped in 10.5s"
    result_pattern = r'(\d+)\s+(passed|failed|skipped|error)'
    matches = re.findall(result_pattern, output, re.IGNORECASE)
    
    for count, status in matches:
        status_lower = status.lower()
        if status_lower in stats:
            stats[status_lower] = int(count)
    
    # 计算总数
    stats['total'] = sum(stats.values())
    
    return stats


def get_test_summary(stats: Dict[str, int]) -> str:
    """
    获取测试结果摘要
    
    Args:
        stats: 测试统计信息
        
    Returns:
        格式化的摘要字符串
    """
    if stats['total'] == 0:
        return "未找到测试用例"
    
    # 返回完整的统计信息
    summary = f"共计{stats['total']}个，成功{stats['passed']}个，失败{stats['failed']}个，错误{stats['error']}个，跳过{stats['skipped']}个"
    
    return summary


def analyze_test_results_from_file(result_file: str = "pytest_output.txt") -> Tuple[Dict[str, int], str]:
    """
    从文件分析测试结果
    
    Args:
        result_file: 包含pytest输出的文件路径
        
    Returns:
        (统计信息字典, 摘要字符串)
    """
    try:
        if os.path.exists(result_file):
            with open(result_file, 'r', encoding='utf-8') as f:
                output = f.read()
            
            stats = analyze_pytest_output(output)
            summary = get_test_summary(stats)
            return stats, summary
        else:
            return {'passed': 0, 'failed': 0, 'skipped': 0, 'error': 0, 'total': 0}, "未找到测试输出文件"
            
    except Exception as e:
        return {'passed': 0, 'failed': 0, 'skipped': 0, 'error': 0, 'total': 0}, f"分析失败: {str(e)}"


def get_test_result_data(stats: Dict[str, int], summary: str) -> Dict[str, Any]:
    """
    获取测试结果数据字典
    
    Args:
        stats: 测试统计信息
        summary: 测试摘要
        
    Returns:
        包含测试结果的数据字典
    """
    return {
        'stats': stats,
        'summary': summary
    }


def save_test_results(stats: Dict[str, int], summary: str, output_file: str = "test_results.json"):
    """
    保存测试结果到文件
    
    Args:
        stats: 测试统计信息
        summary: 测试摘要
        output_file: 输出文件路径
    """
    try:
        result_data = get_test_result_data(stats, summary)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 测试结果已保存到: {output_file}")
        
    except Exception as e:
        print(f"❌ 保存测试结果失败: {e}")


if __name__ == "__main__":
    # 测试代码
    test_output = """
    ============================= test session starts ==============================
    platform darwin -- Python 3.8.10, pytest-6.2.5, py-1.10.0, pluggy-0.13.1
    rootdir: /Users/qiukailiang/ws/TI_webUI
    plugins: allure-pytest-2.9.45, html-3.1.1, metadata-1.11.0
    collected 8 items
    
    tests/userpage/test_teacherin.py::TestTeacherIn::test_login_success PASSED    [ 12%]
    tests/userpage/test_teacherin.py::TestTeacherIn::test_login_failed FAILED     [ 25%]
    tests/userpage/test_teacherin.py::TestTeacherIn::test_navigation PASSED       [ 37%]
    tests/userpage/test_teacherin.py::TestTeacherIn::test_data_validation PASSED [ 50%]
    tests/userpage/test_teacherin.py::TestTeacherIn::test_form_submission SKIPPED [ 62%]
    tests/userpage/test_teacherin.py::TestTeacherIn::test_error_handling PASSED   [ 75%]
    tests/userpage/test_teacherin.py::TestTeacherIn::test_performance ERROR      [ 87%]
    tests/userpage/test_teacherin.py::TestTeacherIn::test_security PASSED        [100%]
    
    ============================= short test summary info ==========================
    FAILED tests/userpage/test_teacherin.py::TestTeacherIn::test_login_failed - AssertionError: assert 'Invalid credentials' in response
    ERROR tests/userpage/test_teacherin.py::TestTeacherIn::test_performance - TimeoutError: Test execution timeout
    ========================== 5 passed, 1 failed, 1 skipped, 1 error in 45.2s ==========================
    """
    
    stats = analyze_pytest_output(test_output)
    summary = get_test_summary(stats)
    
    print("测试结果分析:")
    print(f"统计信息: {stats}")
    print(f"摘要: {summary}")
    
    # 保存结果
    save_test_results(stats, summary) 