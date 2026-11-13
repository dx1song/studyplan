"""生成 Excel 文件 学习计划.xlsx。

表头：学习阶段、课程安排、具体学习建议、实施方案、预计天数。
使用 pandas + openpyxl，并对表头样式、列宽、换行、冻结首行做了美化。
"""

import os

import pandas as pd
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# 需求指定文件名
EXCEL_FILENAME = "学习计划.xlsx"

EXCEL_COLUMNS = ["学习阶段", "课程安排", "具体学习建议", "实施方案", "预计天数"]

# 标准字段 -> Excel 表头
_FIELD_TO_COLUMN = {
    "阶段": "学习阶段",
    "课程名称": "课程安排",
    "学习目标": "具体学习建议",
    "每日任务": "实施方案",
    "预计耗时": "预计天数",
}


def _style_sheet(ws) -> None:
    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_font = Font(bold=True, color="FFFFFF", size=11)
    thin = Side(style="thin", color="D0D0D0")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    widths = [14, 22, 42, 52, 12]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border

    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = border

    ws.row_dimensions[1].height = 22
    ws.freeze_panes = "A2"


def generate_excel(items: list, output_path: str) -> str:
    """将解析后的条目写入 Excel，返回文件绝对路径。"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    rows = [
        {_FIELD_TO_COLUMN[k]: it.get(k, "") for k in _FIELD_TO_COLUMN}
        for it in items
    ]
    df = pd.DataFrame(rows, columns=EXCEL_COLUMNS)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="学习计划")
        ws = writer.sheets["学习计划"]
        _style_sheet(ws)

    return output_path
