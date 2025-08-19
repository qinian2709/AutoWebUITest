#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import argparse
from datetime import datetime

def run_command(command, description, check=False, env=None):
    """运行命令"""
    print(f"\n{'='*50}")
    print(f"执行: {description}")
    print(f"命令: {command}")
    print(f"{'='*50}")
    
    try:
        # 使用list形式而不是shell=True
        if isinstance(command, str):
            # 如果是字符串，转换为列表
            if command.startswith("pytest"):
                # 对于pytest命令，特殊处理
                cmd_parts = command.split()
            else:
                cmd_parts = command.split()
        else:
            cmd_parts = command
        
        print(f"调试: 执行命令列表: {cmd_parts}")
        
        result = subprocess.run(cmd_parts, check=check, capture_output=True, text=True, env=env)
        print("✅ 执行成功")
        if result.stdout:
            print("输出:", result.stdout)
        if result.stderr:
            print("错误输出:", result.stderr)
        return True, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print("❌ 执行失败")
        print("错误:", e.stderr)
        return False, e.stdout, e.stderr

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="TI-WebUI自动化测试 - 支持多环境")
    parser.add_argument("--env", choices=["dev", "test", "prod"], 
                       default="test", help="测试环境")
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], 
                       default="chromium", help="浏览器类型")
    parser.add_argument("--headless", action="store_true", help="无头模式")
    parser.add_argument("--markers", help="测试标记")
    parser.add_argument("--test-file", help="测试文件")
    parser.add_argument("--test-function", help="测试函数")
    parser.add_argument("--parallel", action="store_true", help="并行运行")
    parser.add_argument("--allure", action="store_true", help="生成Allure报告")
    parser.add_argument("--install-browsers", action="store_true", help="安装浏览器")
    parser.add_argument("--ci", action="store_true", help="CI环境执行（Jenkins等）")
    
    args = parser.parse_args()
    
    print("🚀 WebUI自动化测试运行器 - 多环境支持")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"环境: {args.env}")
    
    # 设置环境变量
    env_vars = os.environ.copy()
    env_vars["ENV"] = args.env
    env_vars["BROWSER"] = args.browser
    env_vars["HEADLESS"] = str(args.headless).lower()
    
    # 安装浏览器
    if args.install_browsers:
        print("\n📦 安装Playwright浏览器...")
        if not run_command("playwright install", "安装Playwright浏览器", env=env_vars):
            return 1
    
    # 构建pytest命令
    pytest_cmd = ["pytest"]
    
    if args.test_file:
        if args.test_function:
            # 当指定测试函数时，让pytest自动查找，不指定类名
            pytest_cmd.append(f"{args.test_file}::{args.test_function}")
        else:
            pytest_cmd.append(args.test_file)
    else:
        pytest_cmd.append("tests/")
    
    if args.markers:
        pytest_cmd.extend(["-m", args.markers])
    
    if args.parallel:
        pytest_cmd.extend(["-n", "auto"])
    
    # 清除之前的测试数据（在测试执行前）
    if args.allure:
        print("\n🧹 清除之前的测试数据...")
        import shutil
        import pathlib
        
        allure_results_dir = f"./reports/{args.env}/allure-results"
        allure_report_dir = f"./reports/{args.env}/allure-report"
        
        # 清除Allure结果目录
        if os.path.exists(allure_results_dir):
            shutil.rmtree(allure_results_dir)
            print(f"✅ 已清除Allure结果目录: {allure_results_dir}")
        
        # 清除Allure报告目录
        if os.path.exists(allure_report_dir):
            shutil.rmtree(allure_report_dir)
            print(f"✅ 已清除Allure报告目录: {allure_report_dir}")
        
        # 清除旧视频文件（可选）
        videos_dir = f"./reports/{args.env}/videos"
        if os.path.exists(videos_dir):
            try:
                from utils.video_manager import VideoManager
                video_manager = VideoManager()
                video_manager.cleanup_old_videos(max_age_hours=1)  # 清理1小时前的视频
                print(f"✅ 已清理旧视频文件: {videos_dir}")
            except Exception as e:
                print(f"⚠️ 清理视频文件失败: {e}")
        
        # 确保目录存在
        pathlib.Path(allure_results_dir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(allure_report_dir).mkdir(parents=True, exist_ok=True)
    
    # 构建pytest命令
    if args.allure:
        # 使用环境特定的报告路径
        allure_results_dir = f"./reports/{args.env}/allure-results"
        pytest_cmd.extend([f"--alluredir={allure_results_dir}"])
    
    # 运行测试 - 不检查返回值，确保即使测试失败也能继续执行
    test_success, test_stdout, test_stderr = run_command(pytest_cmd, "运行测试", check=False, env=env_vars)
    
    # 合并pytest输出
    pytest_output = test_stdout + "\n" + test_stderr if test_stderr else test_stdout
    
    # 分析测试结果
    try:
        from utils.test_result_analyzer import analyze_pytest_output, get_test_summary, get_test_result_data
        
        stats = analyze_pytest_output(pytest_output)
        summary = get_test_summary(stats)
        
        print(f"\n📊 测试结果统计:")
        print(f"📈 {summary}")
        
        # 将结果输出为JSON格式，供Jenkins读取
        result_data = get_test_result_data(stats, summary)
        import json
        print(f"TEST_RESULT_JSON: {json.dumps(result_data, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"⚠️ 测试结果分析失败: {e}")
        # 创建默认结果
        stats = {"passed": 0, "failed": 0, "skipped": 0, "error": 0, "total": 0}
        summary = "分析失败"
        result_data = {"stats": stats, "summary": summary}
        import json
        print(f"TEST_RESULT_JSON: {json.dumps(result_data, ensure_ascii=False)}")
    
    # 生成Allure报告 - 根据环境选择处理方式
    if args.allure:
        allure_results_dir = f"./reports/{args.env}/allure-results"
        
        if args.ci:
            # CI环境（Jenkins等）- 只生成结果，不生成报告
            print("\n📊 Allure结果已生成，报告将由Jenkins处理...")
            allure_results_dir = f"./reports/{args.env}/allure-results"
            print(f"📁 Allure结果目录: {allure_results_dir}")
            print("✅ 测试结果已准备就绪，Jenkins将自动生成Allure报告")

        else:
            # 本地环境 - 生成报告并启动服务器
            print("\n📊 生成Allure报告...")
            allure_report_dir = f"./reports/{args.env}/allure-report"
            
            allure_success = run_command(f"allure generate {allure_results_dir} -o {allure_report_dir} --clean", 
                                    "生成Allure报告", check=False, env=env_vars)
            
            if allure_success:
                print("\n🌐 启动Allure报告服务器...，按 Ctrl+C 停止服务器")
                run_command(f"allure serve {allure_results_dir}", "启动Allure报告服务器", check=False, env=env_vars)
            else:
                print("⚠️ Allure报告生成失败，请检查是否安装了Allure命令行工具")
    
    # 根据测试结果返回不同的退出码
    if test_success:
        print("\n✅ 测试运行完成!")
        return 0
    else:
        print("\n⚠️ 测试运行完成，但有测试失败!")
        return 1

if __name__ == "__main__":
    '''
    使用方法：
    cd TI_WEBUI
    python run_tests.py --env test --browser chromium --headless --allure 
    
    
    '''
    sys.exit(main()) 
   