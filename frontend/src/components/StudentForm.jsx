import { useState } from 'react'

const SECTIONS = [
  {
    title: '基本信息',
    icon: '👤',
    fields: [
      { key: 'name', label: '姓名', placeholder: '例如：张三', required: true },
      { key: 'level', label: '当前技术水平', placeholder: '例如：熟悉 Python，会基础前端，未接触过 AI 开发', required: true },
      { key: 'target_role', label: '目标岗位', placeholder: '例如：AI 全栈开发工程师', required: true },
    ],
  },
  {
    title: '学习情况',
    icon: '📚',
    fields: [
      { key: 'daily_hours', label: '每天可投入学习时间', placeholder: '例如：工作日 2 小时，周末 6 小时', required: true },
      { key: 'weaknesses', label: '薄弱环节', placeholder: '例如：算法基础薄弱、工程化经验不足、缺乏项目经历', required: true, textarea: true },
      { key: 'duration', label: '期望学习周期（可选）', placeholder: '例如：3 个月' },
      { key: 'notes', label: '补充说明（可选）', placeholder: '其他想告诉 AI 的信息', textarea: true },
    ],
  },
]

const INITIAL = Object.fromEntries(
  SECTIONS.flatMap((s) => s.fields).map((f) => [f.key, '']),
)

export default function StudentForm({ onSubmit, onBack, error }) {
  const [form, setForm] = useState(INITIAL)

  const update = (key) => (e) => setForm((s) => ({ ...s, [key]: e.target.value }))
  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(form)
  }

  const inputCls =
    'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-800 placeholder-slate-400 shadow-sm transition focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200'

  return (
    <div className="fade-in min-h-screen bg-slate-50">
      {/* 顶部栏 */}
      <header className="border-b bg-white shadow-sm">
        <div className="mx-auto flex max-w-3xl items-center gap-4 px-6 py-4">
          <button
            onClick={onBack}
            className="rounded-lg px-3 py-1.5 text-sm font-medium text-slate-600 transition hover:bg-slate-100 hover:text-slate-900"
          >
            ← 返回
          </button>
          <h1 className="text-lg font-bold">填写学生信息</h1>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-6 py-8">
        {/* 步骤指示 */}
        <div className="mb-6 flex items-center gap-2 text-sm text-slate-500">
          <span className="font-semibold text-indigo-600">① 填写信息</span>
          <span>→</span>
          <span>② AI 生成</span>
          <span>→</span>
          <span>③ 下载计划</span>
        </div>

        {error && (
          <div className="mb-5 rounded-xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
            ⚠️ {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {SECTIONS.map((section) => (
            <section key={section.title} className="rounded-2xl bg-white p-6 shadow-sm">
              <h2 className="mb-4 flex items-center gap-2 text-base font-semibold text-slate-800">
                <span>{section.icon}</span>
                {section.title}
              </h2>
              <div className="grid gap-4 sm:grid-cols-2">
                {section.fields.map((f) => (
                  <div key={f.key} className={f.textarea ? 'sm:col-span-2' : ''}>
                    <label className="mb-1.5 block text-sm font-medium text-slate-700">
                      {f.label}
                      {f.required && <span className="text-red-500"> *</span>}
                    </label>
                    {f.textarea ? (
                      <textarea
                        className={inputCls}
                        rows={3}
                        placeholder={f.placeholder}
                        value={form[f.key]}
                        onChange={update(f.key)}
                        required={f.required}
                      />
                    ) : (
                      <input
                        className={inputCls}
                        type="text"
                        placeholder={f.placeholder}
                        value={form[f.key]}
                        onChange={update(f.key)}
                        required={f.required}
                      />
                    )}
                  </div>
                ))}
              </div>
            </section>
          ))}

          <button
            type="submit"
            className="w-full rounded-xl bg-gradient-to-r from-indigo-600 to-blue-600 px-6 py-3.5 text-base font-semibold text-white shadow-lg shadow-indigo-200 transition hover:from-indigo-700 hover:to-blue-700"
          >
            生成学习计划 →
          </button>
        </form>
      </main>
    </div>
  )
}
