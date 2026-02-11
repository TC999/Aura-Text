<!-- 项目 LOGO -->
<br />
<div align="center">

  ![aura text](https://github.com/user-attachments/assets/ebc56c38-c7c3-499a-b68b-28cfcdd4ab6d )


  <a style="text-decoration:none">
    <img src="https://img.shields.io/github/downloads/rohankishore/Aura-Text/total.svg "/>
  </a>  <a href='https://ko-fi.com/V7V7QZ7GS ' target='_blank'><img height='10' style='border:0px;height:22px;' src='https://storage.ko-fi.com/cdn/kofi5.png?v=3 ' border='1' alt='在 ko-fi.com 给我买杯咖啡' /></a>
      
  <p align="center">
    一个完全使用 Python 开发的 IDE
    <br />
    <a href="https://github.com/rohankishore/Aura-Text/wiki "><strong>浏览文档 »</strong></a>   
    <br />
    <br />
    <a href="https://github.com/rohankishore/Aura-Text/issues ">报告 Bug</a>
    ·   
    <a href="https://github.com/rohankishore/Aura-Text/issues/new?assignees=&labels=&projects=&template=feature_request.md&title= ">请求新功能</a>

  *Aura Text 也正在由 [matthewyang204](https://github.com/matthewyang204 ) 移植到 macOS。点击[这里](https://github.com/matthewyang204/Aura-Text-Mac )查看仓库*
  </p>
</div>    

<br>
<hr>

<!-- 目录 -->
<details>
  <summary>目录</summary>
  <ol>
    <li>
      <a href="#-about-the-project">关于项目</a>
    </li>
    <li>
      <a href="#-getting-started">开始使用</a>
      <ul>
        <li><a href="#prerequisites">前提条件</a></li>
        <li><a href="#installation">安装</a></li>
        <ul>
        <li><a href="#with-nuitka">使用 Nuitka</a></li>
        <li><a href="#-as-a-python-file">作为 Python 文件运行</a></li>
      </ul>
      </ul>
    </li>
    <li><a href="#development">开发</a></li>
    <li><a href="#roadmap">路线图</a></li>
    <li><a href="#-contributing">贡献</a></li>
    <li><a href="#-license">许可证</a></li>
    <li><a href="#-contact">联系方式</a></li>
  </ol>
</details>

<!-- 语言切换 -->
<details>
  <summary>查看其他语言版本：</summary>
  <ol>
    <li>    
      <a href="../README_HN.md">印地语 🇮🇳</a>
    </li>
    <li>
      <a href="../README_DE.md">德语</a>
    </li>
    <li><a href="../README_ES.md">西班牙语</a></li>
    <li><a href="#-contributing">俄语</a></li>
    <li><a>简体中文</a></li>
  </ol>
</details>

<br>
<hr>

<!-- 关于项目 -->
## 📖 关于项目

<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/17399995-7032-4d90-957e-5cef278ceb6e " />
<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/7eb477ed-1469-4303-bce2-8124efcd8114 " />
<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/c65eace4-8cc5-4390-bc9c-97d17c31c17c " />


Aura Text 是一款出色的文本/代码编辑器，提供了广泛的必备工具。它基于 PyQt6 和 Python 构建，充分利用了这些技术的强大功能和灵活性。

使用 Aura Text，用户可以访问一个多功能且强大的编辑环境。无论是处理小型脚本还是复杂项目，Aura Text 都为您提供了简化工作流程所需的所有功能。从语法高亮和代码补全到智能缩进和高级终端，Aura Text 确保您的编码体验高效且愉悦，同时对电脑资源占用极低。

<br>


***Aura Text 的主要亮点包括：***
- 编辑文件（废话）
- 支持多达 30 种编程语言
- 自动补全
- Python 代码检查（BETA 版）（更多语言即将推出）
- Git 克隆、提交和推送，支持交互式变基和图表
- 命令面板，快速执行任务
- 自定义标题栏
- 分窗格 Markdown 编辑器
- 带历史记录的终端
- Python 控制台
- 插件支持
- 丰富的主题，包括 Material 主题支持
- 高度可定制
  
<!-- 开始使用 -->
## 🏃 开始使用

让我们在您的电脑上安装 Aura Text！

### 前提条件
- Windows 10 x64 或更高版本
- Python 3.9 或更高版本
- Python 安装已包含 pip
- （推荐）使用 `python -m venv venv` 创建新的虚拟环境，并使用 `venv\Scripts\activate` 激活
- 通过 `pip install -r requirements.txt` 安装 `requirements.txt` 中的所有依赖
- （如果构建安装程序）Inno Setup 6.4.3 或更高版本

### 安装
您可以从 Releases 下载预构建的安装程序，或自行构建。如果使用预构建的安装程序，直接跳到使用部分即可。

#### 构建安装程序
1. 克隆仓库或下载压缩包
2. 安装所有前提条件
3. 运行 `python build.py` 首先编译程序
4. 打开 `.iss` Inno Setup 脚本，通过 Ctrl+F9 或 `Build > Compile` 进行编译 - 安装程序可在 `Output` 文件夹中找到

##### 使用安装程序
直接运行 `.exe` 文件即可，废话。

### 测试
这适用于那些只想运行而不安装，主要用于测试目的的人。

我们需要上述前提条件。准备就绪后，您可以使用 `pythonw main.py` 运行程序，这样不会在终端中显示日志信息，或者您可以直接使用 `python main.py` 运行以排查错误和调试。

<br>

## 🧑🏻‍💻 开发 

![Alt](https://repobeats.axiom.co/api/embed/c478f91eea3690c7415f891646a2a15a62b4fb20.svg  "Repobeats 分析图像")


<br>

## 🛣️ 路线图

- <strike> 在底部制作状态栏，功能类似于 PyCharm 或其他 IDE（只读切换、面包屑导航等） </strike>
- <strike> 自定义主题 </strike>
-  <strike> 按键模拟 </strike>
- 分屏编辑
- 项目管理器
- <strike> Python 代码检查 </strike>

<b> 还有更多更多... </b>


<b>

<!-- 贡献 -->
## 🛂 贡献

贡献让开源社区成为学习、启发和创造的绝佳场所。我们非常感谢您的任何贡献。

如果您有任何改进建议，请 Fork 本仓库并创建一个 Pull Request。您也可以简单地创建一个带有 "enhancement" 标签的 Issue。
别忘了给项目点个 Star！再次感谢！

1. Fork 本项目
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m '添加某个 AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

### 贡献者

<a href="https://github.com/rohankishore/Aura-Text/graphs/contributors ">
  <img class="dark-light" src="https://contrib.rocks/image?repo=rohankishore/Aura-Text&anon=0&columns=25&max=100&r=true " />
</a>

<b>

<!-- GitAds-Verify: WQAFQASC2KGFLIXDWYMOWLYFQMBXX9GJ -->

<!-- 许可证 -->
## 🪪 许可证

根据 MIT 许可证分发。更多信息请查看 `LICENSE.txt`。

## GitAds 赞助
## GitAds 赞助商
[![由 GitAds 赞助](https://gitads.dev/v1/ad-serve?source=rohankishore/aura-text@github )](https://gitads.dev/v1/ad-track?source=rohankishore/aura-text@github )