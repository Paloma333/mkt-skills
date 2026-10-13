#!/usr/bin/env python3
"""合并 chagee-interviewer 产出的访谈数据（原始数据合并，不做清洗）。

用法:
    python3 collect.py <访谈数据目录> [-o <输出目录>]

扫描目录下所有符合 references/data-format.md 结构的 .json，输出三张总表:
    merged_turns.csv        逐轮长表   —— 做质性编码用（一行一轮对话）
    merged_interviews.csv   访谈级宽表 —— 做配额核对与进度追踪用（一行一场）
    merged_transcripts.md   全文合并稿 —— 通读用

只合并、不修改内容。需要清洗请在此之后再单独做。
"""

import argparse
import csv
import json
import sys
from pathlib import Path

MODULES = [
    ("module_2_self_concept", "模块2 自我概念与身份"),
    ("module_3_attitude", "模块3 品牌与竞品态度"),
    ("module_4_memory_learning", "模块4 品牌记忆与学习"),
    ("module_5_social_culture", "模块5 社会文化圈层"),
    ("module_6_other", "模块6 其他洞察"),
]

TURN_COLS = [
    "respondent_id", "route", "market", "interviewer", "date",
    "q", "turn_index", "interviewer_text", "respondent_text",
]

INTERVIEW_COLS = [
    "respondent_id", "route", "market", "interviewer", "date", "duration_min",
    "brand_named_at_opening", "consent",
    "age", "gender", "location_raw", "frequency", "usual_brands",
    "brand_relation", "attitude", "attitude_why",
    "turn_count", "module_2", "module_3", "module_4", "module_5", "module_6",
    "anomaly_count", "gap_count", "source_file",
]


def load_interviews(folder):
    """读取目录下所有合法 json，返回 (记录列表, 跳过的文件名列表)。"""
    records, skipped = [], []
    for path in sorted(Path(folder).glob("*.json")):
        if path.name.startswith("."):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            skipped.append((path.name, f"JSON 解析失败: {exc}"))
            continue
        if not isinstance(data, dict) or "turns" not in data:
            skipped.append((path.name, "不是本 skill 的数据格式（缺 turns）"))
            continue
        records.append((path, data))
    return records, skipped


def build_rows(records):
    turn_rows, interview_rows = [], []
    for path, data in records:
        meta = data.get("meta") or {}
        profile = data.get("profile") or {}
        card = data.get("evidence_card") or {}
        rid = meta.get("respondent_id") or path.stem

        turns = data.get("turns") or []
        for idx, turn in enumerate(turns, start=1):
            turn_rows.append({
                "respondent_id": rid,
                "route": meta.get("route", ""),
                "market": meta.get("market", ""),
                "interviewer": meta.get("interviewer", ""),
                "date": meta.get("date", ""),
                "q": turn.get("q", ""),
                "turn_index": idx,
                "interviewer_text": (turn.get("interviewer") or "").strip(),
                "respondent_text": (turn.get("respondent") or "").strip(),
            })

        usual = profile.get("usual_brands") or []
        if isinstance(usual, list):
            usual = " / ".join(str(x) for x in usual)

        row = {
            "respondent_id": rid,
            "route": meta.get("route", ""),
            "market": meta.get("market", ""),
            "interviewer": meta.get("interviewer", ""),
            "date": meta.get("date", ""),
            "duration_min": meta.get("duration_min", ""),
            "brand_named_at_opening": meta.get("brand_named_at_opening", ""),
            "consent": meta.get("consent", ""),
            "age": profile.get("age", ""),
            "gender": profile.get("gender", ""),
            "location_raw": profile.get("location_raw", ""),
            "frequency": profile.get("frequency", ""),
            "usual_brands": usual,
            "brand_relation": profile.get("brand_relation", ""),
            "attitude": profile.get("attitude", ""),
            "attitude_why": profile.get("attitude_why", ""),
            "turn_count": len(turns),
            "anomaly_count": len(card.get("anomalies") or []),
            "gap_count": len(card.get("gaps") or []),
            "source_file": path.name,
        }
        for idx, (key, _label) in enumerate(MODULES, start=2):
            block = card.get(key) or {}
            pts = block.get("points") or []
            row[f"module_{idx}"] = " / ".join(str(p) for p in pts) if isinstance(pts, list) else str(pts)
        interview_rows.append(row)

    turn_rows.sort(key=lambda r: (r["respondent_id"], r["turn_index"]))
    interview_rows.sort(key=lambda r: r["respondent_id"])
    return turn_rows, interview_rows


def write_csv(path, cols, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_transcripts(path, records):
    parts = ["# 霸王茶姬访谈 · 全文合并稿\n"]
    for _p, data in sorted(records, key=lambda r: (r[1].get("meta") or {}).get("respondent_id", "")):
        meta = data.get("meta") or {}
        profile = data.get("profile") or {}
        card = data.get("evidence_card") or {}
        rid = meta.get("respondent_id", "")
        parts.append(f"\n---\n\n## {rid}｜{meta.get('route', '')}｜{meta.get('market', '')}"
                     f"｜访谈员 {meta.get('interviewer', '')}｜{meta.get('date', '')}\n")
        parts.append(f"\n画像：{profile.get('age', '')} 岁，{profile.get('gender', '')}，"
                     f"频率 {profile.get('frequency', '')}，常喝 {profile.get('usual_brands', '')}，"
                     f"与品牌关系 {profile.get('brand_relation', '')}\n")
        parts.append("\n### 逐字稿\n")
        for turn in data.get("turns") or []:
            parts.append(f"\n**问（{turn.get('q', '')}）**：{turn.get('interviewer', '')}\n")
            parts.append(f"\n**答**：{turn.get('respondent', '')}\n")
        parts.append("\n### 证据卡\n")
        for key, label in MODULES:
            block = card.get(key) or {}
            parts.append(f"\n**【{label}】**\n")
            for p in block.get("points") or []:
                parts.append(f"- 要点：{p}\n")
            for q in block.get("quotes") or []:
                parts.append(f"- 原话：“{q}”\n")
        for heading, key in (("反常点 / 前后不一致", "anomalies"), ("这次没有问出来的", "gaps")):
            items = card.get(key) or []
            if items:
                parts.append(f"\n**【{heading}】**\n")
                for it in items:
                    parts.append(f"- {it}\n")
    Path(path).write_text("".join(parts), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="合并 chagee-interviewer 的访谈数据")
    parser.add_argument("folder", help="存放访谈 json 的目录")
    parser.add_argument("-o", "--out", default=None, help="输出目录（默认写到输入目录）")
    args = parser.parse_args()

    src = Path(args.folder).expanduser()
    if not src.is_dir():
        sys.exit(f"目录不存在: {src}")
    out = Path(args.out).expanduser() if args.out else src
    out.mkdir(parents=True, exist_ok=True)

    records, skipped = load_interviews(src)
    if not records:
        sys.exit(f"在 {src} 里没找到可识别的访谈 json。")

    turn_rows, interview_rows = build_rows(records)
    write_csv(out / "merged_turns.csv", TURN_COLS, turn_rows)
    write_csv(out / "merged_interviews.csv", INTERVIEW_COLS, interview_rows)
    write_transcripts(out / "merged_transcripts.md", records)

    print(f"✅ 合并完成：{len(records)} 场访谈，{len(turn_rows)} 轮对话")
    routes = {}
    for r in interview_rows:
        routes[r["route"]] = routes.get(r["route"], 0) + 1
    for route, n in sorted(routes.items()):
        print(f"   {route or '未标注路线'}: {n} 场")
    empties = [r["respondent_id"] for r in interview_rows if not r["module_2"] and not r["module_3"]]
    if empties:
        print(f"⚠️  证据卡几乎空的（可能没写完整）: {', '.join(empties)}")
    for name, reason in skipped:
        print(f"⏭  跳过 {name} —— {reason}")
    print(f"\n输出目录: {out}")
    print("   merged_turns.csv       逐轮长表")
    print("   merged_interviews.csv  访谈级宽表")
    print("   merged_transcripts.md  全文合并稿")


if __name__ == "__main__":
    main()
