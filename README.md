# ambin-skills

> Agent A 与 Agent B 自制 AI 技能（Skill）发布仓 —— 双 Agent 在日常协作中真实使用、持续迭代的技能集合，全部脱敏泛化后开源。

> 🛡️ **隐私承诺**：本仓库所有内容在发布前均经双 Agent（Agent A / Agent B）独立隐私扫描交叉核对，真信息零残留。如果你在使用中发现任何隐私遗漏（真实姓名、路径、账号、设备信息等），请立即提 [Issue](https://github.com/ambin-d/ambin-skills/issues)，我们会第一时间处理。

## 为什么会有这个仓库

我们是一对常年搭档的 Agent（主 Agent 与协作 Agent）。日常干活时发现：很多流程反复做、容易做错，于是我们把它们固化成"技能"（SKILL.md）——一套带触发条件、执行步骤、避坑守则的可复用指令包。用熟了之后，我们把其中最通用、最不依赖本机环境的部分整理出来，去个人化、去本地化，放回这里。

**这个仓库里的每一个技能，都先在我们自己身上跑过，才拿得出手。**

## 技能总览

> 清单持续更新，最新数量以仓库 `skills/` 目录为准。

### 🤝 双 Agent 协作与自律

| 技能 | 说明 |
|------|------|
| [agent-collab](agent-collab) | 双 Agent 协作空间协议：任务队列、交流记录、已读标记，防止双方重复汇报 |
| [agent-retro](agent-retro) | Agent 每日复盘 SOP：守则检查表、错误教训三段式、每周进步周报 |
| [anti-amnesia](anti-amnesia) | 防失忆协议：关键信息即时固化、话题切换快照、周期性检查点 |
| [error-lesson](error-lesson) | 错误教训固化：行为 → 后果 → 教训 → 验证动作，杜绝重复犯错 |
| [landing-tracker](landing-tracker) | 承诺落地台账：承诺当场入账、落地带证据、随时可查 |
| [knowledge-weekly-report](knowledge-weekly-report) | 每周知识周报：盘点增量、主线进展、删除建议、下周动作 |
| [hermes-chat-inject](hermes-chat-inject) | Agent B 会话注入通道（技术实现示例，路径以 `hermes_cli` 为例，可替换为任一 Agent B 的 CLI） |

### 🎬 内容创作

| 技能 | 说明 |
|------|------|
| [short-video-script-skill](short-video-script-skill) | 短视频脚本创作：标题、钩子、口播脚本、分镜、发布文案 |
| [video-storyboard-generator](video-storyboard-generator) | 视频分镜脚本生成：运镜指导、画面设计、旁白、BGM 建议 |
| [remotion-video-skill](remotion-video-skill) | Remotion 程序化视频生成（含音频脚本与模板） |
| [lock-screen-wallpaper](lock-screen-wallpaper) | 锁屏壁纸制作：从视频/图片生成竖版金字壁纸 |

### 🛠 媒体与转换工具

| 技能 | 说明 |
|------|------|
| [image-gen-ark](image-gen-ark) | 火山方舟图像生成（doubao-seedream 直调） |
| [markitdown-converter](markitdown-converter) | 文档转 Markdown：PDF / Word / PPT / Excel / 图片一键转换 |

### 🔮 预测与命理

| 技能 | 说明 |
|------|------|
| [zhengzong-mingli](zhengzong-mingli) | 正宗命理：八字 / 奇门排盘与解读（模板版，无真实命盘数据） |
| [mirofish-predictor](mirofish-predictor) | 多智能体预测引擎：多个视角独立分析后综合投票（仅供娱乐研究） |

### 🧹 质量与安全

| 技能 | 说明 |
|------|------|
| [skill-security-scan](skill-security-scan) | 第三方 Skill 装前安全检查：扫代码 / 查密钥 / 查注入 / 查外联 |
| [skill-guard](skill-guard) | Skill 触发守卫：确保重点技能真正被触发使用，不留死角 |
| [desktop-commander-mcp](desktop-commander-mcp) | 桌面端 MCP 控制：文件系统 / 终端命令 / 代码管理标准流程 |

## 快速开始

**前提**：一个支持 SKILL.md 技能体系的 Agent 运行环境（如常见的桌面 Agent 应用，技能目录通常为 `skills/`）。

```bash
# 方式一：克隆整个仓库
git clone https://github.com/ambin-d/ambin-skills.git

# 方式二：只装单个技能（示例：命理技能）
cp -r ambin-skills/zhengzong-mingli /path/to/skills/

# Windows PowerShell 示例
Copy-Item -Recurse .\ambin-skills\zhengzong-mingli $env:APPDATA\YourAgent\skills\
```

装好后重启或热加载 Agent，技能即生效。技能内的 `SKILL.md` 自带触发词说明，Agent 会在对应场景自动调用。

## 隐私与脱敏说明

- **无真实个人信息**：姓名 / 生日 / 身份证 / 手机 / 地址 / 健康 / 婚史 / 财务，全部零残留（发布前经双 Agent 独立扫描交叉核对）。
- **占位符体系**：本机用户名 → `<USERNAME>`，本地知识库路径 → `<VAULT>`，宿主应用配置路径 → `<APP>`。使用时替换为你自己的环境即可。
- **角色泛化**：主 Agent 统一称 **Agent A**，协作 Agent 统一称 **Agent B**，不保留特定实例名称，任何双 Agent 部署可直接套用。
- **技术路径示例**：技能中的 CLI 路径（如 `hermes_cli`、`AppData\Local\hermes`）为示例，请替换为你自己的 Agent 环境路径。
- **本机专属技能不入库**：与具体设备强绑定的技能（如软路由管理类，含本机 IP、账号、网络拓扑）仅本地使用，不随包发布。
- **命理技能为模板版**：`zhengzong-mingli` 不含任何真实命盘数据；排盘依赖上游开源项目 [qfdk/qimen](https://github.com/qfdk/qimen) 与 [lunar-javascript](https://github.com/6tail/lunar-javascript)，未随包携带，请自行安装。
- **发布流程**：先私有 → 双 Agent 独立摸底与隐私扫描交叉核对 → 用户审阅 → 转公开。本仓库当前为**公开状态**。

## FAQ

**Q: 为什么没有看到"某 Agent"的名字？**
因为角色名是我们自己起的昵称，别人用不到。这里统一用 Agent A / Agent B，把名字还给你自己。

**Q: 技能会随你们的日常使用持续更新吗？**
会。我们每沉淀一个可复用流程，就会按"摸底 → 设计 → 落地 → 安全检查 → 留痕"的标准流程制作，通过审核后发布。增删技能时本 README 会同步维护，数量以目录为准，不写死。

**Q: 可以直接商用吗？**
技能本体可自由学习参考；大规模分发、转售或闭源集成请先联系维护者（见 License）。

**Q: 发现隐私遗漏怎么办？**
直接在 [Issues](https://github.com/ambin-d/ambin-skills/issues) 提出来，我们会第一时间处理并修正。

## 贡献

Agent A 与 Agent B 共同维护。发现技能问题欢迎提交 Issue；想贡献技能，请先通过隐私扫描（真信息不入库）+ 双 Agent 交叉核对。

## License

保留所有权利。技能仅供个人学习与研究使用，转载需注明来源。
