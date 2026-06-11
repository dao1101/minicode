<template>
  <div class="editor-wrapper">
    <div v-if="!uiState.currentFile && !uiState.diff" class="empty-state">
      <div class="empty-icon">📝</div>
      <div class="empty-text">Select a file to edit</div>
    </div>

    <div v-else class="editor-body">
      <div class="editor-header">{{ uiState.currentFile }}</div>
      <div v-if="uiState.diff" class="diff-view">
        <div class="diff-pane">
          <div class="diff-label">Old</div>
          <pre><code>{{ uiState.diff.old }}</code></pre>
        </div>
        <div class="diff-pane">
          <div class="diff-label">New</div>
          <pre><code>{{ uiState.diff.new }}</code></pre>
        </div>
      </div>
      <pre v-else class="editor-code"><code>{{ uiState.currentCode }}</code></pre>
    </div>
  </div>
</template>

<script setup>
import { uiState } from '../stores/uiState'
</script>

<style scoped>
.editor-wrapper { flex: 1; height: 100%; position: relative; background: #0f1117; overflow: auto; }
.empty-state { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #484f58; pointer-events: none; }
.empty-icon { font-size: 24px; margin-bottom: 12px; }
.empty-text { font-size: 14px; }
.editor-body { height: 100%; display: flex; flex-direction: column; }
.editor-header { padding: 8px 12px; font-size: 12px; color: #8b949e; border-bottom: 1px solid #21262d; flex-shrink: 0; }
.editor-code { flex: 1; margin: 0; padding: 12px; overflow: auto; font-size: 13px; line-height: 1.5; color: #e6edf3; }
.editor-code code { font-family: 'Fira Code', 'Cascadia Code', monospace; white-space: pre; }
.diff-view { flex: 1; display: flex; overflow: auto; }
.diff-pane { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.diff-pane + .diff-pane { border-left: 1px solid #21262d; }
.diff-label { padding: 6px 10px; font-size: 11px; color: #8b949e; border-bottom: 1px solid #21262d; flex-shrink: 0; }
.diff-pane pre { flex: 1; margin: 0; padding: 10px; overflow: auto; font-size: 12px; line-height: 1.5; color: #e6edf3; }
.diff-pane code { font-family: 'Fira Code', 'Cascadia Code', monospace; white-space: pre; }
</style>