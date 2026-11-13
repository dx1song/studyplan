export default function LoadingView() {
  return (
    <div className="fade-in flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-indigo-600 via-violet-600 to-blue-700 px-6 text-center text-white">
      <div className="h-14 w-14 animate-spin rounded-full border-4 border-white/30 border-t-white" />
      <h1 className="mt-8 text-2xl font-bold">AI 正在为你生成学习计划…</h1>
      <p className="mt-3 max-w-md leading-relaxed text-indigo-100">
        正在分析你的情况，并规划 8 门课程的学习路线。
        <br />
        通常需要 <span className="font-semibold text-white">30 秒 ~ 2 分钟</span>，请稍候。
      </p>
    </div>
  )
}
