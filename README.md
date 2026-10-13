# MKT Skills

基于 Kotler《Marketing Management》知识体系（CUHK MKT 课程）提炼的可复用 AI skill。

## Skills

| Skill | 一句话 | 触发场景 |
|---|---|---|
| [mkt-stp-scaffold](skills/mkt-stp-scaffold/SKILL.md) | 把产品/品牌描述 → Kotler 框架下的完整 STP 战略文档 | 做 STP / 做定位 / 用户分层 / 目标市场分析 |
| [mkt-research-designer](skills/mkt-research-designer/SKILL.md) | 把研究问题 → Kotler 5-stage 调研流程下的完整方案 | 做调研 / 设计问卷 / 调研方案 / 用户访谈 |
| [chagee-interviewer](skills/chagee-interviewer/SKILL.md) | 把一份访谈提纲变成可执行的 AI 访谈员：前置画像分流 + 逐题动态追问 + 结构化证据卡 | 做用户访谈 / 质性调研 / 消费者深度访谈 |

## 知识来源

- [knowledge/mkt-knowledge-map.md](knowledge/mkt-knowledge-map.md) — 两份 XMind（期末知识体系 + final review）的完整导出，是这两个 skill 的知识基础
- 课程：CUHK Marketing Management（Kotler 教材体系）

## 安装（WorkBuddy / Claude Code 类 agent）

```bash
# 用户级安装（所有项目可用）
git clone https://github.com/Paloma333/mkt-skills.git
cp -r mkt-skills/skills/* ~/.workbuddy/skills/
```

安装后直接在对话中说「做 STP」「帮我做个定位」「设计一个调研方案」即可触发。

## mkt-stp-scaffold 输出结构（6 部分）

1. Segmentation 维度建议（4 基础 + B2B 五维度）
2. Targeting 策略 + Persona 草案
3. Positioning 陈述（Among / is / within / because 模板 + 三域价值）
4. POD vs POP 拆分（POP 入局，POD 赢局）
5. 可持续优势三策略
6. 注意事项（Frame of reference / Decoy effect / Straddle positioning）

## mkt-research-designer 输出结构（5 阶段）

1. 定义研究问题（managerial problem → marketing problem）
2. 制定研究计划（五方法选型 + 采样三问）
3. 信息收集（Questionnaires / Qualitative 四技术 / Devices）
4. 分析（含需求测量六概念辨析）
5. 决策输出（insights + 行动建议 + 营销生产力四路径追踪指标）

## chagee-interviewer 工作方式

这是一份现制茶饮消费者深度访谈的执行协议（13 题：4 题前置画像 + 9 题主访谈）。设计上有四个着力点：

- **三层深度**：描述层（喝几次、花多少钱——归问卷）→ 意义层 → 价值与文化层（访谈的主战场）。访谈只在上面两层作业，不与问卷抢地盘。
- **入口分流**：第 3 题判定受访者与品牌的关系（买过 / 知道但没买过 / 没听过），走三条不同路线。其中"知道但没买过"这条最有价值——它解释的是为什么没有转化。
- **动态追问**：每一题都写成「听到什么信号 → 切哪个角度」，而不是固定脚本。同一题在不同回答下走完全不同的追问方向。
- **硬约束**：追问一次问完（每题不超过两次，避免让受访者厌烦）、不问"为什么是 A 而不是 B"这类逼人辩护的假二选一、不接受概括回答（"就随便买的"必须补情境）。

交付物是访谈结束后的**结构化证据卡**：按模块打标、带逐字原话引用，并单列「反常点」与「这次没问出来的」。

附带两个文件：`references/brand-facts.md`（事实型追问要用的素材）与 `references/example-dialogue.md`（示范对话 + 反面示范，用来校准追问密度与语气）。

## License

MIT
