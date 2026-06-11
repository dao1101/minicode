import { reactive } from 'vue'

const STORAGE_KEY = 'minicode_editor_state'

function loadPersisted() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) return JSON.parse(raw)
  } catch {}
  return {}
}

const persisted = loadPersisted()

export const uiState = reactive({
  mode: 'build',
  activePanel: 'editor',
  currentFile: persisted.currentFile || null,
  currentCode: persisted.currentCode || '',
  files: [],
  diff: persisted.diff || null,
  previousCode: ''
})

export function persistUiState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      currentFile: uiState.currentFile,
      currentCode: uiState.currentCode,
      diff: uiState.diff,
    }))
  } catch {}
}