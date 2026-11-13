const COURSES = [
  { icon: '💻', name: 'vibe coding项目开发', desc: 'AI 辅助编码与项目实战' },
  { icon: '🔧', name: 'AI应用全栈开发基础', desc: '前后端全栈开发能力' },
  { icon: '🤖', name: 'RAG智能体开发', desc: '检索增强与智能体开发' },
  { icon: '🏗️', name: '企业工程化能力（Java）', desc: 'Java 企业级工程化' },
  { icon: '⚙️', name: 'AI工程化-微服务智能体实战', desc: '微服务智能体工程化实战' },
  { icon: '🔄', name: '传统项目的智能化升级', desc: '传统项目智能化改造' },
  { icon: '📈', name: 'AI应用评估与模型调优', desc: '应用评估与模型调优' },
  { icon: '🎯', name: '面试指导与就业加强', desc: '面试指导与就业提升' },
]

const STEPS = [
  { n: '01', t: '填写信息', d: '告诉我们你的水平与目标' },
  { n: '02', t: 'AI 生成', d: '为你定制每日 / 每周计划' },
  { n: '03', t: '下载计划', d: '一键导出 学习计划.xlsx' },
]

export default function Landing({ onStart }) {
  return (
    <div className="fade-in min-h-screen bg-gradient-to-br from-indigo-600 via-violet-600 to-blue-700 text-white">
      {/* 顶部导航 */}
      <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
        <div className="flex items-center gap-2.5 text-lg font-bold">
          <span className="grid h-10 w-10 place-items-center rounded-xl bg-white/15 text-xl shadow-inner">
            🎓
          </span>
          <span>AI 学习计划</span>
        </div>
        <span className="hidden rounded-full bg-white/10 px-4 py-1.5 text-sm text-indigo-100 sm:inline">
          由大模型驱动
        </span>
      </header>

      {/* Hero 区 */}
      <section className="mx-auto max-w-6xl px-6 pb-16 pt-14 text-center sm:pt-20">
        <span className="inline-flex items-center gap-2 rounded-full bg-white/15 px-4 py-1.5 text-sm font-medium backdrop-blur">
          ✨ AI 驱动 · 个性化学习路线
        </span>
        <h1 className="mx-auto mt-7 max-w-3xl text-4xl font-extrabold leading-tight sm:text-5xl">
          你的专属
          <span className="bg-gradient-to-r from-amber-200 to-orange-300 bg-clip-text text-transparent">
            {' '}AI 学习计划{' '}
          </span>
          生成器
        </h1>
        <p className="mx-auto mt-5 max-w-2xl text-lg leading-relaxed text-indigo-100">
          只需几步，AI 将结合 8 门系统课程，为你量身定制一份可落地的学习路线与每日实施方案。
        </p>

        <button
          onClick={onStart}
          className="mt-10 rounded-full bg-white px-9 py-4 text-lg font-bold text-indigo-700 shadow-xl shadow-indigo-900/30 transition hover:scale-105 hover:bg-indigo-50"
        >
          开始制定计划 <span className="ml-1">→</span>
        </button>

        {/* 三步说明 */}
        <div className="mx-auto mt-16 grid max-w-3xl gap-4 sm:grid-cols-3">
          {STEPS.map((s) => (
            <div
              key={s.n}
              className="rounded-2xl bg-white/10 p-5 text-left backdrop-blur transition hover:bg-white/15"
            >
              <div className="text-2xl font-extrabold text-amber-300">{s.n}</div>
              <div className="mt-2 font-semibold">{s.t}</div>
              <div className="mt-1 text-sm text-indigo-100">{s.d}</div>
            </div>
          ))}
        </div>
      </section>

      {/* 课程列表 */}
      <section className="mx-auto max-w-6xl px-6 pb-20">
        <h2 className="text-center text-2xl font-bold">你将系统学习这 8 门课程</h2>
        <p className="mt-2 text-center text-indigo-100">
          课程内容固定，AI 会根据你的情况个性化安排学习节奏
        </p>
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {COURSES.map((c) => (
            <div
              key={c.name}
              className="rounded-2xl bg-white/10 p-5 backdrop-blur transition hover:-translate-y-1 hover:bg-white/20"
            >
              <div className="text-3xl">{c.icon}</div>
              <div className="mt-3 font-semibold leading-snug">{c.name}</div>
              <div className="mt-1 text-sm text-indigo-100">{c.desc}</div>
            </div>
          ))}
        </div>

        <div className="mt-14 text-center">
          <button
            onClick={onStart}
            className="rounded-full border-2 border-white/60 px-8 py-3 text-base font-semibold transition hover:bg-white/10"
          >
            开始制定我的计划
          </button>
        </div>
      </section>

      <footer className="border-t border-white/10 py-6 text-center text-sm text-indigo-200">
        AI 个性化学习计划生成系统 · 为你量身定制可落地的学习路线
      </footer>
    </div>
  )
}
