# 数据落盘格式与回收流程

一场访谈结束必须留下**两个文件**：`.json`（结构化原始数据）+ `.md`（可读逐字稿）。
两者的完整对话内容必须一致，`.json` 是给脚本合并用的，`.md` 是给人读和做编码用的。

## 一、落盘位置与命名

默认目录：`~/chagee-interviews/`（不存在就自动创建）。

文件名：`{受访者编号}__{日期}__{访谈员}.json`，例如：

```
~/chagee-interviews/U01__2026-10-14__成员5.json
~/chagee-interviews/U01__2026-10-14__成员5.md
```

**受访者编号统一由组长分配**，按路线编码 —— 后面做配额和交叉分析都靠它：

| 前缀 | 路线 | 建议配额 |
|---|---|---|
| `U01`–`U04` | ① 买过 | 4 人 |
| `A01`–`A03` | ② 知道但没买过 | 3 人 |
| `C01` | ③ 没听过（零认知对照） | 0–1 人 |

## 二、原始数据的硬要求

1. **逐字，不加工。** `turns` 里写受访者原话，不改写、不润色、不替他归纳、不做摘要。
2. **访谈员的话也要记**（开场白、每一句追问、结束语）。没有提问就无法判断回答的语境。
3. **没回答的题记「（未回答）」**，不要留空、不要跳过 —— 缺口本身是数据。
4. **不写可识别信息。** 不要记录真实姓名、手机号、微信号、公司名。只保留 `respondent_id`。
5. **标注分流与来源**：`route`、`market`、`brand_named_at_opening`（开场有没有提前报品牌名）必填，
   否则后面无法解释数据差异。

## 三、JSON 结构

```json
{
  "schema_version": "1.0",
  "meta": {
    "respondent_id": "U01",
    "route": "①买过",
    "market": "中国香港",
    "interviewer": "成员5",
    "date": "2026-10-14",
    "started_at": "2026-10-14T20:31:00+08:00",
    "duration_min": 14,
    "consent": true,
    "brand_named_at_opening": true
  },
  "profile": {
    "age": "22",
    "gender": "女",
    "location_raw": "香港",
    "market": "中国香港",
    "frequency": "一周1-2次",
    "usual_brands": ["万波", "喜茶"],
    "brand_relation": "买过",
    "attitude": "偏正面",
    "attitude_why": "觉得在奶茶里算干净卫生的，味道也好"
  },
  "turns": [
    { "q": "开场", "interviewer": "全文……", "respondent": "全文……" },
    { "q": "P1",   "interviewer": "……",     "respondent": "……" },
    { "q": "Q1",   "interviewer": "……",     "respondent": "……" },
    { "q": "Q1.f1","interviewer": "……",     "respondent": "……" }
  ],
  "evidence_card": {
    "module_2_self_concept":    { "points": [], "quotes": [] },
    "module_3_attitude":        { "points": [], "quotes": [] },
    "module_4_memory_learning": { "points": [], "quotes": [] },
    "module_5_social_culture":  { "points": [], "quotes": [] },
    "module_6_other":           { "points": [], "quotes": [] },
    "anomalies": [],
    "gaps": []
  },
  "notes": ""
}
```

关于 `turns` 里的 `q` 字段：主问题写 `Q1`，它的第一层追问写 `Q1.f1`，第二层写 `Q1.f2`。
画像题写 `P1`–`P4`，开场与收尾写 `开场` / `结束`。

## 四、回报给研究者的流程

skill **不能自动把数据传回去** —— 它运行在访谈员自己的电脑上，没有回传通道。所以走文件交接：

1. 访谈员跑完访谈 → 到 `~/chagee-interviews/` 找到刚生成的 `.json` 和 `.md` 两个文件
2. 两个文件一起发给研究者（微信 / 邮件 / 网盘都行）
3. 研究者把收到的所有文件**丢进同一个文件夹**
4. 在该文件夹跑合并脚本：

   ```bash
   python3 scripts/collect.py ~/chagee-interviews
   ```

   会生成三张总表：逐轮长表（做编码用）、访谈级宽表（做配额核对用）、全文合并稿（通读用）。

## 五、边界情况

- **受访者不愿留档**：只输出证据卡，不写文件，并在证据卡里注明「受访者不同意留档」。
- **中途中断**：照样落盘，`turns` 里到哪里停就到哪里，并在 `notes` 写明中断原因。
- **同一访谈员跑多场**：文件名里的 `respondent_id` 不同即可，都放同一个目录。
- **`consent` 为 false**：不要落盘。
