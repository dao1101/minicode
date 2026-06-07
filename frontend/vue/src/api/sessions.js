export function withTimeout(ms = 10000) {
  const ctrl = new AbortController()
  const timer = setTimeout(() => ctrl.abort(), ms)
  ctrl.cancel = () => clearTimeout(timer)
  return ctrl
}

export async function fetchSessions(q = '', signal) {
  const res = await fetch(`/api/sessions?q=${encodeURIComponent(q)}`, { signal })
  if (!res.ok) throw new Error('fetch sessions failed')
  return res.json()
}

export async function saveSession(title, messages, signal) {
  const res = await fetch('/api/sessions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, messages }),
    signal
  })
  if (!res.ok) throw new Error('save session failed')
  return res.json()
}

export async function loadSession(id, signal) {
  const res = await fetch(`/api/sessions/${id}`, { signal })
  if (!res.ok) throw new Error('load session failed')
  return res.json()
}

export async function deleteSession(id, signal) {
  const res = await fetch(`/api/sessions/${id}`, { method: 'DELETE', signal })
  if (!res.ok) throw new Error('delete session failed')
  return res.json()
}

export async function searchSessions(q, semantic = false, signal) {
  const res = await fetch(`/api/sessions/search?q=${encodeURIComponent(q)}&semantic=${semantic}`, { signal })
  if (!res.ok) throw new Error('search sessions failed')
  return res.json()
}
