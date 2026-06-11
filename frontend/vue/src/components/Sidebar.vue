<template>
  <div class="sidebar">
    <!-- 隐藏的文件选择器，始终存在 -->
    <input
      type="file"
      webkitdirectory
      ref="folderInput"
      class="folder-input"
      @change="onSelectRoot"
    />

    <div v-if="!treeData.length" class="empty-state">
      <label class="empty-clickable" @click="selectFolder">
        <span class="empty-icon">📁</span>
        <span class="empty-text">Select a folder...</span>
      </label>
    </div>

    <template v-else>
      <div class="tree-toolbar">
        <span class="tree-title">Files</span>
        <button class="tree-reload" @click="selectFolder">📂 Select a folder...</button>
      </div>
      <ul class="file-tree">
        <FileNode
          v-for="node in treeData"
          :key="node.path"
          :node="node"
        />
      </ul>
    </template>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import FileNode from './FileNode.vue'

const TREE_KEY = 'minicode_sidebar_tree'
const treeData = ref([])
const folderInput = ref(null)

function stripFile(obj) {
  return {
    name: obj.name,
    path: obj.path,
    file: null,
    isFolder: obj.isFolder,
    expanded: obj.expanded,
    hidden: obj.hidden,
    children: obj.children ? obj.children.map(stripFile) : []
  }
}

function saveTree() {
  try {
    localStorage.setItem(TREE_KEY, JSON.stringify(treeData.value.map(stripFile)))
  } catch {}
}

watch(treeData, saveTree, { deep: true })

onMounted(() => {
  try {
    const raw = localStorage.getItem(TREE_KEY)
    if (raw) {
      const restored = JSON.parse(raw)
      if (restored.length) treeData.value = restored
    }
  } catch {}
})

function selectFolder() {
  folderInput.value?.click()
}

function onSelectRoot(event) {
  const fileList = Array.from(event.target.files)
  if (!fileList.length) return

  const rootNodes = []

  fileList.forEach(file => {
    const parts = file.webkitRelativePath.split('/')
    let currentLevel = rootNodes
    let pathAcc = ''

    parts.forEach((part, idx) => {
      pathAcc = pathAcc ? pathAcc + '/' + part : part
      let existing = currentLevel.find(n => n.name === part)
      if (!existing) {
        existing = {
          name: part,
          path: pathAcc,
          file: idx === parts.length - 1 ? file : null,
          isFolder: idx !== parts.length - 1,
          children: [],
          expanded: idx === 0,
          hidden: part.startsWith('__') || part.startsWith('venv')
        }
        currentLevel.push(existing)
      }
      currentLevel = existing.children
    })
  })

  treeData.value = rootNodes
}
</script>

<style scoped>
.sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;
  min-width: 200px;
  max-width: 400px;
  overflow-x: auto;
  overflow-y: auto;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #484f58;
  user-select: none;
}

.empty-clickable {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.empty-clickable input[type="file"] {
  position: absolute;
  width: 1px;
  height: 1px;
  opacity: 0;
  overflow: hidden;
  z-index: -1;
}

.folder-input {
  display: none;
}

.tree-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 8px;
  border-bottom: 1px solid #21262d;
  flex-shrink: 0;
}

.tree-title {
  font-size: 12px;
  color: #8b949e;
  font-weight: 600;
}

.tree-reload {
  background: none;
  border: 1px solid #30363d;
  border-radius: 4px;
  color: #8b949e;
  cursor: pointer;
  font-size: 11px;
  padding: 2px 6px;
}

.tree-reload:hover {
  color: #e6edf3;
  border-color: #58a6ff;
}

.empty-icon {
  font-size: 24px;
}

.empty-text {
  font-size: 14px;
}

.file-tree {
  flex: 1;
  margin: 0;
  padding: 0;
  list-style: none;
  padding-top: 4px;
  white-space: nowrap;
}
</style>