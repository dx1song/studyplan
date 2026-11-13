"""固定课程安排（后端硬编码，前端无需输入）。

需求要求 8 门课程固定保存于后端，LLM 生成计划时必须完整覆盖。
"""

FIXED_COURSES = [
    {"index": 1, "name": "vibe coding项目开发", "description": "掌握 AI 辅助编码与 vibe coding 项目实战能力"},
    {"index": 2, "name": "AI应用全栈开发基础", "description": "AI 应用的前后端全栈开发能力"},
    {"index": 3, "name": "RAG智能体开发", "description": "检索增强生成（RAG）与智能体开发"},
    {"index": 4, "name": "企业工程化能力（Java）", "description": "Java 企业级工程化能力"},
    {"index": 5, "name": "AI工程化-微服务智能体实战", "description": "微服务架构下的智能体工程化实战"},
    {"index": 6, "name": "传统项目的智能化升级", "description": "传统项目的智能化升级改造"},
    {"index": 7, "name": "AI应用评估与模型调优", "description": "AI 应用评估、模型调优与优化"},
    {"index": 8, "name": "面试指导与就业加强", "description": "面试指导与就业能力提升"},
]


def courses_as_text() -> str:
    """将课程列表渲染为可注入 Prompt 的文本。"""
    return "\n".join(
        f"{c['index']}. {c['name']}（{c['description']}）" for c in FIXED_COURSES
    )
