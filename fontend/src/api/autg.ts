// fontend/src/api/auth.ts
import axios from 'axios';

const API_URL = 'http://localhost:5300/api';

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 添加请求拦截器，自动添加token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const authApi = {
  // 发送邮箱验证码
  sendVerificationCode(email: string) {
    return apiClient.post('/auth/send-code', { email });
  },

  // 验证码登录
  login(email: string, code: string) {
    return apiClient.post('/auth/login', { email, code });
  },

  // 注册
  register(email: string, code: string, password: string) {
    return apiClient.post('/auth/register', { email, code, password });
  },

  // 获取当前用户信息
  getCurrentUser() {
    return apiClient.get('/auth/me');
  }
};

// fontend/src/api/image.ts
export const imageApi = {
  // 生成图像
  generateImage(prompt: string, style: string, ratio: string) {
    return apiClient.post('/image/generate', { prompt, style, ratio });
  },

  // 获取用户生成的图像列表
  getUserImages(page = 1, perPage = 10) {
    return apiClient.get(`/image/list?page=${page}&per_page=${perPage}`);
  }
};