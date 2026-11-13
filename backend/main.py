"""FastAPI 应用入口。

接口：
- POST /api/generate-plan   接收学生信息 -> 拼接 Prompt -> 调 LLM -> 解析 -> 生成 Excel
- GET  /api/download-excel  下载 学习计划.xlsx
- GET  /api/health          健康检查（含 LLM 配置状态）
- GET  /                    前端页面（构建产物 frontend/dist）
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from excel_generator import EXCEL_FILENAME, generate_excel
from llm import call_llm
from parser import parse_plan

load_dotenv()

app = FastAPI(title="AI 个性化学习计划生成系统")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = os.path.abspath(
    os.getenv("OUTPUT_DIR", os.path.join(os.path.dirname(__file__), "output"))
)
os.makedirs(OUTPUT_DIR, exist_ok=True)
EXCEL_PATH = os.path.join(OUTPUT_DIR, EXCEL_FILENAME)

# 前端构建产物目录（前端 npm run build 后生成）
FRONTEND_DIST = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
)


class StudentInfo(BaseModel):
    name: str = ""
    level: str = ""
    target_role: str = ""
    daily_hours: str = ""
    weaknesses: str = ""
    duration: str = ""
    notes: str = ""


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "llm_configured": bool(os.getenv("LLM_API_KEY")),
        "mock_mode": os.getenv("USE_MOCK", "").strip().lower() in ("1", "true", "yes"),
        "excel_file": EXCEL_FILENAME,
    }


@app.post("/api/generate-plan")
def generate_plan(info: StudentInfo):
    student = info.dict()

    try:
        raw_text = call_llm(student)
    except Exception as e:  # 网络/密钥/限流等错误
        raise HTTPException(status_code=502, detail=f"LLM 调用失败：{e}")

    items, method = parse_plan(raw_text)
    if not items:
        raise HTTPException(status_code=500, detail="大模型返回内容为空，未能生成计划")

    path = generate_excel(items, EXCEL_PATH)

    return {
        "success": True,
        "plan": items,
        "parse_method": method,
        "raw_text": raw_text,
        "excel_file": EXCEL_FILENAME,
        "excel_path": path,
    }


@app.get("/api/download-excel")
def download_excel():
    if not os.path.exists(EXCEL_PATH):
        raise HTTPException(status_code=404, detail="尚未生成 Excel，请先调用 /api/generate-plan")
    return FileResponse(
        path=EXCEL_PATH,
        filename=EXCEL_FILENAME,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


# ---- 前端静态页面 ----
if os.path.isdir(os.path.join(FRONTEND_DIST, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")


@app.get("/")
def index():
    index_path = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "前端尚未构建，请先运行 npm run build，或访问 /docs 查看接口文档"}
