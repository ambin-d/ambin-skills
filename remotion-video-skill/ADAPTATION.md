# 本机适配说明（2026-08-09）

原仓库为通用 Agent Skill（Claude Code/Codex 向），在本机安装后需按以下约定执行：

## 环境（已验证 2026-08-09）
- Node v24.17.0 ✅（要求 18+）
- npm / npx 11.13.0 —— 必须用 `npm.cmd` / `npx.cmd` 调用（PowerShell 执行策略禁止 .ps1 脚本）
- Python 3.11.15 / 3.12.10 ✅（配音脚本用，`python` 即可）
- ffmpeg / ffprobe 8.1.1 ✅
- Chrome 系统版：`C:\Program Files\Google\Chrome\Application\chrome.exe`（渲染必须指定，避免下载 headless shell）
- edge-tts 7.2.8 ✅（本机已装）

## ⚠️ TypeScript 版本坑（首次渲染踩到，已修复）
- npm 默认装 `typescript@latest` 会装到 **7.0.2（原生版）**，其 API 移除了 `typescript.sys`，@remotion/bundler 打包直接崩：
  `TypeError: Cannot read properties of undefined (reading 'readFile')`
- **必须固定 typescript@5.x**（实测 5.9.3 可用）：
  `npm.cmd install -D --no-audit --no-fund typescript@5.9.3`
- 新建 Remotion 工程时直接写死 5.9.3，不要再装 latest。

## ⚠️ 火山方舟图片模型名坑（2026-08-09 踩到）
- `image_generate` 默认模型 doubao-seedream-2.1 报"不存在或无权限"；裸名 `doubao-seedream-4-0` 直调 API 报 **404 InvalidEndpointOrModel.NotFound**
- **必须用带日期后缀的 `doubao-seedream-4-0-250828`**（见 image-gen-ark skill 的 generate_image.ps1）
- 端点：`POST https://ark.cn-beijing.volces.com/api/v3/images/generations`，Header `Authorization: Bearer <volc_api_key>`，响应 `data[0].url`
- 竖版图：size=720x1280（seedream 支持）

## 渲染约定
- remotion.config.ts 中必须设置 `Config.setBrowserExecutable()` 指向系统 Chrome
- 渲染命令：`npx.cmd remotion render <CompositionId> <输出路径>`
- 成片输出到 `<VAULT>\收件箱\成片\`，工程文件放 `C:\Users\<USERNAME>\remotion-test\`
- 长渲染（>2 分钟）用后台方式跑，避免阻塞对话
- 竖版视频：Composition width=720 height=1280，图片 objectFit=cover 填满

## 实测记录

### 第一条（2026-08-09 01:51，全链路首次跑通）
- 成片：`<VAULT>\收件箱\成片\20260809_第一条代码成片.mp4`
- 规格（ffprobe）：h264+aac / 1280×720 / 30fps / 5.056s / 369KB
- 渲染：150 帧约 15 秒（含打包）

### 第二条《潮汐代码》（2026-08-09 02:04，三 skill 生产线全链路）
- 成片：`<VAULT>\收件箱\成片\20260809_潮汐代码_30s成片.mp4`
- 规格（ffprobe）：h264+aac(2ch) / 720×1280 竖版 / 30fps / 30.058s / 12.2MB
- 生产线：Short Video Script（口播台词）→ Video Storyboard（9镜分镜，套《闺阁·朝暮》镜头语法）→ Remotion（TideCode 工程）
- 画面：火山方舟 doubao-seedream-4-0-250828 生成 9 张 720×1280（9 镜景别，共用人物锚点 prompt 防漂移），Ken Burns 缓推缓拉 + 前景 bokeh 光斑（模拟珠帘窥视）+ 暖调 overlay + 唯一冷调收尾
- 配音：Edge TTS zh-CN-XiaoxiaoNeural（-4% 语速）整段独白 22.3s，Audio from=15 帧对齐
- 环境音：numpy FFT 粉红噪声 + 海浪慢调制合成 30s，音量 0.32（无 BGM 素材时的廉价替代）
- 渲染：900 帧约 1m45s（4 并发）
- 字幕：KaiTi 楷体，逐镜淡入淡出，与配音节奏大致对齐
- 分镜稿：`<VAULT>\收件箱\分镜稿\20260809_潮汐代码_分镜.md`

## 与生产线衔接
- 输入：Short Video Script（口播稿）+ Video Storyboard（分镜）的产出
- 配音：Edge TTS（免费）优先，MiniMax 需 Key（config.json 已有 minimax_api_key）
- audioConfig.ts 模板：一个概念 = 一个场景 = 一段音频，音画同步单一数据源
- 复用脚本（sandbox/tmp_cyborg/）：generate_all.py（9镜出图）、gen_audio.py（配音）、gen_ambient.py（环境音）——改 prompt 即可换选题/形象
