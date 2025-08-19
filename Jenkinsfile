pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['test', 'dev', 'prod'],
            description: '选择测试环境'
        )
        choice(
            name: 'BROWSER_TYPE',
            choices: ['chromium', 'firefox', 'webkit'],
            description: '选择浏览器类型'
        )
        booleanParam(
            name: 'HEADLESS_MODE',
            description: '是否使用无头模式',
            defaultValue: true
        )
    }
    
    environment {
        ENV = "${params.ENVIRONMENT}"
        BROWSER = "${params.BROWSER_TYPE}"
        HEADLESS = "${params.HEADLESS_MODE}"
        PYTHONPATH = "${WORKSPACE}"
        PYTHONUNBUFFERED = '1'
        DISPLAY = ':99'
    }
    
    stages {
        stage('Checkout Git Repository') {
            steps {
                script {
                    def gitBranch = sh(
                        script: 'git name-rev --name-only HEAD',
                        returnStdout: true
                    ).trim()
                    
                    // 如果返回的是完整路径，提取分支名
                    if (gitBranch.startsWith('remotes/origin/')) {
                        gitBranch = gitBranch.replace('remotes/origin/', '')
                    } else if (gitBranch.startsWith('origin/')) {
                        gitBranch = gitBranch.replace('origin/', '')
                    } else if (gitBranch == 'HEAD') {
                        gitBranch = sh(
                            script: 'git branch -r --contains HEAD | grep -v HEAD | head -1 | sed "s/origin\\///"',
                            returnStdout: true
                        ).trim()
                        
                        if (!gitBranch || gitBranch == '') {
                            gitBranch = env.GIT_BRANCH ?: env.BRANCH_NAME ?: 'unknown'
                        }
                    }
                    def gitCommit = sh(
                        script: 'git rev-parse HEAD',
                        returnStdout: true
                    ).trim()
                    def gitShortCommit = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    
                    echo "🌿 当前Git分支: ${gitBranch}"
                    echo "🔗 完整提交: ${gitCommit}"
                    echo "🔗 短提交: ${gitShortCommit}"
                    
                    sh '''
                        echo "📋 Git仓库信息:"
                        git remote -v
                        git log --oneline -5
                        echo "📍 当前分支: $(git name-rev --name-only HEAD)"
                        echo "🔗 当前提交: $(git rev-parse HEAD)"
                    '''
                    
                    env.GIT_BRANCH_NAME = gitBranch
                    env.GIT_COMMIT_FULL = gitCommit
                    env.GIT_COMMIT_SHORT = gitShortCommit
                    
                    echo "✅ Git代码检出完成"
                }
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    def pythonCmd = "/usr/local/src/python38/bin/python3.8"
                    env.PYTHON_CMD = pythonCmd
                    
                    echo "🐍 使用Python命令: ${pythonCmd}"
                    sh "${pythonCmd} --version"
                    sh "${pythonCmd} -m pip --version"
                    sh "${pythonCmd} -m venv venv"
                    echo "✅ Python虚拟环境创建完成"
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    sh '''
                        . venv/bin/activate
                        
                        python -m pip install --upgrade pip
                        python -m pip install -r requirements.txt
                        
                        # 创建Playwright浏览器安装目录（在虚拟环境内）
                        mkdir -p .venv/playwright_browsers
                        export PLAYWRIGHT_BROWSERS_PATH=.venv/playwright_browsers
                        
                        playwright install ${BROWSER}
                    '''
                    echo "✅ Python、浏览器依赖安装完成"
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    echo "🚀 开始执行测试"
                    echo "📋 分支: ${env.GIT_BRANCH_NAME}"
                    echo "🔗 完整提交: ${env.GIT_COMMIT_FULL}"
                    echo "🌍 环境: ${params.ENVIRONMENT}"
                    echo "🌐 浏览器: ${params.BROWSER_TYPE}"
                    echo "👻 无头模式: ${params.HEADLESS_MODE}"
                    
                    def testOutput = sh(
                        script: '''
                            . venv/bin/activate
                            # 确保测试执行时，Playwright能找到指定路径的浏览器
                            export PLAYWRIGHT_BROWSERS_PATH=.venv/playwright_browsers
                            python run_tests.py --env ${ENV} --browser ${BROWSER} --test-file tests --allure --ci
                        ''',
                        returnStdout: true
                    ).trim()
                    
                    // 从输出中提取测试结果JSON
                    def testResultMatch = testOutput =~ /TEST_RESULT_JSON: (.+)/
                    if (testResultMatch) {
                        def testResultJson = testResultMatch[0][1]
                        def slurper = new groovy.json.JsonSlurper()
                        def testResults = slurper.parseText(testResultJson)
                        
                        // 直接输出所有测试数据
                        echo "📈 测试结果详细统计:"
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
                        
                    } else {
                        echo "⚠️ 未找到测试结果数据"
                        env.TEST_SUMMARY = "未找到测试结果"
                        env.TEST_STATS = "{}"
                        env.TEST_TOTAL = "0"
                        env.TEST_PASSED = "0"
                        env.TEST_FAILED = "0"
                        env.TEST_ERROR = "0"
                        env.TEST_SKIPPED = "0"
                    }
                }
            }
        }
    }
    
    post {
        always {
            script {
                def gitAuthor = sh(
                    script: 'git log -1 --pretty=format:"%an"',
                    returnStdout: true
                ).trim()
                
                currentBuild.description = "分支: ${env.GIT_BRANCH_NAME} | 完整提交: ${env.GIT_COMMIT_FULL} | 短提交: ${env.GIT_COMMIT_SHORT} | 作者: ${gitAuthor}"
                currentBuild.displayName = "#${env.BUILD_NUMBER} -WebUIAutoTest- ${env.GIT_BRANCH_NAME} (${env.GIT_COMMIT_SHORT})"
            }
            
            script {
                def allureResultsDir = "reports/${params.ENVIRONMENT}/allure-results"
                def allureExists = fileExists(allureResultsDir)
                
                if (allureExists) {
                    try {
                        allure([
                            includeProperties: false,
                            jdk: '',
                            properties: [],
                            reportBuildPolicy: 'ALWAYS',
                            results: [[path: allureResultsDir]]
                        ])
                        echo "✅ Allure报告发布成功"
                    } catch (Exception e) {
                        echo "⚠️ Allure报告发布失败: ${e.getMessage()}"
                    }
                } else {
                    echo "⚠️ 未找到Allure结果目录: ${allureResultsDir}"
                }
                archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
            }
        }
        
        success {
            script {
                try {
                    def buildInfo = getBuildInfo()
                    def messageContent = buildWechatMessage(buildInfo.jobName, buildInfo.buildNumber, buildInfo.buildUrl, buildInfo.environment, buildInfo.browserType, buildInfo.headlessMode, env.GIT_BRANCH_NAME, env.GIT_COMMIT_SHORT, buildInfo.duration, "green", "构建成功 ✅")
                    
                    try {
                        withCredentials([string(credentialsId: 'WECHAT_WEBHOOK', variable: 'WEBHOOK_URL')]) {
                            def webhookInfo = "${WEBHOOK_URL}"
                            echo "===== 企业微信通知配置信息 ====="
                            echo "Webhook URL: ${webhookInfo}"
                            echo "使用的凭据ID: WECHAT_WEBHOOK"
                            echo ""
                            echo "===== 企业微信通知内容 ====="
                            echo messageContent
                            echo "==========================="
                            
                            sendWechatNotification(WEBHOOK_URL, messageContent)
                        }
                    } catch (Exception e) {
                        echo "⚠️ 企业微信通知发送失败: ${e.getMessage()}"
                    }
                  } catch (Exception e) {
                    echo "🎉 测试执行成功！"
                    echo "📋 Git信息获取失败，但测试已通过"
                    
                    def buildInfo = getBuildInfo()
                    def simpleMessageContent = buildSimpleWechatMessage(buildInfo.jobName, buildInfo.buildNumber, buildInfo.buildUrl, "green", "构建成功 ✅")
                    
                    try {
                        withCredentials([string(credentialsId: 'WECHAT_WEBHOOK', variable: 'WEBHOOK_URL')]) {
                            sendWechatNotification(WEBHOOK_URL, simpleMessageContent)
                        }
                    } catch (Exception ex) {
                        echo "⚠️ 企业微信通知发送失败: ${ex.getMessage()}"
                    }
                  }
              }
          }
        
        failure {
            script {
                try {
                    def buildInfo = getBuildInfo()
                    def messageContent = buildWechatMessage(buildInfo.jobName, buildInfo.buildNumber, buildInfo.buildUrl, buildInfo.environment, buildInfo.browserType, buildInfo.headlessMode, env.GIT_BRANCH_NAME, env.GIT_COMMIT_FULL, buildInfo.duration, "red", "构建失败 ❌")
                    
                    try {
                        withCredentials([string(credentialsId: 'WECHAT_WEBHOOK', variable: 'WEBHOOK_URL')]) {
                            sendWechatNotification(WEBHOOK_URL, messageContent)
                        }
                    } catch (Exception e) {
                        echo "⚠️ 企业微信通知发送失败: ${e.getMessage()}"
                    }
                } catch (Exception e) {
                    echo "❌ 测试执行失败！"
                    echo "📋 Git信息获取失败"
                    
                    def buildInfo = getBuildInfo()
                    def simpleMessageContent = buildSimpleWechatMessage(buildInfo.jobName, buildInfo.buildNumber, buildInfo.buildUrl, "red", "构建失败 ❌")
                    
                    try {
                        withCredentials([string(credentialsId: 'WECHAT_WEBHOOK', variable: 'WEBHOOK_URL')]) {
                            sendWechatNotification(WEBHOOK_URL, simpleMessageContent)
                        }
                    } catch (Exception ex) {
                        echo "⚠️ 企业微信通知发送失败: ${ex.getMessage()}"
                    }
                }
            }
        }
        
        cleanup {
            sh 'rm -rf venv'
            echo "🧹 清理.venv完成"
        }
    }
}

def getBuildInfo() {
    return [
        jobName: env.JOB_NAME ?: "Unknown Job",
        buildNumber: env.BUILD_NUMBER ?: "Unknown",
        buildUrl: env.BUILD_URL ?: "",
        environment: params.ENVIRONMENT ?: "unknown",
        browserType: params.BROWSER_TYPE ?: "unknown",
        headlessMode: params.HEADLESS_MODE ?: "unknown",
        duration: currentBuild.durationString ?: "unknown"
    ]
}

// 构建测试统计详情的通用函数
def buildTestStatsDetails() {
    def testTotal = env.TEST_TOTAL ?: "0"
    def testPassed = env.TEST_PASSED ?: "0"
    def testFailed = env.TEST_FAILED ?: "0"
    def testError = env.TEST_ERROR ?: "0"
    def testSkipped = env.TEST_SKIPPED ?: "0"
    
    // 构建详细统计部分
    def statsDetails = "> **详细统计**:\n>   • 总计: ${testTotal}个\n>   • 成功: <font color=\"green\">${testPassed}个</font>"
    
    // 只有当失败数大于0时才添加失败统计
    if (testFailed.toInteger() > 0) {
        statsDetails += "\n>   • 失败: <font color=\"red\">${testFailed}个</font>"
    }
    
    // 只有当错误数大于0时才添加错误统计
    if (testError.toInteger() > 0) {
        statsDetails += "\n>   • 错误: <font color=\"red\">${testError}个</font>"
    }
    
    // 只有当跳过数大于0时才添加跳过统计
    if (testSkipped.toInteger() > 0) {
        statsDetails += "\n>   • 跳过: <font color=\"orange\">${testSkipped}个</font>"
    }
    
    return statsDetails
}

def buildWechatMessage(jobName, buildNumber, buildUrl, environment, browserType, headlessMode, gitBranch, gitCommit, duration, color, status) {
    def statsDetails = buildTestStatsDetails()
    
    return """### 【${jobName}】构建通知
> **状态**: <font color=\"${color}\">${status}</font>
> **分支**: ${gitBranch}
> **提交信息**: ${gitCommit}
> **执行环境**: ${environment}
> **执行浏览器**: ${browserType}
> **执行时间**: ${duration.replace(' and counting', '')}
> **控制台日志**: [查看日志](${buildUrl}console)
> **Allure报告**: [查看报告](${buildUrl}allure)
${statsDetails}"""
}

def buildSimpleWechatMessage(jobName, buildNumber, buildUrl, color, status) {
    def statsDetails = buildTestStatsDetails()
    
    return """### 【${jobName}】构建通知
> **状态**: <font color=\"${color}\">${status}</font>
> **控制台日志**: [查看日志](${buildUrl}console)
> **Allure报告**: [查看报告](${buildUrl}allure)
${statsDetails}"""
}

def sendWechatNotification(webhookUrl, messageContent) {
    sh """
        . venv/bin/activate
        echo "📢 发送企微通知..."
        python utils/send_wechat_notice.py "${webhookUrl}" "${messageContent}"
    """
}