import axios from 'axios';

// 使用与auth相同的API实例配置
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

// 图像生成相关API
export default {
  // 生成图像
  generateImage(prompt: string, style: string = '自然风格', ratio: string = '1:1') {
    return api.post('/image/generate', { prompt, style, ratio });
  },

  // 获取用户生成的图像列表
  getImageList(page: number = 1, perPage: number = 10) {
    return api.get('/image/list', {
      params: { page, per_page: perPage }
    });
  }
}; 