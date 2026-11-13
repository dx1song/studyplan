"""大模型返回结果的容错解析器。

LLM 的输出不可完全信任，可能返回：
1. 纯 JSON 数组
2. 被 ```json ... ``` 代码块包裹的 JSON
3. 前后带解释性文字的 JSON
4. 对象包裹的列表（如 {"plan": [...]}）
5. Markdown 表格
6. 纯文本

本模块按优先级依次尝试，全部失败时兜底为单条文本记录，保证流程不中断。
"""

import json
import re
from typing import Any, List, Tuple

# 标准字段（也是 Excel 生成所依赖的规范键）
CANONICAL_KEYS = ["阶段", "课程名称", "学习目标", "每日任务", "预计耗时"]

# 各标准字段的别名（兼容 LLM 可能使用的同义词 / 英文键）
ALIASES = {
    "阶段": ["阶段", "学习阶段", "学习周期", "stage", "phase"],
    "课程名称": ["课程名称", "课程安排", "课程", "course", "course_name", "name"],
    "学习目标": ["学习目标", "具体学习建议", "学习建议", "目标", "goal", "objective"],
    "每日任务": ["每日任务", "实施方案", "实施计划", "任务", "tasks", "daily_tasks", "plan", "action"],
    "预计耗时": ["预计耗时", "预计天数", "预计时间", "天数", "duration", "days", "estimated_days"],
}

# 反向映射：别名 -> 标准键
_ALIAS_MAP = {alias: key for key, names in ALIASES.items() for alias in names}

# 对象包裹列表时可能的键名
_LIST_KEYS = ["plans", "plan", "data", "schedule", "items", "learning_plan",
              "学习计划", "课程计划", "结果", "list"]


def _extract_json(text: str) -> Any:
    """从文本中尽力提取 JSON 对象/数组，失败返回 None。"""
    t = text.strip()
    if not t:
        return None

    # 1) 去掉 Markdown 代码块
    fence = re.search(r"```(?:json)?\s*(.*?)```", t, re.DOTALL | re.IGNORECASE)
    if fence:
        t = fence.group(1).strip()

    # 2) 整段直接解析
    try:
        return json.loads(t)
    except Exception:
        pass

    # 3) 截取第一个 [ 或 { 到最后一个 ] 或 }
    for open_c, close_c in (("[", "]"), ("{", "}")):
        start = t.find(open_c)
        end = t.rfind(close_c)
        if start != -1 and end > start:
            candidate = t[start:end + 1]
            try:
                return json.loads(candidate)
            except Exception:
                continue
    return None


def _normalize_item(item: dict) -> dict:
    """将任意键名的条目规整为标准字段。"""
    out = {}
    for key in CANONICAL_KEYS:
        value = ""
        for alias in ALIASES[key]:
            if alias in item and item[alias] not in (None, ""):
                value = item[alias]
                break
        out[key] = value
    return out


def _fill_defaults(items: List[dict]) -> List[dict]:
    """确保每条记录都具备全部标准字段，且值均为字符串。"""
    result = []
    for it in items:
        clean = {}
        for key in CANONICAL_KEYS:
            v = it.get(key, "")
            if v is None:
                v = ""
            elif not isinstance(v, str):
                v = str(v)
            clean[key] = v
        # 完全空白的条目丢弃
        if any(clean.values()):
            result.append(clean)
    return result


def _parse_markdown_table(text: str) -> List[dict]:
    """解析 Markdown 表格为条目列表。"""
    table_lines = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("|")]
    if len(table_lines) < 2:
        return []

    def split_row(line: str) -> List[str]:
        return [c.strip() for c in line.strip("|").split("|")]

    header = split_row(table_lines[0])
    rows = []
    for ln in table_lines[1:]:
        cells = split_row(ln)
        # 跳过分隔行（如 |---|---|）
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue
        rows.append(cells)

    items = []
    for cells in rows:
        item = {}
        for i, value in enumerate(cells):
            if i < len(header):
                key = header[i]
                canon = _ALIAS_MAP.get(key, key)
                item[canon] = value
        if item:
            items.append(_normalize_item(item))
    return items


def parse_plan(raw_text: str) -> Tuple[List[dict], str]:
    """解析 LLM 返回文本，返回 (条目列表, 解析方式)。

    解析方式取值：json / markdown / fallback_text / empty
    """
    if not raw_text or not raw_text.strip():
        return [], "empty"

    data = _extract_json(raw_text)

    # 对象 -> 取出包裹的列表，或视为单条
    if isinstance(data, dict):
        for key in _LIST_KEYS:
            if key in data and isinstance(data[key], list):
                data = data[key]
                break
        else:
            data = [data]

    if isinstance(data, list):
        items = []
        for it in data:
            if isinstance(it, dict):
                items.append(_normalize_item(it))
            elif isinstance(it, str):
                items.append({"阶段": "", "课程名称": "", "学习目标": "",
                              "每日任务": it, "预计耗时": ""})
        if items:
            return _fill_defaults(items), "json"

    # Markdown 表格
    md_items = _parse_markdown_table(raw_text)
    if md_items:
        return _fill_defaults(md_items), "markdown"

    # 兜底：整段文本作为一条记录，保证不中断
    fallback = [{
        "阶段": "整体计划",
        "课程名称": "全部课程",
        "学习目标": "见「实施方案」中的原始输出",
        "每日任务": raw_text.strip(),
        "预计耗时": "",
    }]
    return fallback, "fallback_text"
