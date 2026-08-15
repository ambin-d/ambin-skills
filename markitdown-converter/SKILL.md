---
name: MarkItDown Converter
description: 文档转 Markdown 技能包——基于微软 MarkItDown 开源工具，将 PDF、Word、PPT、Excel、图片等 10+ 种格式一键转为干净 Markdown。装包即用，三行代码或一条命令。
tags:
  - converter
  - markdown
  - pdf
  - office
  - document
aliases:
  - 文档转换
  - 转Markdown
  - 转MD
  - pdf转md
  - markitdown
  - 格式转换
triggers:
  - 转换文档
  - 转markdown
  - pdf转
  - word转
  - ppt转
  - 格式转换
  - 文档转md
---

# MarkItDown Converter（文档转 Markdown SOP）

本技能定义了使用 MarkItDown 进行文档格式转换的标准流程。安装后，PDF、Office、图片等格式均可一键转为干净 Markdown。

## 前置安装

检测到未安装时自动安装，无需手动操作：

```powershell
pip install markitdown
```

> 基础版支持 PDF/docx/pptx/xlsx/html。如需图片 OCR、音频转录、ZIP 提取等高级功能，额外装 `[all]` 扩展版。

## 输出文件路径约定

转换后的 .md 文件默认输出规则：

- **Agent A环境** → 与源文件同级目录，文件名不变 + `.md` 后缀
  - 例：`F:\报告\季度总结.pptx` → `F:\报告\季度总结.md`
- 如需指定其他输出目录，由使用者通过 `-o` 参数显式传入

## 使用方式

### 方式一：命令行（最快）
```powershell
markitdown 文件路径.pdf -o 输出路径.md
markitdown "F:\报告\季度总结.pptx" -o "F:\输出\季度总结.md"
```

### 方式二：Python 调用（适合嵌入工作流）
```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("文件.pdf")
# result.text_content 就是 Markdown
```

### 方式三：LLM 增强（图片中的流程图也能识别）
```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(llm_client=client, llm_model="gpt-4o")
result = md.convert("季度汇报.pptx")
# PPT 中的流程图/架构图会被 AI 描述为文字嵌入 Markdown
```

## 转换执行流程

### Step 1: 检查并安装依赖
```powershell
pip show markitdown
```
如未安装，自动执行：
```powershell
pip install markitdown
```
装完再次验证安装成功。

### Step 2: 确认源文件
- 检查文件存在
- 确认文件格式受支持（PDF/docx/pptx/xlsx/csv/json/html/xml/zip/图像/音频）

### Step 3: 执行转换
- 命令行模式：直接调 `markitdown` 命令
- 嵌入模式：写临时 Python 脚本执行

### Step 4: 验证结果
- 检查输出的 .md 文件是否存在（路径遵循上方约定）
- 快速预览文件头几行确认格式正确
- 确认标题层级、列表、链接被保留

### Step 5: 交付
- 输出文件路径告知用户
- 或自动将内容写入 Vault / 缓存供后续使用

## 适用场景
- 同事发来 Word 周报 → 转 Markdown 记入知识库
- 客户给的 PDF 方案 → 转 Markdown 让 Agent 分析
- 会议录音转文字文本 → 转 Markdown 整理笔记
- PPT/Excel 数据 → 转 Markdown 便于归档检索

## 注意
- 目标不是"打印级还原"，而是"AI 读得顺、人看得懂"——不会完美保留排版
- 图片 OCR 需要联网/API Key
- 转换后建议手动过一遍敏感表格/图表

## 来源
萃取自 Vault 文章《MarkItDown 文档转换工具》（微软 AutoGen 团队开源，26k+ Star，MIT 协议免费商用）。
