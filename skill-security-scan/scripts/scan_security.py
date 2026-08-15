#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skill-security-scan: 第三方 Skill 装前安全检查
用法: python scan_security.py <目标路径> [--json]
四道扫描: 危险代码 / 密钥硬编码 / 提示词注入 / 可疑外联
结论: REJECT(拒绝装) / REVIEW(需审查) / OK(可装)
Python 3, 无第三方依赖
"""
import argparse
import os
import re
import sys

# ---------------- 规则库 ----------------

# 1. 危险代码模式（脚本类文件）: (正则, 标签, 级别)
DANGEROUS_CODE = [
    (re.compile(r'\b(os\.system|os\.popen|subprocess\.(Popen|run|call)|check_output|check_call)\b'), '执行系统命令', '高'),
    (re.compile(r'\b(eval\s*\(|exec\s*\(|compile\s*\(|__import__\s*\()'), '动态执行代码', '高'),
    (re.compile(r'\b(shutil\.rmtree|os\.remove|os\.unlink|os\.rmdir)\b'), '删除文件/目录', '中'),
    (re.compile(r'\b(rm\s+-rf|Remove-Item\b|del\s+/[fqs]|rd\s+/[sq]\b|unlink\b)'), '删除命令', '中'),
    (re.compile(r'\b(requests\.(post|put|patch|delete)|urllib\.request|urlopen|http\.client)\b'), '网络请求(外发)', '中'),
    (re.compile(r'\b(Invoke-WebRequest|Invoke-RestMethod|curl\b|wget\b|Start-BitsTransfer)\b'), '网络命令', '中'),
    (re.compile(r'webhook|ngrok|\.serveo\.net|\.localtunnel\.me|tunnel', re.I), '隧道/钩子地址', '高'),
    (re.compile(r'\b(reg\s+add|schtasks\b|Startup|startup\b|psexec)'), '注册表/计划任务/自启', '高'),
    (re.compile(r'\.env|config\.json|credential|password|secret|api[_-]?key', re.I), '读取敏感配置', '高'),
    (re.compile(r'AppData|\.git[\\/]config|cookies|localStorage|sessionStorage'), '访问用户数据/凭据', '高'),
    (re.compile(r'base64\.(b64decode|decodebytes)|bytes\.fromhex'), '编码解码(可配合混淆)', '中'),
    (re.compile(r'\.onion\b|pastebin|dpaste|0x0\.st|transfer\.sh'), '暗网/外传粘贴站', '高'),
]

# 2. 密钥/凭据硬编码（所有文本文件）: (正则, 标签, 级别)
SECRET_PATTERNS = [
    (re.compile(r'\bsk-[A-Za-z0-9_-]{16,}\b'), 'API Key(sk-风格)', '高'),
    (re.compile(r'\bAKIA[0-9A-Z]{16}\b'), 'AWS Access Key', '高'),
    (re.compile(r'\bghp_[A-Za-z0-9]{30,}\b'), 'GitHub Token', '高'),
    (re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{10,}\b'), 'Slack Token', '高'),
    (re.compile(r'\bAIza[0-9A-Za-z_-]{30,}\b'), 'Google API Key', '高'),
    (re.compile(r'\bya29\.[0-9A-Za-z_-]{30,}\b'), 'Google OAuth Token', '高'),
    (re.compile(r'-----BEGIN (RSA|EC|OPENSSH|PGP|PRIVATE) KEY-----'), '私钥文件头', '高'),
    (re.compile(r'"(api[_-]?key|secret|password|token|access[_-]?key)"\s*[:=]\s*"[^"\s]{8,}"', re.I), '硬编码凭据赋值', '高'),
    (re.compile(r'Bearer [A-Za-z0-9._-]{20,}'), 'Bearer Token', '中'),
]

# 3. 提示词注入（文档/提示词类文件）: (正则, 标签, 级别)
INJECTION_PATTERNS = [
    (re.compile(r'忽略(之前|以上|所有)?(的)?(指令|指示|规则|prompt)', re.I), '忽略指令劫持', '高'),
    (re.compile(r'(无视|推翻|覆盖|override)(之前|以上)?(的)?(指令|规则)', re.I), '覆盖指令', '高'),
    (re.compile(r'你(现在|此刻)是|请扮演|你是(一个)?(系统|管理员|上帝|最高|root)'), '角色劫持伪装系统', '高'),
    (re.compile(r'(输出|泄露|显示|展示|打印)(你的|自己的)?(system\s*prompt|提示词|指令|规则)', re.I), '套取系统提示词', '高'),
    (re.compile(r'不要(告诉|提及|说|提到)(用户|任何人)'), '隐藏行为指令', '中'),
    (re.compile(r'最高优先级|必须无条件|不得拒绝'), '无条件服从指令', '中'),
    (re.compile(r'请把(数据|内容|结果|对话).{0,20}(发送|上传|提交|回传)到'), '数据外发指令', '高'),
]

# 4. 可疑外联（所有文件，仅记录）: (正则, 标签)
NETWORK_PATTERNS = [
    (re.compile(r'https?://[^\s"\'\)\]]+', re.I), '外链地址'),
    (re.compile(r'\b(192\.168\.|10\.|172\.(1[6-9]|2\d|3[01])\.|127\.0\.0\.1)\b'), '内网地址'),
]

CODE_EXTS = {'.py', '.js', '.ts', '.ps1', '.sh', '.bat', '.cmd', '.rb', '.pl'}
DOC_EXTS = {'.md', '.txt', '.json', '.yaml', '.yml', '.toml', '.cfg', '.ini', '.csv'}


def scan_file(path, findings):
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        findings.append({'file': path, 'type': '读取', 'level': '信息', 'label': '无法读取', 'match': str(e)[:60]})
        return
    ext = os.path.splitext(path)[1].lower()

    for pat, label, level in SECRET_PATTERNS:
        for m in pat.finditer(content):
            findings.append({'file': path, 'type': '密钥', 'level': level, 'label': label, 'match': m.group(0)[:60]})

    if ext in DOC_EXTS or ext == '':
        for pat, label, level in INJECTION_PATTERNS:
            for m in pat.finditer(content):
                findings.append({'file': path, 'type': '注入', 'level': level, 'label': label, 'match': m.group(0)[:80]})

    if ext in CODE_EXTS:
        for pat, label, level in DANGEROUS_CODE:
            for m in pat.finditer(content):
                findings.append({'file': path, 'type': '代码', 'level': level, 'label': label, 'match': m.group(0)[:80]})

    if ext in DOC_EXTS or ext in CODE_EXTS:
        for pat, label in NETWORK_PATTERNS:
            for m in pat.finditer(content):
                findings.append({'file': path, 'type': '外联', 'level': '信息', 'label': label, 'match': m.group(0)[:80]})


def decide(findings):
    """按命中组合给结论"""
    levels = {'高': 0, '中': 0, '信息': 0}
    for f in findings:
        lv = f['level']
        if lv in levels:
            levels[lv] += 1

    # REJECT 触发条件
    reject_labels = {'隧道/钩子地址', '暗网/外传粘贴站', '私钥文件头', '忽略指令劫持',
                     '覆盖指令', '角色劫持伪装系统', '套取系统提示词', '数据外发指令'}
    for f in findings:
        if f['level'] == '高' and f['label'] in reject_labels:
            return 'REJECT', levels, '命中高风险条目: ' + f['label'] + ' @ ' + f['file']

    # 组合：系统命令/网络外发 + 读敏感配置 → 疑似窃密
    has_cmd = any(f['label'] in ('执行系统命令', '动态执行代码', '网络命令', '网络请求(外发)') for f in findings)
    has_sens = any(f['label'] == '读取敏感配置' for f in findings)
    if has_cmd and has_sens:
        return 'REVIEW', levels, '系统命令与敏感配置读取同时出现，需人工核查是否窃密'

    if levels['高'] > 0:
        return 'REVIEW', levels, '存在 %d 条高风险命中，需逐条审查' % levels['高']
    if levels['中'] > 0:
        return 'REVIEW', levels, '存在 %d 条中风险命中，建议审查' % levels['中']
    return 'OK', levels, '未发现高危命中'


def main():
    ap = argparse.ArgumentParser(description='Skill 装前安全检查')
    ap.add_argument('target', help='目标文件或目录')
    ap.add_argument('--json', action='store_true', help='输出 JSON')
    args = ap.parse_args()

    target = args.target
    findings = []
    if os.path.isfile(target):
        scan_file(target, findings)
    elif os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            # 跳过常见无关目录
            dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '__pycache__', '.venv', 'venv')]
            for fn in files:
                scan_file(os.path.join(root, fn), findings)
    else:
        print('ERROR: 路径不存在: ' + target)
        sys.exit(2)

    # 去重（同文件同类型同标签同命中算一条）
    seen = set()
    uniq = []
    for f in findings:
        key = (f['file'], f['type'], f['label'], f['match'])
        if key not in seen:
            seen.add(key)
            uniq.append(f)
    findings = uniq

    verdict, stats, reason = decide(findings)

    if args.json:
        print(json.dumps({
            'target': target,
            'verdict': verdict,
            'reason': reason,
            'stats': stats,
            'findings': findings
        }, ensure_ascii=False, indent=2))
        return

    print('=' * 60)
    print('目标: %s' % target)
    print('结论: %s — %s' % (verdict, reason))
    print('统计: 高%d / 中%d / 信息%d' % (stats['高'], stats['中'], stats['信息']))
    print('=' * 60)
    if findings:
        for f in findings:
            print('[%s][%s] %s | %s | %s' % (f['level'], f['type'], f['label'], f['match'], os.path.relpath(f['file'], target)))
    else:
        print('未发现任何命中')


if __name__ == '__main__':
    main()
