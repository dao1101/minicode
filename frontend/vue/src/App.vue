<template>
  <div class="layout" :class="{ 'is-resizing': !!resizing, 'chat-fullscreen': isChatFullscreen }">
    <div class="topbar">
      <div class="logo">MINICODE V1.12.5</div>
    </div>

    <div class="main">
      <div v-show="!isSidebarCollapsed" class="sidebar" :style="{ width: sidebarWidth + 'px' }">
        <Sidebar />
        <button class="toggle-btn left" @click="isSidebarCollapsed = true">◀</button>
      </div>

      <div v-if="!isSidebarCollapsed" class="resizer" @mousedown="startLeftResize"></div>

      <div v-show="!isChatFullscreen" class="editor" :style="{ width: editorWidth + 'px' }">
        <Editor />
        <button v-if="isSidebarCollapsed" class="toggle-btn expand-sidebar" @click="isSidebarCollapsed = false">▶</button>
        <button class="toggle-btn collapse-editor" @click="isChatFullscreen = true">◀</button>
      </div>

      <div class="chat-wrapper">
        <div class="chat" :style="{ width: isChatFullscreen ? '100%' : CHAT_WIDTH + 'px' }">
          <Chat />
        </div>
        <button v-if="isChatFullscreen" class="toggle-btn restore" @click="isChatFullscreen = false">▶</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import Sidebar from './components/Sidebar.vue'
import Editor from './components/Editor.vue'
import Chat from './components/Chat.vue'

const MIN_SIDEBAR = 180
const MIN_EDITOR = 200
const CHAT_WIDTH = 360

const sidebarWidth = ref(Number(localStorage.getItem('sidebarWidth')) || 260)
const editorWidth = ref(0)
const isSidebarCollapsed = ref(false)
const isChatFullscreen = ref(false)
const resizing = ref(null)

watch(sidebarWidth, () => {
  localStorage.setItem('sidebarWidth', sidebarWidth.value)
})

function updateEditorWidth() {
  const activeSidebarWidth = isSidebarCollapsed.value ? 0 : sidebarWidth.value
  editorWidth.value = Math.max(
    MIN_EDITOR,
    window.innerWidth - activeSidebarWidth - CHAT_WIDTH - 6
  )
}

function onMouseMove(e) {
  if (!resizing.value) return
  const maxAllowed = window.innerWidth - CHAT_WIDTH - MIN_EDITOR
  sidebarWidth.value = Math.max(MIN_SIDEBAR, Math.min(maxAllowed, e.clientX))
  updateEditorWidth()
}

function startLeftResize() {
  resizing.value = 'left'
  document.body.classList.add('is-resizing')
  initListeners()
}

function stopResize() {
  resizing.value = null
  document.body.classList.remove('is-resizing')
  document.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', stopResize)
}

function initListeners() {
  document.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', stopResize)
}

onMounted(() => {
  updateEditorWidth()
  window.addEventListener('resize', updateEditorWidth)
})
onUnmounted(() => {
  stopResize()
  window.removeEventListener('resize', updateEditorWidth)
})
</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: #0f1117;
}

.topbar {
  height: 36px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0f1117;
  border-bottom: 1px solid #21262d;
}

.logo {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #58a6ff;
  user-select: none;
}

.main {
  display: flex;
  flex: 1;
  min-height: 0;
}

.sidebar {
  position: relative;
  flex-shrink: 0;
  overflow: hidden;
  transition: width 0.2s;
}

.editor {
  background: #1a1c24;
  min-width: 200px;
  position: relative;
}

.chat-wrapper {
  position: relative;
  flex-shrink: 0;
  display: flex;
  align-items: stretch;
}

.chat {
  flex-shrink: 0;
  position: relative;
  background: #151822;
  transition: width 0.2s;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.resizer {
  width: 3px;
  cursor: col-resize;
  background: transparent;
  position: relative;
}
.resizer::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 1px;
  background: rgba(255,255,255,0.08);
  transform: translateX(-50%);
}
.resizer:hover {
  background: rgba(88,166,255,0.2);
}

body.is-resizing .resizer {
  background: rgba(88,166,255,0.4);
}

.chat-fullscreen .sidebar,
.chat-fullscreen .resizer,
.chat-fullscreen .editor {
  display: none;
}
.chat-fullscreen .chat-wrapper {
  flex: 1;
}

.toggle-btn {
  position: absolute;
  bottom: 12px;
  z-index: 20;
  color: white;
  cursor: pointer;
  padding: 1px 2px;
  border-radius: 3px;
  font-size: 10px;
  border: none;
}
.toggle-btn.left { right: 10px; background: #0f1117; }
.toggle-btn.expand-sidebar { left: 10px; background: #1a1c24; }
.toggle-btn.collapse-editor { right: 10px; background: #1a1c24; }
.toggle-btn.restore { left: 4px; background: #151822; }
</style>

<style>
.chat-fullscreen .chat-panel {
  width: 100% !important;
}
</style>
