export async function clearMemory(signal) {
  const res = await fetch('/api/memory/clear', { method: 'POST', signal })
  if (!res.ok) throw new Error('clear memory failed')
  return res.json()
}
