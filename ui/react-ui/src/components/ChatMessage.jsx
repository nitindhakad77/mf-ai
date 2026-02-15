import React from 'react'

export default function ChatMessage({ role, content }) {
  const isUser = role === 'user'
  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} my-2`}>
      <div className={`max-w-[78ch] rounded-2xl border px-4 py-3 shadow-sm backdrop-blur         ${isUser ? 'bg-sky-500/15 border-sky-400/30' : 'bg-emerald-400/10 border-emerald-300/25'}
      `}>
        <div className="text-[11px] uppercase tracking-wide text-slate-300/80">
          {isUser ? 'You' : 'Assistant'}
        </div>
        <div className="mt-1 whitespace-pre-wrap leading-relaxed text-slate-100">
          {content}
        </div>
      </div>
    </div>
  )
}
