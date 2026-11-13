import { downloadUrl } from '../api'

const METHOD_LABEL = {
  json: '已按标准 JSON 解析',
  markdown: '已按 Markdown 表格解析',
  fallback_text: '未解析出结构化数据，已按纯文本兜底展示',
  empty: '解析结果为空',
}

const COLUMNS = [
  { key: '阶段', label: '学习阶段', width: 'w-32' },
  { key: '课程名称', label: '课程安排', width: 'w-44' },
  { key: '学习目标', label: '具体学习建议' },
  { key: '每日任务', label: '实施方案' },
  { key: '预计耗时', label: '预计天数', width: 'w-24' },
]

export default function ResultView({ result, onRestart }) {
  const { plan, parse_method, excel_file } = result

  return (
    <div className="fade-in min-h-screen bg-slate-50">
      {/* 顶部栏 */}
      <header className="border-b bg-white shadow-sm">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <h1 className="text-lg font-bold">🎉 学习计划已生成</h1>
          <button
            onClick={onRestart}
            className="rounded-lg px-3 py-1.5 text-sm font-medium text-slate-600 transition hover:bg-slate-100 hover:text-slate-900"
          >
            ← 重新制定
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-8">
        {/* 成功横幅 */}
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-500 px-6 py-5 text-white shadow">
          <div>
            <div className="text-base font-semibold">
              ✅ 已生成 {plan.length} 条计划，并导出到「{excel_file}」
            </div>
            <div className="mt-1 text-sm text-emerald-50">
              解析方式：{METHOD_LABEL[parse_method] ?? parse_method}
            </div>
          </div>
          <a
            href={downloadUrl()}
            download={excel_file}
            className="rounded-xl bg-white px-5 py-2.5 text-sm font-bold text-emerald-600 shadow transition hover:bg-emerald-50"
          >
            ⬇ 下载 Excel
          </a>
        </div>

        {/* 计划表格 */}
        <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-800 text-white">
              <tr>
                {COLUMNS.map((c) => (
                  <th
                    key={c.key}
                    className={`px-4 py-3 font-semibold ${c.width || ''}`}
                  >
                    {c.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {plan.map((row, i) => (
                <tr
                  key={i}
                  className={`align-top transition hover:bg-indigo-50/60 ${
                    i % 2 ? 'bg-slate-50' : 'bg-white'
                  }`}
                >
                  {COLUMNS.map((c) => (
                    <td
                      key={c.key}
                      className={`px-4 py-3 ${
                        c.key === '每日任务'
                          ? 'whitespace-pre-wrap text-slate-600'
                          : c.key === '课程名称'
                            ? 'font-semibold text-slate-800'
                            : c.key === '预计耗时'
                              ? 'whitespace-nowrap font-medium text-indigo-600'
                              : 'whitespace-nowrap text-slate-600'
                      }`}
                    >
                      {row[c.key] || '—'}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  )
}
