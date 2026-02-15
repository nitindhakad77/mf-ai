import React from 'react'

export default function SidebarItem({ title, subtitle }) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-3 hover:bg-white/10 transition">
      <div className="text-xs font-semibold text-slate-100 truncate">{title}</div>
      {subtitle && (
        <div className="mt-1 text-[11px] leading-snug text-slate-300">
          {subtitle}
        </div>
      )}
    </div>
  )
}
