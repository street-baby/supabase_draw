<template>
  <div class="auth-container">
    <div class="back-button" @click="$router.push('/')">
      <span class="back-icon">←</span>
      <span>返回主页</span>
    </div>
    
    <div class="left-side">
      <h1>AI文生图平台</h1>
      <p class="slogan">通过文字描述，轻松创建属于你的专属图像</p>
      <div class="features">
        <div class="feature">
          <div class="icon">🎨</div>
          <div class="feature-text">
            <h3>AI 驱动创作</h3>
            <p>使用先进的人工智能技术，将你的文字描述转化为精美图像</p>
          </div>
        </div>
        <div class="feature">
          <div class="icon">⚡</div>
          <div class="feature-text">
            <h3>高速生成</h3>
            <p>只需几秒钟，即可获得高质量的AI生成图像</p>
          </div>
        </div>
        <div class="feature">
          <div class="icon">🔐</div>
          <div class="feature-text">
            <h3>安全可靠</h3>
            <p>保护你的创作和隐私，安全且值得信赖</p>
          </div>
        </div>
      </div>
    </div>
    
    <div class="right-side">
      <div class="form-container">
        <LoginForm
          title="登录账号"
          submitButtonText="登录"
          :loading="authStore.loading"
          @submit="handleSubmit"
        >
          <template #form-footer>
            <p>还没有账号？<router-link to="/register">立即注册</router-link></p>
          </template>
        </LoginForm>
        
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginForm from '@/components/LoginForm.vue'

const router = useRouter()
const authStore = useAuthStore()
const errorMessage = ref('')

const handleSubmit = async (formData: { email: string, code: string }) => {
  errorMessage.value = ''
  
  const success = await authStore.loginWithCode(formData.email, formData.code)
  
  if (success) {
    // 登录成功后跳转到首页
    router.push('/')
  } else {
    errorMessage.value = '登录失败，请检查邮箱和验证码是否正确'
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  min-height: 100vh;
  background-color: #121212;
}

.left-side {
  flex: 1;
  padding: 2rem 4rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: #f5f5f5;
  background-color: #1a1a1a;
}

.left-side h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  background: linear-gradient(90deg, #f5c518, #e67e22);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}

.slogan {
  font-size: 1.2rem;
  margin-bottom: 3rem;
  color: #aaa;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.feature {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.icon {
  font-size: 2rem;
  background: #232323;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.feature-text h3 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #f5f5f5;
}

.feature-text p {
  color: #aaa;
  font-size: 0.95rem;
  line-height: 1.6;
}

.right-side {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  background-color: #121212;
}

.form-container {
  width: 100%;
  max-width: 400px;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: rgba(211, 47, 47, 0.2);
  color: #ff6b6b;
  border-radius: 8px;
  text-align: center;
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

/* 响应式调整 */
@media (max-width: 992px) {
  .auth-container {
    flex-direction: column;
  }
  
  .left-side {
    padding: 3rem 2rem;
    margin-top: 2rem;
  }
  
  .back-button {
    top: 1rem;
    left: 1rem;
  }
}

@media (max-width: 576px) {
  .back-button {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }
}
</style> 