import { useState } from 'react'
import Landing from './components/Landing'
import StudentForm from './components/StudentForm'
import LoadingView from './components/LoadingView'
import ResultView from './components/ResultView'
import { generatePlan } from './api'

export default function App() {
  const [view, setView] = useState('landing') // landing | form | loading | result
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const handleSubmit = async (formData) => {
    setView('loading')
    setError('')
    try {
      const data = await generatePlan(formData)
      setResult(data)
      setView('result')
    } catch (e) {
      setError(e.message || '生成失败，请重试')
      setView('form')
    }
  }

  const reset = () => {
    setResult(null)
    setError('')
    setView('landing')
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      {view === 'landing' && <Landing onStart={() => setView('form')} />}
      {view === 'form' && (
        <StudentForm
          onSubmit={handleSubmit}
          onBack={reset}
          error={error}
        />
      )}
      {view === 'loading' && <LoadingView />}
      {view === 'result' && <ResultView result={result} onRestart={reset} />}
    </div>
  )
}
