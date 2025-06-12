<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'

// 初始化认证状态
const authStore = useAuthStore()

onMounted(() => {
  authStore.initializeAuth()
})
</script>

<template>
  <RouterView />
</template>

<style>
/* 全局样式 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

#app {
  width: 100%;
  height: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

body {
  font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  line-height: 1.6;
  color: #f8f8f8;
  background-color: #121212;
  margin: 0;
  padding: 0;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}

/* 修正移动端字体大小问题 */
html {
  font-size: 16px;
  -webkit-text-size-adjust: 100%;
}

button {
  font-family: inherit;
  cursor: pointer;
}

textarea, input {
  font-family: inherit;
}

/* 统一滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #1e1e1e;
}

::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #444;
}

/* 选中文本样式 */
::selection {
  background: rgba(230, 126, 34, 0.3);
  color: #fff;
}

/* 平滑滚动 */
html {
  scroll-behavior: smooth;
}

/* 焦点样式 */
:focus {
  outline: none;
}

:focus-visible {
  outline: 2px solid rgba(230, 126, 34, 0.5);
  outline-offset: 2px;
}
</style>
