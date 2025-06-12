<template>
  <div class="dashboard-container">
    <div class="back-button" @click="$router.push('/')">
      <span class="back-icon">←</span>
      <span>返回主页</span>
    </div>
    
    <div class="logout-button" @click="handleLogout">
      <span class="logout-icon">⤫</span>
      <span>退出账号</span>
    </div>
    
    <div class="dashboard">
      <div class="header-section">
        <h1>用户控制台</h1>
      </div>
      
      <div class="user-info">
        <h2>欢迎回来，<span class="highlight">{{ username }}</span></h2>
        <p>邮箱账号: {{ authStore.userEmail }}</p>
      </div>
      
      <div class="dashboard-content">
        <div class="dashboard-card">
          <h3>我的余额</h3>
          <div class="balance">
            <span class="amount">0</span>
            <span class="unit">积分</span>
          </div>
          <button class="btn-primary">充值</button>
        </div>
        
        <div class="dashboard-card">
          <h3>文生图</h3>
          <p>通过文字描述生成图像</p>
          <button class="btn-primary" @click="$router.push('/')">开始创作</button>
        </div>
        
        <div class="dashboard-card">
          <h3>历史记录</h3>
          <p>查看已生成的图片</p>
          <button class="btn-secondary">浏览历史</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

// 获取用户名
const username = computed(() => {
  if (authStore.user?.username) {
    return authStore.user.username
  }
  // 如果没有名字，使用邮箱前缀作为用户名
  return authStore.userEmail.split('@')[0]
})

// 退出登录
const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  width: 100%;
  background-color: #121212;
  color: #f5f5f5;
  position: relative;
  padding-top: 2rem;
}

.back-button {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: rgba(230, 126, 34, 0.15);
  color: #e67e22;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
  z-index: 100;
}

.back-button:hover {
  background-color: rgba(230, 126, 34, 0.25);
  transform: translateX(-4px);
}

.back-icon {
  font-size: 1.2rem;
}

.logout-button {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: rgba(211, 47, 47, 0.15);
  color: #ff5252;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
  z-index: 100;
}

.logout-button:hover {
  background-color: rgba(211, 47, 47, 0.25);
  transform: translateX(4px);
}

.logout-icon {
  font-size: 1.2rem;
}

.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.header-section {
  margin-bottom: 2rem;
  text-align: center;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  background: linear-gradient(90deg, #f5c518, #e67e22);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}

.user-info {
  background-color: #1a1a1a;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2.5rem;
  border: 1px solid #333;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.user-info h2 {
  margin: 0 0 1rem 0;
  color: #f5f5f5;
  font-size: 1.5rem;
}

.highlight {
  color: #e67e22;
}

.user-info p {
  margin: 0;
  color: #aaa;
}

.dashboard-content {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.dashboard-card {
  background-color: #1a1a1a;
  border-radius: 12px;
  border: 1px solid #333;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s, box-shadow 0.3s;
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(230, 126, 34, 0.2);
}

.dashboard-card h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #e67e22;
  font-size: 1.3rem;
}

.dashboard-card p {
  margin-bottom: 1.5rem;
  color: #aaa;
  flex-grow: 1;
}

.balance {
  display: flex;
  align-items: baseline;
  margin-bottom: 2rem;
}

.amount {
  font-size: 3rem;
  font-weight: bold;
  color: #e67e22;
  margin-right: 0.5rem;
}

.unit {
  color: #aaa;
  font-size: 1.2rem;
}

.btn-primary, .btn-secondary {
  padding: 0.9rem 1rem;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
}

.btn-primary {
  background-color: #e67e22;
  color: #fff;
}

.btn-primary:hover {
  background-color: #f5c518;
}

.btn-secondary {
  background-color: rgba(230, 126, 34, 0.15);
  color: #e67e22;
  border: 1px solid #e67e22;
}

.btn-secondary:hover {
  background-color: rgba(230, 126, 34, 0.3);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .dashboard-content {
    grid-template-columns: 1fr;
  }
  
  .back-button {
    top: 1rem;
    left: 1rem;
  }
  
  .logout-button {
    top: 1rem;
    right: 1rem;
  }
}
</style> 