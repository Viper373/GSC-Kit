# 📈 GSC-Kit

欢迎使用 **GSC-Kit** 项目！🚀 这个工具旨在自动化从 Google Search Console (GSC) 提取数据，帮助高效地收集和整理网站的性能指标。

## 📋 目录

- [📦 项目结构](#-项目结构)
- [🔧 安装指南](#-安装指南)
    - [1. 克隆仓库](#1-克隆仓库)
    - [2. 创建虚拟环境](#2-创建虚拟环境)
    - [3. 安装依赖](#3-安装依赖)
- [🛠 使用方法](#-使用方法)
    - [1. 配置 Cookies](#1-配置-cookies)
    - [2. 运行主程序](#2-运行主程序)
- [🧰 工具与库](#-工具与库)
- [📦 插件目录](#-插件目录)
- [📝 贡献指南](#-贡献指南)
- [📄 许可证](#-许可证)
- [🐞 已知问题](#-已知问题)
- [📬 联系方式](#-联系方式)

## 📦 项目结构

以下是项目的目录结构概览：

```plaintext
GSC-Kit/ 
├── run_task/ 
│ ├── run_task_get.py 
│ ├── run_task_indexing.py 
│ └── run_task_performance.py 
├── tool_utils/ 
│ ├── decorator_utils.py 
│ ├── string_utils.py 
│ └── file_utils.py 
├── excel/ 
│ └── (Excel 文件将保存在这里) 
├── logs/ │ └── (日志文件将保存在这里) 
├── GSC-Kit1.0/ 
│ └── (Chrome 插件文件) 
├── requirements.txt 
├── gsc_main.py 
└── README.md
```

- **`run_task/`**: 包含执行各种抓取任务的脚本。
- **`tool_utils/`**: 工具模块，用于日志记录、字符串处理和文件管理。
- **`excel/`**: 存储抓取的 Excel 文件，按日期和域名组织。
- **`logs/`**: 存储日志文件。
- **`GSC-Kit1.0/`**: Chrome 插件目录，包含 GSC-Kit1.0 插件文件。
- **`requirements.txt`**: 列出所有 Python 依赖项。
- **`gsc_main.py`**: 主程序入口，用于同时运行索引和性能抓取任务。
- **`README.md`**: 本文档文件。

## 🔧 安装指南

按照以下步骤在本地机器上设置项目。

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/GSC-Kit.git
cd GSC-Kit
```

### 2. 创建虚拟环境
```python
python3.12 -m venv venv
```

激活虚拟环境：
  
- Windows:

  ```bash
  venv\Scripts\activate
  ```
- macOS丨Linux:

  ```bash
  source venv/bin/activate
  ```

### 3. 安装依赖
确保已安装 Python 3.12.1。然后，安装所需的包：
    
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🛠 使用方法
### 1. 配置 Cookies
确保拥有已登录的 Google Search Console 会话的必要 Cookies。这些 Cookies 是进行身份验证所需的。

在运行`gsc_main.py`之前，需要将这些 Cookies 添加到`gsc_main.py`文件中的`cookies`变量中。
```python
# gsc_main.py

from run_task.run_task_indexing import RunTaskIndexing
from run_task.run_task_performance import RunTaskPerformance

cookies = {
    # 你的cookies
}

run_task_indexing = RunTaskIndexing(cookies)
run_task_performance = RunTaskPerformance(cookies)

if __name__ == '__main__':
    run_task_performance.run_performance()
    run_task_indexing.run_indexing()
```

### 2. 运行主程序
```bash
python gsc_main.py
```

## 🧰 工具与库

- **`requests`**: 用于发送 HTTP 请求。
- **`rich`**: 用于增强日志记录和美化输出。
- **`logging`**: 用于记录事件和错误。
- **`re`**: 用于字符串模式匹配和提取。
- **`datetime`**: 用于处理日期和时间。
- **`os`**: 用于文件和目录操作。

## 📦 插件目录

项目还包含一个 Chrome 插件 GSC-Kit1.0，用于平替 GSC 的功能。插件目录结构如下：
```plaintext
GSC-Kit1.0/
└── images/
    ├── icon.png
    ├── icon16.png
    ├── icon32.png
    ├── icon48.png
    └── icon128.png
├── popup
│   ├── popup.html
│   ├── popup.css
│   ├── popup.js
├── scripts
│   ├── background.js
│   ├── content.js
│   ├── function.js
│   ├── xlsx.mjs
├── static
│   ├── data.css
│   ├── data.html
│   ├── data.js
├── manifest.json
```
### 已知问题 🐞
GSC-Kit1.0 插件小BUG: 当前版本的插件在跳转新链接后无法正确提取数据（提取的是旧页面的数据，除非在新页面刷新一次）。欢迎提交 Issue 或 Pull Request 贡献。

## 📝 贡献指南
欢迎任何形式的贡献！🎉 请按照以下步骤进行：

1. Fork 本仓库。
2. 创建新分支: `git checkout -b feature/YourFeature`。
3. 进行更改并提交: `git commit -m '添加新功能'`。
4. 推送到分支: `git push origin feature/YourFeature`。
5. 提交 Pull Request。

## 📄 许可证
本项目采用 MIT 许可证。有关更多信息，请参阅 [LICENSE](LICENSE) 文件。

## 📬 联系方式
如有任何问题或建议，欢迎联系作者：

- Email: 2020311228@bipt.edu.cn
- GitHub: Viper373

感谢使用 GSC-Kit！若有任何问题或需要支持，请随时打开一个 issue 或联系维护者。使用愉快！🕷️✨