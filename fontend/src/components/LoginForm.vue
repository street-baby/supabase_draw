<template>
  <div class="login-form">
    <div class="form-header">
      <h3>{{ title }}</h3>
    </div>
    
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
    
    <form @submit.prevent="onSubmit">
      <div class="form-group">
        <label for="email">邮箱</label>
        <div class="input-wrapper">
          <i class="icon">📧</i>
          <input
            type="email"
            id="email"
            v-model="form.email"
            required
            placeholder="请输入邮箱地址"
          />
        </div>
      </div>
      
      <div class="form-group">
        <label for="verification-code">验证码</label>
        <div class="verification-code-container">
          <div class="input-wrapper code-input">
            <i class="icon">🔑</i>
            <input
              type="text"
              id="verification-code"
              v-model="form.code"
              required
              placeholder="请输入验证码"
              maxlength="6"
            />
          </div>
          <button 
            type="button" 
            class="verification-code-btn" 
            @click="requestVerificationCode"
            :disabled="isCodeButtonDisabled"
          >
            {{ codeButtonText }}
          </button>
        </div>
      </div>
      
      <slot name="extra-fields"></slot>
      
      <button type="submit" class="btn-primary" :disabled="loading || !isValidForm">
        <span v-if="loading" class="loading-icon">⟳</span>
        <span v-else>{{ submitButtonText }}</span>
      </button>
    </form>
    
    <div class="form-footer">
      <slot name="form-footer"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

interface LoginFormProps {
  title: string
  submitButtonText: string
  loading?: boolean
}

const props = withDefaults(defineProps<LoginFormProps>(), {
  loading: false
})

const emit = defineEmits<{
  (e: 'submit', formData: { email: string, code: string }): void
}>()

const form = reactive({
  email: '',
  code: ''
})

const errorMessage = ref('')
const authStore = useAuthStore()
const countdown = ref(0)
const countdownInterval = ref<number | null>(null)

const isValidForm = computed(() => {
  return form.email.trim() !== '' && form.code.trim() !== '';
})

const isCodeButtonDisabled = computed(() => {
  return countdown.value > 0 || !form.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email);
})

const codeButtonText = computed(() => {
  return countdown.value > 0 ? `${countdown.value}秒后重试` : '获取验证码';
})

const startCountdown = (seconds: number = 60) => {
  countdown.value = seconds;
  if (countdownInterval.value) {
    clearInterval(countdownInterval.value);
  }
  
  countdownInterval.value = window.setInterval(() => {
    countdown.value--;
    if (countdown.value <= 0) {
      if (countdownInterval.value) {
        clearInterval(countdownInterval.value);
        countdownInterval.value = null;
      }
    }
  }, 1000);
}

const requestVerificationCode = async () => {
  if (isCodeButtonDisabled.value) return;
  
  try {
    const success = await authStore.sendVerificationCode(form.email);
    if (success) {
      startCountdown();
    } else {
      errorMessage.value = '验证码发送失败，请稍后再试';
    }
  } catch (error) {
    console.error('请求验证码出错', error);
    errorMessage.value = '验证码发送失败，请稍后再试';
  }
}

const onSubmit = () => {
  errorMessage.value = '';
  emit('submit', { email: form.email, code: form.code });
}
</script>

<style scoped>
.login-form {
  width: 100%;
}

.form-header {
  margin-bottom: 1.5rem;
  text-align: center;
}

.form-header h3 {
  font-size: 1.75rem;
  color: #e67e22;
  margin: 0;
  font-weight: 600;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #aaa;
  font-size: 0.95rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background-color: #232323;
  border: 1px solid #333;
  border-radius: 8px;
  transition: all 0.3s;
}

.input-wrapper:focus-within {
  border-color: #e67e22;
  box-shadow: 0 0 0 3px rgba(230, 126, 34, 0.15);
}

.icon {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 0.75rem;
  font-style: normal;
  color: #e67e22;
}

.form-group input {
  width: 100%;
  padding: 0.9rem 0.75rem 0.9rem 0;
  border: none;
  outline: none;
  font-size: 1rem;
  background-color: transparent;
  color: #f5f5f5;
}

.verification-code-container {
  display: flex;
  gap: 10px;
}

.code-input {
  flex: 1;
}

.verification-code-btn {
  width: 120px;
  padding: 0.9rem 0.5rem;
  background-color: rgba(230, 126, 34, 0.2);
  color: #e67e22;
  border: 1px solid #e67e22;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.verification-code-btn:hover:not(:disabled) {
  background-color: rgba(230, 126, 34, 0.3);
}

.verification-code-btn:disabled {
  background-color: rgba(230, 126, 34, 0.1);
  border-color: rgba(230, 126, 34, 0.3);
  color: rgba(230, 126, 34, 0.5);
  cursor: not-allowed;
}

.btn-primary {
  width: 100%;
  padding: 0.9rem;
  background-color: #e67e22;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background-color 0.3s;
  position: relative;
}

.btn-primary:hover:not(:disabled) {
  background-color: #f5c518;
}

.btn-primary:disabled {
  background-color: rgba(230, 126, 34, 0.6);
  cursor: not-allowed;
}

.loading-icon {
  display: inline-block;
  animation: spin 1s infinite linear;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.form-footer {
  margin-top: 1.5rem;
  text-align: center;
  color: #aaa;
}

.form-footer a {
  color: #e67e22;
  text-decoration: none;
  transition: color 0.3s;
}

.form-footer a:hover {
  color: #f5c518;
  text-decoration: underline;
}

.error-message {
  padding: 0.75rem;
  background-color: rgba(211, 47, 47, 0.2);
  color: #ff6b6b;
  border-radius: 8px;
  margin-bottom: 1.2rem;
  text-align: center;
  font-size: 0.9rem;
}
</style> 