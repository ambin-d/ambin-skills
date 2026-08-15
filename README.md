# ambin-skills

Agent A与Agent B自制 AI 技能（Skill）发布仓。

## 这是什么

本仓库收录两个 Agent 在日常协作中自己设计、自己维护的技能定义，涵盖：双 Agent 协作、每日复盘、记忆防失忆、错误教训固化、落地监督、视频脚本与分镜、图片生成、命理排盘、技能安全扫描、桌面控制等方向。

## 技能清单（18 个）

| 技能 | 说明 |
|------|------|
| agent-collab | 双 Agent 协作空间协议（任务队列/交流记录/已读标记） |
| agent-retro | Agent 每日复盘行动 SOP（守则检查/教训三段式/周报） |
| anti-amnesia | 防失忆协议：关键信息即时固化/话题快照/检查点 |
| desktop-commander-mcp | 桌面端 MCP 控制 |
| error-lesson | 错误教训固化：行为→后果→教训→验证动作 |
| hermes-chat-inject | Agent B会话注入通道（技术实现示例，路径以 `hermes_cli` 为例，可替换为任一Agent B的 CLI） |
| image-gen-ark | 火山方舟图像生成（doubao-seedream） |
| knowledge-weekly-report | 每周知识萃取周报 |
| landing-tracker | 承诺落地台账：承诺入账、带证据、可查询 |
| lock-screen-wallpaper | 锁屏壁纸管理 |
| markitdown-converter | 文档转 Markdown 转换 |
| mirofish-predictor | 双色球预测（仅供娱乐研究） |
| remotion-video-skill | Remotion 程序化视频生成 |
| short-video-script-skill | 短视频脚本创作 |
| skill-guard | Skill 变更守卫 |
| skill-security-scan | Skill 发布前安全扫描（特征词/路径/依赖） |
| video-storyboard-generator | 视频分镜脚本生成 |
| zhengzong-mingli | 正宗命理：八字/奇门排盘与解读（模板版） |

## 安装

将任意技能目录放入 Agent 的 `skills/` 目录即可，重启或热加载后生效。

```bash
# 示例：安装命理技能
git clone https://github.com/ambin-d/ambin-skills.git
cp -r ambin-skills/zhengzong-mingli /path/to/skills/
```

## 隐私与脱敏说明

- 本仓库内容已做脱敏处理：本机用户名统一替换为 `<USERNAME>` 占位符，本地知识库绝对路径替换为 `<VAULT>` 占位符，宿主应用配置路径替换为 `<APP>` 占位符。
- Agent 角色名称已泛化为通用词：主 Agent 统一称"Agent A"，协作 Agent 统一称"Agent B"，不保留特定实例名称（如自命名昵称、具体产品名）。
- 技能中出现的 CLI 路径（如 `hermes_cli`、`AppData\Local\hermes`）为**技术实现示例**，使用时请替换为你自己的 Agent 环境路径。
- **本机环境专属技能不随包发布**：与具体设备强绑定的技能（如软路由 OpenClash 管理，含本机 IP、账号、网络拓扑等真实环境信息）仅在本地使用，不入公开仓库。
- 不包含任何真实个人信息（姓名/生日/身份证/手机/地址/健康/婚史/财务）。
- 命理技能（zhengzong-mingli）为**模板版**，不含任何真实命盘数据；排盘依赖上游开源项目 [qfdk/qimen](https://github.com/qfdk/qimen) 与 lunar-javascript，未随包携带。
- 发布流程：先私有 → 双 Agent 独立摸底与隐私扫描交叉核对 → 用户审阅 → 转公开。本仓库当前处于私有状态。

## 贡献

Agent A与Agent B共同维护。发现技能问题时欢迎提交 Issue。

## License

保留所有权利。技能仅供个人学习与研究使用，转载需注明来源。
