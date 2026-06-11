<template>
  <div class="chat-panel">

    <!-- 会话工具栏 -->
    <div class="session-bar">
      <button class="sb-btn" @click="newChat" title="Clear and start new chat">＋ New</button>
      <button class="sb-btn" @click="onSave" title="Save current session" :disabled="!messages.length">
        💾 Save
      </button>
      <button class="sb-btn" @click="showSessions = true" title="Browse history">
        📂 History
      </button>
      <button
        class="sb-btn"
        :class="{ active: useRag }"
        @click="useRag = !useRag"
        title="Enable RAG context retrieval"
      >
        🧠 RAG
      </button>
      <span v-if="saveStatus" class="sb-status">{{ saveStatus }}</span>
    </div>

    <!-- 会话历史面板（覆盖） -->
    <SessionPanel
      v-if="showSessions"
      @close="showSessions = false"
      @load="onLoadSession"
    />

    <!-- 消息列表 -->
    <div class="messages" ref="messagesContainer">
      <div
        v-for="(m, i) in messages"
        :key="i"
        class="message"
        :class="m.role"
        :style="m.role === 'user' ? { '--msg-border': uiState.mode === 'plan' ? '#a371f7' : '#58a6ff' } : {}"
      >
        <div v-if="m.role !== 'user'" class="role-label">Agent：</div>

        <div class="content-bubble" :class="m.role === 'user' ? 'user-bubble' : ''">
          <div v-if="m.text" class="text" v-html="mdToHtml(m.text)"></div>

          <div v-if="m.thinking" class="thinking">
            {{ m.thinking }}
          </div>

          <div v-if="m.tools && m.tools.length" class="tools">
            <div
              v-for="(t, j) in m.tools"
              :key="j"
              class="tool"
              :class="t.type"
            >
              <div v-if="t.type === 'call'" class="tool-call">
                ▶ {{ t.name }}({{ JSON.stringify(t.args) }})
              </div>
              <div v-else class="tool-result"><pre class="tool-pre">{{ t.content }}</pre></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <InputBox @send="handleSend" />
  </div>
</template>

<script setup>
import { ref, nextTick, watch, onMounted } from 'vue'
import { streamChat } from '../api/chat'
import { saveSession, loadSession, withTimeout } from '../api/sessions'
import { clearMemory } from '../api/memory'
import InputBox from './InputBox.vue'
import SessionPanel from './SessionPanel.vue'
import { uiState } from '../stores/uiState'
import { uiActions } from '../stores/uiActions'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'

const md = new MarkdownIt({
  html: true,
  langPrefix: 'hljs language-',
  highlight(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre><code class="hljs language-${lang}">${hljs.highlight(code, { language: lang }).value}</code></pre>`
      } catch (_) {}
    }
    try {
      return `<pre><code class="hljs">${hljs.highlightAuto(code).value}</code></pre>`
    } catch (_) {}
    return ''
  }
})

function mdToHtml(text) {
  if (!text) return ''
  try {
    const html = md.render(text)
    return html
  } catch (e) {
    console.error('mdToHtml error:', e)
    return text
  }
}

const messages = ref([])
const messagesContainer = ref(null)
const showSessions = ref(false)
const saveStatus = ref('')
const useRag = ref(false)

watch(messages, () => {
  const raw = messages.value.map(m => ({ role: m.role, text: m.text }))
  localStorage.setItem('chat_messages', JSON.stringify(raw))
}, { deep: true })

onMounted(() => {
  const saved = localStorage.getItem('chat_messages')
  if (saved) {
    try {
      const restored = JSON.parse(saved)
      messages.value = restored.map(m => ({
        role: m.role,
        text: m.text,
        thinking: '',
        tools: []
      }))
      nextTick(scrollToBottom)
    } catch (_) {}
  }
})

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
    setupCopyButtons()
  })
}

function setupCopyButtons() {
  document.querySelectorAll('.text pre, .tool-pre').forEach(pre => {
    if (pre.querySelector('.copy-btn')) return
    pre.style.position = 'relative'
    const btn = document.createElement('button')
    btn.className = 'copy-btn'
    btn.textContent = '📋'
    Object.assign(btn.style, {
      position: 'absolute',
      top: '4px',
      right: '4px',
      background: '#1a1d2e',
      border: '1px solid #30363d',
      borderRadius: '4px',
      color: '#8b949e',
      cursor: 'pointer',
      fontSize: '12px',
      padding: '2px 6px',
      lineHeight: '1.4',
      opacity: '0.6',
      zIndex: '1'
    })
    btn.addEventListener('mouseenter', () => { btn.style.opacity = '1' })
    btn.addEventListener('mouseleave', () => { btn.style.opacity = '0.6' })
    btn.addEventListener('click', async () => {
      try {
        const code = pre.querySelector('code') || pre
        await navigator.clipboard.writeText(code.textContent || '')
        btn.textContent = '✓'
        setTimeout(() => { btn.textContent = '📋' }, 2000)
      } catch {
        btn.textContent = '✗'
        setTimeout(() => { btn.textContent = '📋' }, 2000)
      }
    })
    pre.appendChild(btn)
  })
}

// ─── Session actions ──────────────────────────────────────────────────────────

function newChat() {
  if (messages.value.length && !confirm('Clear current chat? Unsaved content will be lost.')) return
  messages.value = []
  localStorage.removeItem('chat_messages')
  clearMemory().catch(() => {})
}

async function onSave() {
  if (!messages.value.length) return
  const ctrl = withTimeout()
  try {
    const payload = messages.value
      .filter(m => m.role === 'user' || m.role === 'assistant')
      .map(m => ({ role: m.role, content: m.text }))
    await saveSession('', payload, ctrl.signal)
    localStorage.removeItem('chat_messages')
    saveStatus.value = '✓ Saved'
    setTimeout(() => { saveStatus.value = '' }, 2000)
  } catch (e) {
    console.error('save session error:', e)
    saveStatus.value = '✗ Save failed'
    setTimeout(() => { saveStatus.value = '' }, 2000)
  } finally {
    ctrl.cancel()
  }
}

async function onLoadSession(id) {
  const ctrl = withTimeout()
  try {
    const data = await loadSession(id, ctrl.signal)
    if (!data || !data.messages) return
    messages.value = data.messages.map(m => ({
      role: m.role,
      text: m.content || '',
      thinking: '',
      tools: []
    }))
    showSessions.value = false
    nextTick(scrollToBottom)
  } catch (e) {
    console.error('load session error:', e)
  } finally {
    ctrl.cancel()
  }
}

// ─── Chat ─────────────────────────────────────────────────────────────────────

function handleSend(text) {
  messages.value.push({
    role: 'user',
    text: text,
    thinking: '',
    tools: []
  })
  scrollToBottom()

  const assistantMsg = {
    role: 'assistant',
    text: '',
    thinking: '',
    tools: []
  }
  messages.value.push(assistantMsg)

  const assistantIndex = messages.value.length - 1
  scrollToBottom()

  streamChat(text, uiState.mode, (event) => {
    handleEvent(event, assistantIndex)
    scrollToBottom()
  }, useRag.value)
}

function handleEvent(e, assistantIndex) {
  const msg = messages.value[assistantIndex]
  if (!msg) return

  switch (e.type) {
    case 'token':
      msg.text += e.content
      break

    case 'thinking':
      msg.thinking = e.content
      break

    case 'tool_call':
      msg.tools.push({
        type: 'call',
        name: e.name,
        args: e.args
      })
      break

    case 'tool_result':
      msg.tools.push({
        type: 'result',
        name: e.name,
        content: e.content
      })

      if (e.name === 'patch_file') {
        uiActions.setDiff({
          old: uiState.previousCode,
          new: e.content
        })
      }
      break

    case 'plan_step':
      msg.tools.push({
        type: 'call',
        name: e.tool,
        args: e.args
      })
      msg.tools.push({
        type: 'result',
        name: e.tool,
        content: typeof e.result === 'string' ? e.result : JSON.stringify(e.result)
      })
      break

    case 'plan':
      msg.tools.push({
        type: 'result',
        name: 'Plan',
        content: JSON.stringify(e.content, null, 2)
      })
      break

    case 'error':
      msg.tools.push({
        type: 'result',
        name: 'Error',
        content: typeof e.content === 'string' ? e.content : JSON.stringify(e.content)
      })
      break
  }
}
</script>

<style scoped>
.chat-panel {
  width: 360px;
  background: #151822;
  border-left: none;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  position: relative;
}

/* ── Session bar ── */
.session-bar {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 8px;
  border-bottom: 1px solid #21262d;
  flex-shrink: 0;
}

.sb-btn {
  background: #1a1c24;
  border: 1px solid #30363d;
  border-radius: 4px;
  color: #8b949e;
  cursor: pointer;
  font-size: 11px;
  padding: 3px 8px;
  transition: color 0.15s, border-color 0.15s;
}

.sb-btn:hover:not(:disabled) {
  color: #e6edf3;
  border-color: #58a6ff;
}

.sb-btn:disabled {
  opacity: 0.4;
  cursor: default;
}

.sb-btn.active {
  color: #22c55e;
  border-color: #22c55e;
}

.sb-status {
  font-size: 11px;
  color: #22c55e;
  margin-left: 4px;
}

/* ── Messages ── */
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  min-height: 0;
  max-height: 100%;
}

.messages::-webkit-scrollbar {
  width: 8px;
}
.messages::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}
.messages::-webkit-scrollbar-track {
  background: transparent;
}

.message {
  margin-bottom: 16px;
}

.message.user {
  text-align: right;
}

.content-bubble {
  display: inline-block;
  text-align: left;
  max-width: 95%;
}

.content-bubble.user-bubble {
  border: 1px solid var(--msg-border);
  border-radius: 6px;
  background: #0f1117;
  padding: 8px 10px;
}

.role-label {
  font-size: 11px;
  color: #8b949e;
  margin-bottom: 4px;
}

.message.user .role-label {
  color: #58a6ff;
}

.message.assistant .role-label {
  color: #22c55e;
}

.text {
  font-size: 13px;
  line-height: 1.6;
  word-break: break-word;
}

.text :deep(*) {
  max-width: 100%;
}

.thinking {
  font-size: 11px;
  color: #8b949e;
  margin-top: 6px;
  font-style: italic;
  background: #0a0a0f;
  border-radius: 4px;
  padding: 6px 8px;
}

.tools {
  margin-top: 8px;
  background: #0a0a0f;
  border-radius: 4px;
  padding: 6px 8px;
}

.tool {
  font-size: 11px;
  margin-top: 4px;
}

.tool-call {
  color: #60a5fa;
}

.text :deep(h1),
.text :deep(h2),
.text :deep(h3),
.text :deep(h4) {
  margin: 10px 0 6px;
  color: #e6edf3;
}
.text :deep(h1) { font-size: 16px; }
.text :deep(h2) { font-size: 15px; }
.text :deep(h3) { font-size: 14px; }
.text :deep(h4) { font-size: 13px; }

.text :deep(p) {
  margin: 0 0 6px;
}

.text :deep(pre) {
  background: #0f1117;
  border-radius: 6px;
  padding: 10px 12px;
  overflow-x: auto;
  font-size: 12px;
  margin: 6px 0;
}

.text :deep(code) {
  font-family: 'Fira Code', 'Cascadia Code', monospace;
}

.text :deep(ul), .text :deep(ol) {
  padding-left: 18px;
  margin: 4px 0;
}

.text :deep(li) {
  margin: 2px 0;
}

.text :deep(a) {
  color: #58a6ff;
}

.text :deep(blockquote) {
  border-left: 3px solid #30363d;
  padding-left: 10px;
  color: #8b949e;
  margin: 6px 0;
}

.text :deep(table) {
  border-collapse: collapse;
  font-size: 12px;
}

.text :deep(th), .text :deep(td) {
  border: 1px solid #30363d;
  padding: 4px 8px;
}

.tool-pre {
  white-space: pre-wrap;
  word-break: break-all;
  color: #8b949e;
  margin: 0;
  font-size: 11px;
  font-family: monospace;
  max-height: 200px;
  overflow-y: auto;
}

/* ── highlight.js token colors ── */
.text :deep(.hljs) { background: #0f1117; color: #e6edf3; }
.text :deep(.hljs-keyword),
.text :deep(.hljs-selector-tag),
.text :deep(.hljs-built_in) { color: #ff7b72; }
.text :deep(.hljs-string),
.text :deep(.hljs-attr),
.text :deep(.hljs-template-variable) { color: #a5d6ff; }
.text :deep(.hljs-number),
.text :deep(.hljs-literal) { color: #79c0ff; }
.text :deep(.hljs-comment),
.text :deep(.hljs-quote) { color: #8b949e; font-style: italic; }
.text :deep(.hljs-function),
.text :deep(.hljs-title) { color: #d2a8ff; }
.text :deep(.hljs-variable),
.text :deep(.hljs-params) { color: #ffa657; }
.text :deep(.hljs-class .hljs-title),
.text :deep(.hljs-type) { color: #ffa657; }
.text :deep(.hljs-meta) { color: #79c0ff; }
.text :deep(.hljs-tag) { color: #7ee787; }
.text :deep(.hljs-name) { color: #7ee787; }
.text :deep(.hljs-property) { color: #79c0ff; }
.text :deep(.hljs-operator),
.text :deep(.hljs-punctuation) { color: #e6edf3; }
</style>
