# AI 个性化学习计划生成系统

填写学生信息 → 后端拼接「学生信息 + 8 门固定课程」Prompt → 调用大模型（DeepSeek v4 pro）→ 生成详细学习计划 → 解析并导出 **`学习计划.xlsx`**。

## 🚀 一键启动（双击即可，推荐）

直接双击项目根目录的 **`启动学习计划系统.bat`**：

1. 脚本自动检测 Python 并首次自动安装后端依赖；
2. 启动后端服务（前端页面已由后端一并托管，无需单独启动前端）；
3. 自动打开浏览器访问 `http://localhost:8000`。

> 停止：在弹出窗口中按 `Ctrl+C` 或直接关闭窗口。
> 首次运行会自动执行 `pip install -r requirements.txt`，之后再次双击秒开。

## 已配置信息

- 大模型：`deepseek-v4-pro`（DeepSeek 官方接口，API Key 已写入 `backend/.env`）
- 该模型为推理型模型，生成完整计划约需 30 秒~2 分钟，提交后请耐心等待「生成中…」提示。

如需更换模型/密钥，编辑 `backend/.env` 即可（`LLM_BASE_URL`、`LLM_MODEL`、`LLM_API_KEY`）。

## 技术栈

- 后端：Python + FastAPI + OpenAI SDK（兼容 DeepSeek / 通义千问等）+ pandas + openpyxl
- 前端：React + Vite + Tailwind CSS（构建后由后端托管静态页面）

## 目录结构

```
studyplan/
├── 启动学习计划系统.bat   # 双击启动入口
├── backend/
│   ├── main.py             # FastAPI 入口 + 路由 + 托管前端页面
│   ├── launcher.py         # 启动服务并自动打开浏览器
│   ├── courses.py          # 8 门固定课程（硬编码）
│   ├── prompts.py          # System Prompt + 用户 Prompt 拼接
│   ├── llm.py              # LLM 调用封装
│   ├── mock_data.py        # 无 Key 联调示例数据
│   ├── parser.py           # 容错解析（JSON / Markdown / 兜底）
│   ├── excel_generator.py  # 生成 学习计划.xlsx（backend/output/）
│   ├── .env                # API Key 等配置（已配好，勿提交）
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/                # React 页面（表单 + 结果展示）
│   ├── dist/               # 构建产物（后端托管的就是它）
│   ├── vite.config.js
│   └── package.json
└── README.md
```

## 手动启动（开发模式，可选）

后端：

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

前端（如需改前端代码，改完重新构建）：

```bash
cd frontend
npm install
npm run dev            # 开发热更新，/api 已代理到 :8000
npm run build          # 重新生成 dist/，双击启动脚本用的是它
```

## 接口说明

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/generate-plan` | 接收学生信息，触发「拼接 Prompt → 调 LLM → 解析 → 生成 Excel」全流程 |
| GET | `/api/download-excel` | 下载生成的 `学习计划.xlsx` |
| GET | `/api/health` | 健康检查，含 LLM 配置状态 |

### POST /api/generate-plan 请求体

```json
{
  "name": "张三",
  "level": "熟悉 Python，会基础前端，未接触过 AI 开发",
  "target_role": "AI 全栈开发工程师",
  "daily_hours": "工作日 2 小时、周末 6 小时",
  "weaknesses": "工程化经验不足，缺乏项目经历",
  "duration": "3 个月",
  "notes": ""
}
```

## 容错处理方案（LLM 返回解析失败）

`backend/parser.py` 按优先级依次处理，任何一步失败都不中断流程：

1. **纯 JSON 数组** → 直接解析；
2. **代码块包裹的 JSON**（```json ... ```）→ 去围栏后解析；
3. **带解释性文字/前后缀的 JSON** → 截取首个 `[`/`{` 到末个 `]`/`}` 解析；
4. **对象包裹列表**（如 `{"plan": [...]}`）→ 取出列表；
5. **Markdown 表格** → 按表头映射为标准字段；
6. **纯文本兜底** → 整段文本作为一条记录写入「实施方案」。

字段名做了**别名归一化**（`阶段/学习阶段/stage`、`课程名称/课程安排/course` 等均能识别），解析方式通过接口的 `parse_method` 字段回传前端展示。
