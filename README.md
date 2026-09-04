# MKT Skills

基于 Kotler《Marketing Management》知识体系（CUHK MKT 课程）提炼的两个可复用 AI skill。

## Skills

| Skill | 一句话 | 触发场景 |
|---|---|---|
| [mkt-stp-scaffold](skills/mkt-stp-scaffold/SKILL.md) | 把产品/品牌描述 → Kotler 框架下的完整 STP 战略文档 | 做 STP / 做定位 / 用户分层 / 目标市场分析 |
| [mkt-research-designer](skills/mkt-research-designer/SKILL.md) | 把研究问题 → Kotler 5-stage 调研流程下的完整方案 | 做调研 / 设计问卷 / 调研方案 / 用户访谈 |

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

## License

MIT
