import { uiState, persistUiState } from './uiState'

export const uiActions = {
  toggleMode() {
    uiState.mode = uiState.mode === 'build' ? 'plan' : 'build'
  },

  setCurrentFile(file, code) {
    uiState.previousCode = uiState.currentCode
    uiState.currentFile = file
    uiState.currentCode = code
    uiState.diff = null
    persistUiState()
  },

  setDiff(diff) {
    uiState.diff = diff
  },

  clearDiff() {
    uiState.diff = null
  },

  setFiles(files) {
    uiState.files = files
  }
}