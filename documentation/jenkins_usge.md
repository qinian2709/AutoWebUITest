# Jenkins 自动化测试使用指南

## 概述

本项目支持在Jenkins CI/CD环境中自动执行测试用例并生成Allure报告。

## 🚀 快速开始

### 5分钟快速配置

1. **安装插件**：Pipeline, Allure Jenkins Plugin, Git plugin
2. **配置Allure**：Global Tool Configuration > Allure Commandline
3. **创建项目**：New Item > Pipeline > TI-WebUI-AutoTest
4. **配置Git**：Pipeline script from SCM > Git > 仓库URL
5. **指定分支**：Branch Specifier > `*/jenkins`
6. **脚本路径**：Script Path > `Jenkinsfile`
7. **立即构建**：Build Now

### 验证成功标志
- ✅ Git代码检出成功
- ✅ Python环境创建成功
- ✅ 依赖安装成功
- ✅ 测试执行通过
- ✅ Allure报告生成成功

## 执行方式

### 1. 本地执行（开发环境）

```bash
# 基本执行
python run_tests.py --env test --test-file tests --allure

# 指定浏览器
python run_tests.py --env test --browser chromium --test-file tests --allure

# 并行执行
python run_tests.py --env test --test-file tests --allure --parallel
```

**本地执行特点：**
- ✅ 自动生成Allure报告
- ✅ 启动本地Allure服务器（http://localhost:8080）
- ✅ 适合开发和调试

### 2. Jenkins执行（CI环境）

```bash
# Jenkins中使用的命令
python run_tests.py --env test --test-file tests --allure --ci
```

**Jenkins执行特点：**
- ✅ 只生成Allure结果文件
- ✅ 由Jenkins自动生成和发布Allure报告
- ✅ 适合持续集成环境

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--env` | 测试环境 | `dev`, `test`, `prod` |
| `--browser` | 浏览器类型 | `chromium`, `firefox`, `webkit` |
| `--test-file` | 测试文件路径 | `tests`, `tests/userpage/` |
| `--allure` | 生成Allure报告 | 无值 |
| `--ci` | CI环境执行 | 无值 |
| `--parallel` | 并行执行 | 无值 |
| `--headless` | 无头模式 | 无值 |

## Jenkins配置

### 1. 前置准备

#### 1.1 安装必要的Jenkins插件
在Jenkins管理页面 (`Manage Jenkins` > `Manage Plugins`) 安装以下插件：

**必需插件：**
- ✅ **Pipeline** - 核心Pipeline支持
- ✅ **Allure Jenkins Plugin** - Allure报告集成
- ✅ **Git plugin** - Git集成
- ✅ **Workspace Cleanup Plugin** - 工作空间清理
- ✅ **Pipeline Utility Steps** - Pipeline工具步骤

**可选插件：**
- ✅ **Email Extension Plugin** - 邮件通知
- ✅ **Blue Ocean** - 现代化Pipeline界面
- ✅ **Timestamper** - 时间戳显示

#### 1.2 配置Allure工具
1. 进入 `Manage Jenkins` > `Global Tool Configuration`
2. 找到 **Allure Commandline** 部分
3. 点击 **Add Allure Commandline**
4. 配置：
   - **Name**: `Allure`
   - **Install automatically**: 勾选
   - **Version**: 选择最新版本（如 `2.24.1`）
5. 点击 **Save**

### 2. 创建Jenkins Pipeline项目

#### 2.1 创建新项目
1. 登录Jenkins，点击 **"新建任务"** 或 **"New Item"**
2. 输入项目名称：`TI-WebUI-AutoTest`
3. 选择 **"Pipeline"** 类型
4. 点击 **"确定"** 或 **"OK"**

#### 2.2 配置Pipeline
在项目配置页面中找到 **"Pipeline"** 部分，按以下设置：

1. **Definition**: 选择 **"Pipeline script from SCM"**
2. **SCM**: 选择 **"Git"**
3. **Repository URL**: 输入您的Git仓库URL
   ```
   https://gl.eeo.im/ti_test/ti_webui.git
   ```
4. **Credentials**: 如果使用私有仓库，添加Git凭据
5. **Branch Specifier**: 输入分支名称
   - 主分支：`*/main` 或 `*/master`
   - 开发分支：`*/develop`
   - 当前分支：`*/jenkins`
   - 所有分支：`*/**`
6. **Script Path**: 输入 `Jenkinsfile`
7. **Lightweight checkout**: 建议勾选（提高检出速度）

#### 2.3 配置构建触发器（可选）
在 **"构建触发器"** 部分：

1. **Poll SCM**: 定期检查代码变更
   - 输入Cron表达式：`H/15 * * * *` （每15分钟检查一次）

2. **Build periodically**: 定时构建
   - 输入Cron表达式：`0 2 * * *` （每天凌晨2点构建）

#### 2.4 保存配置
点击页面底部的 **"保存"** 或 **"Save"** 按钮

### 3. 验证配置

#### 3.1 检查Jenkinsfile是否被识别
1. 保存配置后，回到项目页面
2. 点击 **"立即构建"** 或 **"Build Now"**
3. 查看构建日志，确认Jenkinsfile被正确读取

#### 3.2 检查Git检出
在构建日志中应该看到：
```
[Pipeline] checkout
Cloning the remote Git repository
Cloning repository https://gl.eeo.im/ti_test/ti_webui.git
```

### 4. 常见问题解决

#### 4.1 Git凭据问题
如果遇到Git认证问题：
1. 在Jenkins管理页面：`Manage Jenkins` > `Manage Credentials`
2. 添加新的凭据：
   - Kind: `Username with password` 或 `SSH Username with private key`
   - Scope: `Global`
   - 输入用户名和密码或SSH私钥

#### 4.2 分支不存在问题
如果指定的分支不存在：
1. 检查分支名称是否正确
2. 使用 `*/**` 匹配所有分支
3. 或者使用具体的分支名如 `*/jenkins`

#### 4.3 Jenkinsfile路径问题
如果Jenkins找不到Jenkinsfile：
1. 确认Jenkinsfile在项目根目录
2. 检查文件名大小写（必须是`Jenkinsfile`）
3. 确认文件已提交到Git仓库

### 5. Pipeline配置说明

Jenkinsfile已配置好，支持：
- ✅ 自动检出Git代码
- ✅ Python环境设置
- ✅ 依赖安装
- ✅ Playwright浏览器安装
- ✅ 测试执行
- ✅ Allure报告发布

### 6. 构建命令

Jenkins中使用的完整命令：
```bash
python run_tests.py --env test --test-file tests --allure --ci
```

### 7. 环境变量

Jenkins Pipeline中设置的环境变量：
- `ENV=test` - 测试环境
- `BROWSER=chromium` - 浏览器类型
- `HEADLESS=true` - 无头模式
- `PYTHONPATH=${WORKSPACE}` - Python路径

## 报告查看

### 本地报告
- 地址：http://localhost:8080
- 启动：执行本地命令后自动启动

### Jenkins报告
- 位置：Jenkins构建页面
- 查看：点击"Allure Report"链接

## 高级配置

### 1. 邮件通知配置

#### 1.1 配置邮件服务器
1. 进入 `Manage Jenkins` > `Configure System`
2. 找到 **Extended E-mail Notification** 部分
3. 配置SMTP服务器信息：
   - **SMTP server**: `smtp.gmail.com`
   - **SMTP Port**: `587`
   - **Credentials**: 添加邮箱凭据
   - **Default Recipients**: `your-email@example.com`

#### 1.2 在Pipeline中添加邮件通知
在Jenkinsfile的post部分添加：

```groovy
post {
    always {
        // 现有代码...
    }
    
    success {
        emailext (
            subject: "✅ 构建成功: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body: """
                <h2>构建成功</h2>
                <p><strong>项目:</strong> ${env.JOB_NAME}</p>
                <p><strong>构建号:</strong> ${env.BUILD_NUMBER}</p>
                <p><strong>构建时间:</strong> ${new Date().format("yyyy-MM-dd HH:mm:ss")}</p>
                <p><a href="${env.BUILD_URL}">查看构建详情</a></p>
                <p><a href="${env.BUILD_URL}allure/">查看Allure报告</a></p>
            """,
            to: 'your-email@example.com',
            mimeType: 'text/html'
        )
    }
    
    failure {
        emailext (
            subject: "❌ 构建失败: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body: """
                <h2>构建失败</h2>
                <p><strong>项目:</strong> ${env.JOB_NAME}</p>
                <p><strong>构建号:</strong> ${env.BUILD_NUMBER}</p>
                <p><strong>构建时间:</strong> ${new Date().format("yyyy-MM-dd HH:mm:ss")}</p>
                <p><a href="${env.BUILD_URL}">查看构建详情</a></p>
            """,
            to: 'your-email@example.com',
            mimeType: 'text/html'
        )
    }
}
```

### 2. 多环境支持

如果需要支持多个环境，可以修改Jenkinsfile：

```groovy
pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'test', 'prod'],
            description: '选择测试环境'
        )
        choice(
            name: 'BROWSER',
            choices: ['chromium', 'firefox', 'webkit'],
            description: '选择浏览器'
        )
    }
    
    environment {
        ENV = "${params.ENVIRONMENT}"
        BROWSER = "${params.BROWSER}"
        HEADLESS = 'true'
        PYTHONPATH = "${WORKSPACE}"
        PYTHONUNBUFFERED = '1'
    }
    
    // ... 其余Pipeline内容
}
```

### 3. 并行测试执行

```groovy
stage('Run Tests') {
    parallel {
        stage('Chrome Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    python run_tests.py --env test --browser chromium --allure --ci
                '''
            }
        }
        stage('Firefox Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    python run_tests.py --env test --browser firefox --allure --ci
                '''
            }
        }
    }
}
```

## 监控和维护

### 1. 构建监控

#### 1.1 查看构建历史
- 进入项目页面查看构建历史
- 点击构建号查看详细日志
- 查看Allure报告链接

#### 1.2 构建趋势
- 查看构建成功/失败趋势
- 监控测试执行时间
- 关注测试通过率

### 2. 日志分析

#### 2.1 常见日志信息
```
✅ Git代码检出完成
✅ Python虚拟环境创建完成
✅ Python依赖安装完成
✅ Playwright浏览器安装完成
✅ 测试执行完成
✅ Allure报告发布成功
```

#### 2.2 错误日志分析
- Python环境问题：检查Python版本和路径
- 依赖安装失败：检查网络连接和requirements.txt
- 浏览器安装失败：检查系统权限
- Allure报告失败：检查Allure工具配置

## 故障排除

### 1. Python环境问题
```bash
# 检查Python版本
python3 --version

# 检查pip版本
python3 -m pip --version

# 检查Python路径
which python3
```

### 2. Allure安装问题
```bash
# macOS
brew install allure

# Windows
scoop install allure

# Linux
# 参考 https://docs.qameta.io/allure/#_installing_a_commandline

# 验证安装
allure --version
```

### 3. Playwright浏览器问题
```bash
# 安装浏览器
python -m playwright install chromium

# 安装系统依赖
python -m playwright install-deps

# 验证安装
python -m playwright --version
```

### 4. Jenkins常见问题

#### 4.1 内存不足
在Jenkins节点配置中增加JVM参数：
```
-Xmx4g -Xms2g
```

#### 4.2 权限问题
```bash
# 给Jenkins用户添加执行权限
chmod +x venv/bin/activate
chmod +x venv/bin/python
```

#### 4.3 网络问题
- 检查Jenkins服务器网络连接
- 配置代理设置（如需要）
- 检查防火墙设置

## 最佳实践

1. **本地开发**：使用 `--allure` 参数，不使用 `--ci`
2. **Jenkins构建**：使用 `--allure --ci` 参数
3. **环境隔离**：使用虚拟环境避免依赖冲突
4. **报告管理**：定期清理旧的测试报告

## 联系支持

如有问题，请联系开发团队或查看项目文档。 