const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function health() {
  const r = await fetch(`${API_BASE}/health`)
  if (!r.ok) throw new Error('health failed')
  return r.json()
}

export async function latest(limit = 10) {
  const r = await fetch(`${API_BASE}/latest?limit=${limit}`)
  if (!r.ok) throw new Error('latest failed')
  return r.json()
}

export async function search(q, limit = 10) {
  const url = new URL(`${API_BASE}/search`)
  url.searchParams.set('q', q)
  url.searchParams.set('limit', String(limit))
  const r = await fetch(url)
  if (!r.ok) throw new Error('search failed')
  return r.json()
}

export async function chat(question) {
  const r = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  })
  if (!r.ok) {
    const t = await r.text()
    throw new Error(t || 'chat failed')
  }
  return r.json()
}
