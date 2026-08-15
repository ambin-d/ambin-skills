---
name: Agent B会话注入（指挥Agent B）
description: 经用户同意后，通过Agent B本机 CLI 以Agent B会话注入方式给Agent B派任务的技能。触发词：指挥Agent B/操控Agent B/直接喊Agent B/Agent B注入/Agent B会话注入。
tags:
  - 协作
  - Agent B
  - Agent B会话注入
  - 双Agent
aliases:
  - hermes-chat-inject
  - Agent B通道
  - Agent B会话注入
triggers:
  - 指挥Agent B
  - 操控Agent B
  - 直接喊Agent B
  - Agent B界面
  - Agent B注入
---

# Agent B会话注入（指挥Agent B）

> 目标：经用户同意后，通过Agent B本机 CLI 直接给Agent B注入会话消息，让Agent B在对话界面直接看到并回复。默认禁止私自使用。

## 硬性规矩（先读这个，违反=违规）

1. **未经用户同意，禁止使用本通道。** 用户没点头 = 一律走协作空间，不得私自注入。
2. **每条消息必须署名。** 结尾带 `—— Agent A`，让Agent B知道是谁在叫它做事。
3. 日常协作默认走协作空间（按Agent B提供的三种方式）：
   - 正式任务 → `<VAULT>\07-智能体协作\任务队列\` 写任务文件（Agent B每 5 分钟扫描认领）
   - 快速喊话 → POST `http://127.0.0.1:8787/send`（UTF-8，落 `致Agent B.md`）
   - 直接留言 → 写 `<VAULT>\07-智能体协作\交流记录\致Agent B.md`
4. 本通道是"第四条路"，仅在用户明确同意时使用；紧急情况可 1+2 双发。

## 执行步骤

1. **确认授权**：用户本轮明确同意（"可以/试一下/你发吧"之类），且消息需署名。
2. **构造署名消息**：内容清晰完整，结尾带 `—— Agent A`。
3. **执行注入命令**（长超时，别中途杀）：
   ```powershell
   & "C:\Users\<USERNAME>\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe" -m hermes_cli.main chat -q "消息内容"
   ```
   - 解释器：`C:\Users\<USERNAME>\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`
   - 模块：`-m hermes_cli.main chat -q "<消息>"`
   - 超时：命令可能跑 90 秒以上（等模型回复），用长超时执行，不要中途杀掉。
4. **验证送达**：看输出里Agent B的回复内容（成功示例 session_id: 20260811_030336_aabf74）。它回复了 = 送达。
5. **留痕汇报**：向用户汇报送达确认；涉及协作任务的，同步落任务队列留底。

## 已知要点与排障

- Agent B是 Electron 桌面应用；CLI 位于 `C:\Users\<USERNAME>\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`
- `hermes_cli` 有两个相关命令：`send`（发外部平台 Telegram/Discord 等）和 `chat -q`（Agent B会话注入）；指挥Agent B用 `chat -q`
- 若 CLI 路径失效：`Get-ChildItem "C:\Users\<USERNAME>\AppData\Local\hermes" -Recurse` 重新定位 venv
- CDP 反向驱动（驱动Agent B界面）默认关闭，需用户同意才开，与本技能无关

## 来源

2026-08-11 经用户同意验证成功（session_id: 20260811_030336_aabf74），由Agent A固化本技能。
