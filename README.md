# TI WebUI 自动化测试框架

基于 **Python + Playwright + Allure** 的现代化 WebUI 自动化测试框架，采用 **PO设计模式** 和 **数据驱动** 架构，支持多环境测试、装饰器截图、视频录制等功能。

## 🚀 框架特性

### 核心功能
- ✅ **PO设计模式** - 页面对象模式，代码复用性高，维护性强
- ✅ **数据驱动** - 支持 selectors 和 target 数据分离，灵活配置
- ✅ **多环境支持** - 支持 dev/test/prod 环境隔离
- ✅ **公共数据引用** - 支持环境间数据共享和引用机制
- ✅ **装饰器截图** - 自动为每个测试步骤截图
- ✅ **视频录制** - 自动录制测试执行过程
- ✅ **Allure报告** - 美观详细的测试报告
- ✅ **环境数据隔离** - 不同环境使用不同的测试数据
- ✅ **并行执行** - 支持多进程并行测试
- ✅ **失败重试** - 支持测试失败自动重试
- ✅ **中文环境** - 默认中文浏览器环境，支持国际化测试

### 技术栈
- **Python 3.11+** - 主要编程语言
- **Playwright 1.40.0** - 现代化浏览器自动化
- **Pytest 7.4.3** - 测试框架
- **Allure 2.13.2** - 测试报告
- **Loguru 0.7.2** - 结构化日志
- **Pydantic 2.5.0** - 数据验证

## 📁 项目结构

```
TI_webUI/
├── config/                     # 配置管理
│   ├── __init__.py
│   ├── config.py              # 主配置
│   └── environments.py        # 环境配置
├── data/                      # 测试数据（按环境隔离）
│   ├── common.json            # 公共测试数据
│   ├── dev/
│   │   └── test_data.json    # 开发环境数据
│   ├── test/
│   │   └── test_data.json    # 测试环境数据
│   └── prod/
│       └── test_data.json    # 生产环境数据
├── pages/                     # 页面对象
│   ├── __init__.py
│   ├── base_page.py          # 基础页面类
│   └── teacherin_page.py     # TeacherIn页面对象
├── tests/                     # 测试用例
│   ├── __init__.py
│   ├── conftest.py           # Pytest配置
│   └── userpage/             # 用户页面测试
│       └── test_teacherin.py # TeacherIn测试用例
├── utils/                     # 工具类
│   ├── __init__.py
│   ├── base_page.py          # 基础页面工具
│   ├── decorators.py         # 装饰器（截图+视频）
│   ├── logger.py             # 日志工具
│   ├── screenshot.py         # 截图工具
│   ├── test_case_base.py     # 测试用例基类
│   ├── test_data_manager.py  # 测试数据管理
│   ├── video_manager.py      # 视频管理工具
│   └── wait.py               # 等待工具
├── reports/                  # 测试报告
├── playwright.config.py      # Playwright配置
├── pytest.ini               # Pytest配置
├── requirements.txt          # 依赖包
├── run_tests.py             # 测试运行脚本
├── TEST_EXECUTION_GUIDE.md  # 测试执行详细指南
└── README.md                # 项目文档
```

## 🛠️ 安装配置

### 1. 克隆项目
```bash
git clone <repository-url>
cd TI_webUI
```

### 2. 创建虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 安装浏览器
```bash
playwright install
```

### 5. 安装Allure（可选）
```bash
# Mac
brew install allure

# Windows
scoop install allure

# Linux
# 参考: https://docs.qameta.io/allure/#_installing_a_commandline
```

## 🎯 使用方法

### 基本命令
```bash
# 运行所有测试（默认test环境）
python run_tests.py

# 指定环境运行
python run_tests.py --env dev
python run_tests.py --env test
python run_tests.py --env prod

# 运行指定测试文件
python run_tests.py --env test --test-file tests/userpage/test_teacherin.py

# 运行指定测试函数
python run_tests.py --env test --test-file tests/userpage/test_teacherin.py --test-function test_teacherin_multi_page

# 生成Allure报告
python run_tests.py --env test --allure

# 并行执行
python run_tests.py --env test --parallel

# 指定浏览器
python run_tests.py --env test --browser firefox

# 无头模式
python run_tests.py --env test --headless

# 安装浏览器
python run_tests.py --install-browsers
```

### 完整测试执行示例
```bash
# 运行测试环境的所有测试，生成Allure报告
python run_tests.py --env test --test-file tests --allure
```

## 📝 数据驱动设计

### 公共数据引用机制
框架支持公共数据引用，允许环境间数据共享：

#### 公共数据文件 (`data/common.json`)
```json
{
  "teacherin_user_page_star_course": "收藏的课程",
  "teacherin_user_page_post_course": "发布的课程",
  "teacherin_user_page_homepage_title": "TeacherIn",
  "teacherin_user_page_url_contains": "teacherin",
  "timeout_short": 5000,
  "timeout_medium": 10000,
  "timeout_long": 30000,
  "search_keyword_1": "自动化测试",
  "search_keyword_2": "Playwright"
}
```

#### 环境数据引用 (`data/test/test_data.json`)
```json
{
  "teacherin_user_page": {
    "selectors": {
      "star_course": "${common.teacherin_user_page_star_course}",
      "post_course": "${common.teacherin_user_page_post_course}"
    },
    "target": {
      "homepage_title": "${common.teacherin_user_page_homepage_title}",
      "course_name": "示例课程名称",
      "url_contains": "${common.teacherin_user_page_url_contains}"
    }
  }
}
```

### 引用语法
- **格式**: `${common.key1.key2}`
- **解析**: 自动解析为公共数据中的对应值
- **优先级**: 环境数据 > 公共数据引用 > 默认值

### 测试数据结构
框架采用 **selectors** 和 **target** 分离的数据驱动设计：

```json
{
  "teacherin_user_page": {
    "selectors": {
      "star_course": "收藏的课程",
      "post_course": "发布的课程"
    },
    "target": {
      "homepage_title": "TeacherIn",
      "course_name": "示例课程名称",
      "url_contains": "teacherin"
    }
  }
}
```

- **selectors**: 用于页面元素定位
- **target**: 用于页面内容验证

### 环境数据隔离
- `data/common.json` - 公共测试数据（各环境共享）
- `data/dev/test_data.json` - 开发环境数据
- `data/test/test_data.json` - 测试环境数据  
- `data/prod/test_data.json` - 生产环境数据

## 🎨 页面对象模式

### 基础页面类
```python
from utils.base_page import BasePage

class BasePage:
    """提供通用页面操作方法"""
    - navigate_to()           # 页面导航
    - click()                 # 点击元素
    - type_text()            # 输入文本
    - verify_title_contains() # 验证标题
    - click_text_element()   # 点击文本元素
    - verify_page_content_contains() # 验证页面内容
    - get_current_url()      # 获取当前URL
```

### 具体页面对象
```python
class TeacherInHomePage(BasePage):
    def __init__(self, page: Page, base_url: str, selectors: dict, target_data: dict = None):
        super().__init__(page, base_url)
        self.star_course_text = selectors["star_course"]
        self.target_data = target_data or {}

    @allure_step("打开TeacherIn个人主页")
    def open_homepage(self) -> bool:
        return self.navigate_to()

    @allure_step("验证主页元素")
    def verify_homepage_elements(self) -> bool:
        expected_title = self.target_data.get("homepage_title", "TeacherIn")
        return self.verify_title_contains(expected_title)

    @allure_step("点击收藏的课程")
    def click_star_course(self) -> bool:
        return self.click_text_element(self.star_course_text)
```

## 🧪 编写测试用例

### 测试用例结构
```python
@allure.epic("TeacherIn网站")
@allure.feature("页面解耦与多页面对象组合")
class TestTeacherInNavigation(TestCaseBase):
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        # 初始化测试环境
        self.setup_test_environment(page)
        
        # 获取URL配置
        urls = self.get_urls()
        
        # 获取测试数据
        teacherin_data = self.get_test_data().get_all_data().get("teacherin_user_page", {})
        selectors_data = teacherin_data.get("selectors", {})
        target_data = teacherin_data.get("target", {})
        
        # 初始化页面对象
        self.home_page = TeacherInHomePage(page, base_url=urls["teacherin_user_page"], 
                                         selectors=selectors_data, target_data=target_data)
        self.education_page = TeacherInEducationPage(page, selectors=selectors_data, 
                                                   target_data=target_data)
        
        # 记录测试数据
        self.log_test_data("teacherin_user_page")

    @allure.story("分页面对象组合操作")
    def test_teacherin_multi_page(self, page: Page):
        self._step_open_homepage(page)
        self._step_click_core_literacy(page)
        self._step_verify_url(page)

    @step_screenshot("打开个人主页-验证主页元素")
    def _step_open_homepage(self, page: Page):
        assert self.home_page.open_homepage(), "打开个人主页失败"
        assert self.home_page.verify_homepage_elements(), "主页元素校验失败"
        assert self.home_page.click_star_course(), "点击收藏的课程失败"
```

## 🎭 装饰器功能

### 截图装饰器
```python
@step_screenshot("测试步骤描述")
def test_step(self, page: Page):
    # 自动在方法执行前后截图
    # 自动添加到Allure报告
    pass
```

### Allure步骤装饰器
```python
@allure_step("步骤描述")
def page_action(self) -> bool:
    # 在Allure报告中显示为独立步骤
    pass
```

### 视频录制装饰器
```python
@allure_step_with_video("测试步骤", attach_video=True)
def test_step(self, page: Page):
    # 自动录制视频并附加到Allure报告
    pass
```

## 📊 测试报告

### Allure报告特性
- **步骤截图** - 每个测试步骤自动截图
- **测试视频** - 完整的测试执行过程视频
- **环境信息** - 显示测试环境配置
- **测试数据** - 显示使用的测试数据
- **执行时间** - 详细的执行时间统计
- **失败分析** - 详细的失败原因分析
- **测试步骤** - 清晰的测试步骤展示

### 生成报告
```bash
# 运行测试并生成Allure报告
python run_tests.py --env test --allure

# 查看报告
allure serve reports/test/allure-results

# 生成静态报告
allure generate reports/test/allure-results -o reports/test/allure-report --clean
```

## 🔧 配置说明

### pytest.ini
```ini
[tool:pytest]
testpaths = tests
markers =
    smoke: 冒烟测试
    regression: 回归测试
addopts = 
    -v
    --tb=short
    --disable-warnings
```

### playwright.config.py
```python
# 浏览器配置
use = {
    "browser": "chromium",
    "headless": False,
    "viewport": {"width": 1920, "height": 1080},
    "locale": "zh-CN",
    "extra_http_headers": {"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}
}

# 视频录制配置
use = {
    "video": "on-first-retry",
    "video_size": {"width": 1920, "height": 1080}
}
```

### 环境变量
```bash
ENV=test          # 测试环境
BROWSER=chromium  # 浏览器类型
HEADLESS=false    # 无头模式
```

## 🎥 视频录制功能

### 功能特点
- **自动录制** - Playwright自动录制测试执行过程
- **视频附件** - 自动将视频附加到Allure测试报告
- **文件管理** - 自动清理旧视频文件，避免磁盘占用
- **高清录制** - 支持1920x1080高清视频录制

### 配置选项
```python
# playwright.config.py
use = {
    "video": "on-first-retry",  # 录制策略
    "video_size": {"width": 1920, "height": 1080},  # 视频尺寸
    "record_video_dir": "./reports/test/videos"  # 视频保存目录
}
```

## 🔍 测试执行详细说明

### 执行流程
1. **命令解析** → 解析命令行参数
2. **环境设置** → 设置环境变量和配置
3. **数据清理** → 清理历史报告和视频文件
4. **Pytest启动** → 构建并执行Pytest命令
5. **测试发现** → 发现测试文件和用例
6. **数据加载** → 加载公共数据和环境数据
7. **引用解析** → 解析数据引用关系
8. **浏览器启动** → 启动中文环境浏览器
9. **测试执行** → 执行测试用例
10. **视频录制** → 录制测试过程
11. **报告生成** → 生成Allure报告
12. **服务器启动** → 启动报告服务器

### 详细执行指南
请参考 [TEST_EXECUTION_GUIDE.md](./TEST_EXECUTION_GUIDE.md) 获取完整的执行过程解析。

## 🚨 故障排查

### 常见问题及解决方案

#### 1. 浏览器启动失败
**问题**: `Browser.new_context() got an unexpected keyword argument 'accept_language'`
**解决方案**: 
- 检查 Playwright 版本是否为 1.40.0
- 确保使用正确的浏览器上下文参数

#### 2. 测试数据加载失败
**问题**: 环境名称显示为"未知环境"
**解决方案**:
- 检查环境变量 `ENV` 是否正确设置
- 验证 `data/{env}/test_data.json` 文件是否存在

#### 3. 公共数据引用失败
**问题**: `${common.key}` 引用无法解析
**解决方案**:
- 检查 `data/common.json` 文件是否存在
- 验证引用路径是否正确
- 确保引用语法格式正确

#### 4. Allure报告生成失败
**问题**: Allure命令无法执行
**解决方案**:
- 确保已正确安装Allure命令行工具
- 检查Allure版本兼容性
- 验证报告目录权限

#### 5. 视频录制失败
**问题**: 视频文件无法生成或附加
**解决方案**:
- 检查磁盘空间是否充足
- 验证视频目录权限
- 确保Playwright视频配置正确

### 调试方法
1. **查看详细日志**: 关注控制台输出的详细日志信息
2. **检查文件结构**: 验证测试数据文件和配置文件
3. **手动测试**: 单独运行Pytest命令进行调试
4. **环境检查**: 确认环境变量和依赖项
5. **版本验证**: 检查各组件版本兼容性

### 日志级别
```python
# 设置日志级别
import loguru
loguru.logger.remove()
loguru.logger.add(sys.stderr, level="DEBUG")  # 调试级别
```

## 📋 依赖包说明

### 核心依赖
```
playwright==1.40.0          # 浏览器自动化
pytest==7.4.3              # 测试框架
pytest-playwright==0.4.2   # Playwright集成
pytest-xdist==3.3.1        # 并行执行
allure-pytest==2.13.2      # Allure报告
pytest-html==4.1.1         # HTML报告
python-dotenv==1.0.0       # 环境变量
loguru==0.7.2              # 日志工具
pydantic==2.5.0            # 数据验证
```

### 版本兼容性
- **Python**: 3.11+
- **Playwright**: 1.40.0
- **Pytest**: 7.4.3
- **Allure**: 2.13.2

## 🤝 贡献指南

### 开发流程
1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 代码规范
- 遵循PEP 8代码风格
- 添加适当的类型注解
- 编写清晰的文档字符串
- 确保测试覆盖率

### 测试要求
- 新增功能必须包含测试用例
- 修改现有功能需要更新相关测试
- 确保所有测试通过

## 📄 许可证

MIT License

## 📞 联系方式

如有问题，请提交Issue或联系维护者。

## 📚 相关文档

- [测试执行详细指南](./TEST_EXECUTION_GUIDE.md) - 完整的测试执行过程解析
- [Playwright官方文档](https://playwright.dev/python/) - Playwright使用指南
- [Pytest官方文档](https://docs.pytest.org/) - Pytest测试框架
- [Allure官方文档](https://docs.qameta.io/allure/) - Allure报告框架

---

**TI WebUI 自动化测试框架** - 让WebUI测试更简单、更可靠！ 