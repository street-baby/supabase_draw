import axios from 'axios';

// 创建API实例
const API_URL = 'http://localhost:5300/api';
const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器，添加认证令牌
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 认证相关API
export default {
  // 发送邮箱验证码
  sendVerificationCode(email: string) {
    return api.post('/auth/send-code', { email });
  },

  // 用户注册
  register(email: string, code: string, password: string) {
    return api.post('/auth/register', { email, code, password });
  },

  // 邮箱验证码登录
  login(email: string, code: string) {
    return api.post('/auth/login', { email, code });
  },

  // 获取当前用户信息
  getUserInfo() {
    return api.get('/auth/me');
  },

  // 退出登录 (前端处理，清除token)
  logout() {
    localStorage.removeItem('token');
    return Promise.resolve();
  }
}; 