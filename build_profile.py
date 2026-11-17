import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVIDENCE_ROOT = ROOT.parent / "monthly-archive-research"


def read_json(name):
    return json.loads((EVIDENCE_ROOT / name).read_text(encoding="utf-8"))


marketing = read_json("marketing-items.json")
other = read_json("other-items.json")

profile = {
    "schema_version": "1.0",
    "archive_type": "AI信息档案",
    "period": marketing["period"],
    "owner": "zuo xiaopeng",
    "coverage": {
        "marketing": marketing["coverage"],
        "other": other["coverage"],
    },
    "work_items": {
        "marketing": marketing["items"],
        "other": other["items"],
        "personal_assistance": other["personal_assistance"],
    },
}


def item_line(item):
    if "start_date" in item:
        date_range = f"{item['start_date']}—{item['latest_evidence_date']}"
    else:
        date_range = item["date"]
    return (
        f"- **{item['title']}**  \n"
        f"  - 日期：{date_range}  \n"
        f"  - 状态：{item['status']}  \n"
        f"  - 成果：{item['outcome']}"
    )


report_lines = [
    "# 2026年11月 AI信息档案",
    "",
    "## 概览",
    "",
    f"本档案覆盖 **{profile['period']['start']} 至 {profile['period']['end']}**，按 {profile['period']['timezone']} 时区统计。",
    "",
    f"- 营销重构相关工作：**{len(marketing['items'])} 项**",
    f"- 其他工作与工具事项：**{len(other['items'])} 项**",
    f"- 个人辅助事项：**{len(other['personal_assistance'])} 项**",
    "",
    "档案只记录可核查成果，不把“已开发”写成“已上线”。所有状态均保留验证层级。",
    "",
    "## 营销重构",
    "",
]

report_lines.extend(item_line(item) + "\n" for item in marketing["items"])

report_lines.extend([
    "## 其他工作与工具事项",
    "",
])

report_lines.extend(item_line(item) + "\n" for item in other["items"])

report_lines.extend([
    "## 个人辅助事项",
    "",
])

for item in other["personal_assistance"]:
    report_lines.append(item_line(item) + "\n")

report_lines.extend([
    "## 证据与覆盖范围",
    "",
    "- 营销重构：`evidence/marketing-evidence.md`",
    "- 其他工作：`evidence/other-evidence.md`",
    "- 机器可读数据：`ai-info-profile.json`",
    "- 本报告：`AI信息档案-2026-11.md`",
    "",
    "### 覆盖说明",
    "",
    f"- 营销重构核查聊天：**{marketing['coverage']['reviewed_threads']} 个**，本月 **{marketing['coverage']['month_turns']} 轮**。",
    f"- 其他工作核查聊天：**{other['coverage']['reviewed_threads']} 个**，本月 **{other['coverage']['turns_in_period']} 轮**。",
    "- 本档案不做工时统计，不把提交数量当作产出质量，也不把一次成功测试当作整体上线完成。",
    "- 敏感信息已处理：凭据、数据库连接、内网地址、邮箱电话、客户明细和无关私人信息均不进入档案。",
])

(ROOT / "ai-info-profile.json").write_text(
    json.dumps(profile, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

(ROOT / "AI信息档案-2026-11.md").write_text(
    "\n".join(report_lines) + "\n",
    encoding="utf-8",
)

(ROOT / "README.md").write_text(
    "# 2026年11月 AI信息档案\n\n"
    "本目录包含按月归档的工作成果、状态和证据。主报告为 `AI信息档案-2026-11.md`，机器可读数据为 `ai-info-profile.json`。\n",
    encoding="utf-8",
)

evidence_dir = ROOT / "evidence"
evidence_dir.mkdir(exist_ok=True)
for name in ["marketing-evidence.md", "other-evidence.md"]:
    target = evidence_dir / name
    target.write_text((EVIDENCE_ROOT / name).read_text(encoding="utf-8"), encoding="utf-8")

print("Archive generated successfully.")
