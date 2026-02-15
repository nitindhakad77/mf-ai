import React, { useEffect, useRef, useState } from 'react'
import { chat, latest, search as searchApi, health } from './api'
import ChatMessage from './components/ChatMessage'
import SidebarItem from './components/SidebarItem'

export default function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi! Ask me about the mainframe logs (e.g., “Why did ABC123 fail?”)' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [apiOk, setApiOk] = useState(null)

  const [latestItems, setLatestItems] = useState([])
  const [searchQ, setSearchQ] = useState('')
  const [searchItems, setSearchItems] = useState([])

  const bottomRef = useRef(null)

  useEffect(() => {
    (async () => {
      try { await health(); setApiOk(true) } catch { setApiOk(false) }
    })()
  }, [])

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages, loading])

  async function refreshLatest() {
    try {
      const res = await latest(10)
      setLatestItems(res.items || [])
    } catch (e) { console.error(e) }
  }

  async function doSearch() {
    if (!searchQ.trim()) return
    try {
      const res = await searchApi(searchQ.trim(), 10)
      setSearchItems(res.items || [])
    } catch (e) { console.error(e) }
  }

  async function onSend(e) {
    e.preventDefault()
    const q = input.trim()
    if (!q || loading) return

    setMessages(prev => [...prev, { role: 'user', content: q }])
    setInput('')
    setLoading(true)

    try {
      const res = await chat(q)
      setMessages(prev => [...prev, { role: 'assistant', content: res.answer || '' }])
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${err.message}` }])
    } finally {
      setLoading(false)
    }
  }

  const pill = apiOk === null
    ? { text: 'Checking API…', cls: 'bg-white/5 border-white/10 text-slate-300' }
    : apiOk
      ? { text: 'API Connected', cls: 'bg-emerald-500/10 border-emerald-400/30 text-emerald-200' }
      : { text: 'API Not Reachable', cls: 'bg-rose-500/10 border-rose-400/30 text-rose-200' }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="pointer-events-none fixed inset-0">
        <div className="absolute -top-24 left-1/2 h-[380px] w-[780px] -translate-x-1/2 rounded-full bg-gradient-to-r from-sky-500/20 via-indigo-500/15 to-emerald-400/15 blur-3xl" />
      </div>

      <div className="relative mx-auto grid min-h-screen max-w-[1400px] grid-cols-1 lg:grid-cols-[360px_1fr]">
        <aside className="hidden lg:flex flex-col gap-4 border-r border-white/10 bg-white/[0.03] p-5">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm font-extrabold tracking-wide">POC MF AI</div>
              <div className="text-xs text-slate-300">Hackathon UI (Tailwind)</div>
            </div>
            <div className={`rounded-full border px-3 py-1 text-[11px] ${pill.cls}`}>{pill.text}</div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="mb-3 flex items-center justify-between">
              <div className="text-sm font-semibold">Latest Summaries</div>
              <button className="rounded-xl border border-white/10 bg-white/5 px-3 py-1.5 text-xs hover:bg-white/10" onClick={refreshLatest}>
                Refresh
              </button>
            </div>
            <div className="grid gap-3">
              {latestItems.length === 0 ? (
                <div className="text-xs text-slate-300">No items yet. Run ingestor + processor.</div>
              ) : latestItems.slice(0, 6).map((it) => (
                <SidebarItem key={it.id} title={it.filename || 'log'} subtitle={(it.summary || '').slice(0, 140)} />
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="mb-2 text-sm font-semibold">Search</div>
            <div className="flex gap-2">
              <input
                className="w-full rounded-xl border border-white/10 bg-slate-900/40 px-3 py-2 text-sm outline-none placeholder:text-slate-400 focus:border-sky-400/40"
                placeholder="ABEND / RC= / JOBNAME"
                value={searchQ}
                onChange={(e) => setSearchQ(e.target.value)}
                onKeyDown={(e) => (e.key === 'Enter' ? doSearch() : null)}
              />
              <button className="rounded-xl bg-sky-500/20 px-3 py-2 text-sm font-semibold text-sky-100 hover:bg-sky-500/30" onClick={doSearch}>
                Go
              </button>
            </div>
            <div className="mt-3 grid gap-3">
              {searchItems.slice(0, 6).map((it) => (
                <SidebarItem key={`s-${it.id}`} title={it.filename || 'log'} subtitle={(it.summary || '').slice(0, 140)} />
              ))}
            </div>
            <div className="mt-4 text-xs text-slate-400">Set <code className="text-sky-300">VITE_API_BASE</code> in <code className="text-sky-300">.env</code></div>
          </div>
        </aside>

        <main className="flex min-h-screen flex-col">
          <header className="border-b border-white/10 bg-white/[0.03] px-5 py-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-base font-extrabold">Mainframe Log Chatbot</div>
                <div className="text-xs text-slate-300">FastAPI backend + Bedrock summaries</div>
              </div>
              <div className={`rounded-full border px-3 py-1 text-[11px] lg:hidden ${pill.cls}`}>{pill.text}</div>
            </div>
          </header>

          <section className="flex-1 overflow-auto px-5 py-4">
            {messages.map((m, idx) => <ChatMessage key={idx} role={m.role} content={m.content} />)}
            {loading && <ChatMessage role="assistant" content="Thinking…" />}
            <div ref={bottomRef} />
          </section>

          <form onSubmit={onSend} className="border-t border-white/10 bg-white/[0.03] px-5 py-4">
            <div className="flex gap-2">
              <input
                className="w-full rounded-2xl border border-white/10 bg-slate-900/40 px-4 py-3 text-sm outline-none placeholder:text-slate-400 focus:border-sky-400/40"
                placeholder='Ask: "Why did JOB ABC123 fail?"'
                value={input}
                onChange={(e) => setInput(e.target.value)}
              />
              <button
                type="submit"
                disabled={loading}
                className="rounded-2xl bg-gradient-to-r from-sky-500/40 to-emerald-400/30 px-5 py-3 text-sm font-bold text-white hover:from-sky-500/55 hover:to-emerald-400/40 disabled:opacity-60"
              >
                Send
              </button>
            </div>
            <div className="mt-2 text-[11px] text-slate-400">Tip: Try <span className="text-slate-200">"Show recent abends"</span> or <span className="text-slate-200">"What caused RC=08"</span>.</div>
          </form>
        </main>
      </div>
    </div>
  )
}
