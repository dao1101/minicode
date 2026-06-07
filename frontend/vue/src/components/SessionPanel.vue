<template>
  <div class="session-panel">
    <div class="sp-header">
      <span class="sp-title-text">历史会话</span>
      <input
        v-model="query"
        class="sp-search"
        placeholder="🔍 搜索..."
        @input="onSearch"
      />
      <button
        class="sp-btn-mode"
        :class="{ active: semantic }"
        @click="semantic = !semantic; reload()"
        title="语义搜索"
      >
        🔍⇄
      </button>
      <button class="sp-close" @click="$emit('close')">✕</button>
    </div>

    <div v-if="loading" class="sp-empty">加载中...</div>

    <div v-else-if="sessions.length" class="sp-list">
      <div
        v-for="s in sessions"
        :key="s.id"
        class="sp-item"
        @click="$emit('load', s.id)"
      >
        <div class="sp-item-title">{{ s.title }}</div>
        <div class="sp-item-meta">{{ formatDate(s.created_at) }} · {{ s.count }} 条消息</div>
        <button class="sp-del" @click.stop="onDelete(s.id)" title="删除">🗑</button>
      </div>
    </div>

    <div v-else class="sp-empty">
      {{ query ? '无匹配结果' : '暂无历史会话' }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { fetchSessions, deleteSession, searchSessions, withTimeout } from '../api/sessions'

const emit = defineEmits(['close', 'load'])

const sessions = ref([])
const query = ref('')
const semantic = ref(false)
const loading = ref(false)
let debounceTimer = null

async function reload() {
  const ctrl = withTimeout()
  loading.value = true
  try {
    if (semantic.value && query.value) {
      sessions.value = await searchSessions(query.value, true, ctrl.signal)
    } else {
      sessions.value = await fetchSessions(query.value, ctrl.signal)
    }
  } catch (e) {
    console.error('load sessions error:', e)
  } finally {
    loading.value = false
    ctrl.cancel()
  }
}

function onSearch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(reload, 300)
}

onUnmounted(() => clearTimeout(debounceTimer))

async function onDelete(id) {
  if (!confirm('确认删除这条会话？')) return
  const ctrl = withTimeout()
  try {
    await deleteSession(id, ctrl.signal)
    await reload()
  } catch (e) {
    console.error('delete session error:', e)
  } finally {
    ctrl.cancel()
  }
}

function formatDate(iso) {
  if (!iso) return ''
  return iso.replace('T', ' ')
}

onMounted(reload)
</script>

<style scoped>
.session-panel {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #151822;
  z-index: 50;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #21262d;
}

.sp-header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 10px;
  border-bottom: 1px solid #21262d;
  flex-shrink: 0;
}

.sp-title-text {
  font-size: 12px;
  color: #8b949e;
  white-space: nowrap;
}

.sp-search {
  flex: 1;
  background: #0f1117;
  border: 1px solid #30363d;
  border-radius: 4px;
  color: #e6edf3;
  padding: 4px 8px;
  font-size: 12px;
  outline: none;
}

.sp-search:focus {
  border-color: #58a6ff;
}

.sp-close {
  background: none;
  border: none;
  color: #8b949e;
  cursor: pointer;
  font-size: 14px;
  line-height: 1;
  padding: 2px 4px;
}

.sp-close:hover {
  color: #e6edf3;
}

.sp-btn-mode {
  background: none;
  border: 1px solid #30363d;
  border-radius: 4px;
  color: #8b949e;
  cursor: pointer;
  font-size: 12px;
  padding: 2px 6px;
  line-height: 1.4;
  transition: color 0.15s, border-color 0.15s;
}

.sp-btn-mode:hover {
  color: #e6edf3;
  border-color: #58a6ff;
}

.sp-btn-mode.active {
  color: #22c55e;
  border-color: #22c55e;
}

.sp-list {
  flex: 1;
  overflow-y: auto;
  padding: 6px;
}

.sp-list::-webkit-scrollbar {
  width: 6px;
}

.sp-list::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 3px;
}

.sp-item {
  position: relative;
  padding: 8px 32px 8px 10px;
  margin-bottom: 4px;
  border-radius: 5px;
  cursor: pointer;
  background: #1a1c24;
  border: 1px solid #21262d;
  transition: border-color 0.15s;
}

.sp-item:hover {
  border-color: #58a6ff;
}

.sp-item-title {
  font-size: 13px;
  color: #e6edf3;
  margin-bottom: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sp-item-meta {
  font-size: 11px;
  color: #484f58;
}

.sp-del {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #484f58;
  cursor: pointer;
  font-size: 13px;
  opacity: 0;
  transition: opacity 0.15s;
  padding: 2px;
}

.sp-item:hover .sp-del {
  opacity: 1;
}

.sp-del:hover {
  color: #f85149;
}

.sp-empty {
  color: #484f58;
  text-align: center;
  margin-top: 50px;
  font-size: 13px;
}
</style>
