export async function fetchSessions(q = '') {
  const res = await fetch(`/api/sessions?q=${encodeURIComponent(q)}`)
  if (!res.ok) throw new Error('fetch sessions failed')
  return res.json()
}

export async function saveSession(title, messages) {
  const res = await fetch('/api/sessions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, messages })
  })
  if (!res.ok) throw new Error('save session failed')
  return res.json()
}

export async function loadSession(id) {
  const res = await fetch(`/api/sessions/${id}`)
  if (!res.ok) throw new Error('load session failed')
  return res.json()
}

export async function deleteSession(id) {
  const res = await fetch(`/api/sessions/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('delete session failed')
  return res.json()
}
