<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

const prompt = ref('')
const loading = ref(false)
const generatedImage = ref('')

const styles = ['自然风格', '写实', '动漫', '水彩', '油画', '素描', '3D']
const selectedStyle = ref('自然风格')

const ratios = ['1:1', '4:3', '16:9', '9:16']
const selectedRatio = ref('1:1')

const exampleImages = [
  {
    url: 'https://picsum.photos/seed/1/300/300',
    prompt: '宁静的湖面上，一艘小船漂浮着，周围是秋季的红叶'
  },
  {
    url: 'https://picsum.photos/seed/2/300/300',
    prompt: '未来城市的夜景，霓虹灯闪烁，飞行汽车穿梭其间'
  },
  {
    url: 'https://picsum.photos/seed/3/300/300',
    prompt: '一只蓝眼睛的白猫坐在窗台上，窗外是下着雪的冬天'
  },
  {
    url: 'https://picsum.photos/seed/4/300/300',
    prompt: '科幻风格的太空站，宇航员在太空行走'
  },
  {
    url: 'https://picsum.photos/seed/5/300/300',
    prompt: '森林中的童话小屋，门口点着温暖的灯光'
  },
  {
    url: 'https://picsum.photos/seed/6/300/300',
    prompt: '水下世界，色彩斑斓的珊瑚和热带鱼'
  },
  {
    url: 'https://picsum.photos/seed/7/300/300',
    prompt: '繁星点点的夜空下，一个人坐在山顶眺望'
  },
  {
    url: 'https://picsum.photos/seed/8/300/300',
    prompt: '中国古代宫廷场景，红墙金瓦，亭台楼阁'
  }
]

const generateImage = async () => {
  if (!prompt.value.trim()) return
  
  loading.value = true
  
  try {
    // 这里模拟API调用，实际项目中应该调用真正的文生图API
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 模拟返回图片URL（使用随机图片代替）
    generatedImage.value = `https://picsum.photos/seed/${Math.random()}/800/800`
    
  } catch (error) {
    console.error('生成图片失败', error)
  } finally {
    loading.value = false
  }
}

const useExamplePrompt = (examplePrompt: string) => {
  prompt.value = examplePrompt
  // 自动滚动到输入区
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const downloadImage = () => {
  const link = document.createElement('a')
  link.href = generatedImage.value
  link.download = `ai-image-${Date.now()}.jpg`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const saveImage = () => {
  // 保存图片到用户作品集，实际项目中应该调用API
  console.log('保存图片', generatedImage.value)
  alert('图片已保存到您的作品集')
}
</script>

<template>
  <div class="home-container">
    <header class="site-header">
      <div class="logo">
        <h1>AI文生图平台</h1>
      </div>
      <div class="header-right">
        <button v-if="!authStore.isAuthenticated" @click="$router.push('/login')" class="login-btn">登录</button>
        <button v-else @click="$router.push('/dashboard')" class="dashboard-btn">我的控制台</button>
      </div>
    </header>
    
    <main class="main-content">
      <section class="hero-section">
        <h1 class="main-title">在几秒钟内创建令人惊叹的AI<br>生成图像</h1>
        <p class="subtitle">通过文字描述，轻松转化为高质量图像</p>
        
        <div class="prompt-container">
          <div class="input-wrapper">
            <textarea 
              v-model="prompt" 
              class="prompt-input" 
              placeholder="请输入文字描述，例如：一只金色的猫在宇宙中漂浮" 
              @keyup.enter="generateImage"
            ></textarea>
            <button class="generate-btn" @click="generateImage" :disabled="loading">
              <span v-if="loading" class="loading-icon">⟳</span>
              <span v-else>生成图像</span>
            </button>
          </div>
          
          <div class="options-container">
            <div class="options-row">
              <div class="option-label">风格：</div>
              <div class="options-buttons">
                <button 
                  v-for="(style, index) in styles" 
                  :key="index" 
                  :class="['style-btn', selectedStyle === style ? 'active' : '']"
                  @click="selectedStyle = style"
                >
                  {{ style }}
                </button>
              </div>
            </div>
            
            <div class="options-row">
              <div class="option-label">比例：</div>
              <div class="options-buttons">
                <button 
                  v-for="(ratio, index) in ratios" 
                  :key="index" 
                  :class="['ratio-btn', selectedRatio === ratio ? 'active' : '']"
                  @click="selectedRatio = ratio"
                >
                  {{ ratio }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <section class="result-section" v-if="generatedImage">
        <h2>生成结果</h2>
        <div class="image-result">
          <img :src="generatedImage" alt="AI生成的图像" />
          <div class="image-actions">
            <button class="action-btn download-btn" @click="downloadImage">
              <span>下载</span>
            </button>
            <button v-if="!authStore.isAuthenticated" @click="$router.push('/login')" class="action-btn save-btn">
              <span>登录并保存</span>
            </button>
            <button v-else class="action-btn save-btn" @click="saveImage">
              <span>保存到我的作品</span>
            </button>
          </div>
        </div>
      </section>
      
      <section class="gallery-section">
        <h2 class="section-title">获得灵感</h2>
        <p class="section-subtitle">从精选示例中寻找创作灵感</p>
        <div class="gallery-grid">
          <div 
            v-for="(example, index) in exampleImages" 
            :key="index" 
            class="gallery-item"
            @click="useExamplePrompt(example.prompt)"
          >
            <img :src="example.url" :alt="example.prompt" />
            <div class="overlay">
              <p>{{ example.prompt }}</p>
            </div>
          </div>
        </div>
      </section>
      
      <section class="features-section">
        <h2 class="section-title">主要功能</h2>
        <div class="features-grid">
          <div class="feature">
            <div class="feature-icon">🎨</div>
            <h3>高质量生成</h3>
            <p>利用先进的AI模型，生成细节丰富的图像</p>
          </div>
          <div class="feature">
            <div class="feature-icon">⚡</div>
            <h3>快速响应</h3>
            <p>秒级出图，让您的创意即刻呈现</p>
          </div>
          <div class="feature">
            <div class="feature-icon">🔄</div>
            <h3>多样风格</h3>
            <p>支持多种艺术风格，满足不同创作需求</p>
          </div>
          <div class="feature">
            <div class="feature-icon">💾</div>
            <h3>作品管理</h3>
            <p>保存您喜欢的作品，随时查看和使用</p>
          </div>
        </div>
      </section>
    </main>
    
    <footer class="site-footer">
      <p>&copy; 2024 AI文生图平台 • 保留所有权利</p>
    </footer>
  </div>
</template>

<style scoped>
.home-container {
  width: 100%;
  min-height: 100vh;
  background-color: #121212; /* 更深的黑色背景 */
  color: #f5f5f5;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.site-header {
  width: 100%;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background-color: rgba(18, 18, 18, 0.95);
  z-index: 10;
  backdrop-filter: blur(5px);
}

.logo h1 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
  background: linear-gradient(90deg, #f5c518, #e67e22);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-right button {
  background-color: #e67e22;
  color: #121212;
  padding: 0.5rem 1.2rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.header-right button:hover {
  background-color: #f5c518;
}

.main-content {
  flex: 1;
  max-width: 1000px;
  width: 100%;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero-section {
  text-align: center;
  padding: 3rem 0 2rem;
  width: 100%;
  max-width: 800px;
}

.main-title {
  font-size: 2.5rem;
  line-height: 1.2;
  margin-bottom: 1rem;
  background: linear-gradient(90deg, #f5c518, #e67e22);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}

.subtitle {
  font-size: 1.1rem;
  margin-bottom: 2.5rem;
  color: #aaa;
}

.section-title {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  color: #e67e22;
}

.section-subtitle {
  color: #aaa;
  margin-bottom: 2rem;
}

.prompt-container {
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
  background-color: #1a1a1a;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
}

.prompt-input {
  width: 100%;
  padding: 1rem;
  min-height: 80px;
  border-radius: 6px;
  border: 1px solid #333;
  background-color: #232323;
  color: #f5f5f5;
  font-size: 1rem;
  resize: vertical;
}

.prompt-input:focus {
  outline: none;
  border-color: #e67e22;
  box-shadow: 0 0 0 1px rgba(230, 126, 34, 0.2);
}

.generate-btn {
  width: 100%;
  padding: 0.9rem;
  border-radius: 6px;
  background: #e67e22;
  color: white;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}

.generate-btn:hover:not(:disabled) {
  background: #f5c518;
  transform: translateY(-2px);
}

.generate-btn:disabled {
  opacity: 0.7;
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

.options-container {
  margin-top: 1.5rem;
  width: 100%;
}

.options-row {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.option-label {
  font-size: 0.9rem;
  color: #aaa;
  width: 60px;
  text-align: right;
  margin-right: 0.8rem;
}

.options-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.style-btn, .ratio-btn {
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  border: 1px solid #333;
  background-color: #232323;
  color: #aaa;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.style-btn:hover, .ratio-btn:hover {
  border-color: #e67e22;
  color: #e67e22;
}

.style-btn.active, .ratio-btn.active {
  background-color: #e67e22;
  color: #fff;
  border-color: #e67e22;
}

.result-section {
  margin-top: 3rem;
  text-align: center;
  width: 100%;
}

.result-section h2 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #e67e22;
}

.image-result {
  max-width: 600px;
  margin: 0 auto;
  width: 100%;
}

.image-result img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
}

.image-actions {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.7rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.download-btn {
  background-color: #3498db;
  color: white;
}

.download-btn:hover {
  background-color: #2980b9;
}

.save-btn {
  background-color: #2ecc71;
  color: white;
}

.save-btn:hover {
  background-color: #27ae60;
}

.gallery-section {
  margin-top: 5rem;
  text-align: center;
  width: 100%;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 3rem;
  width: 100%;
}

.gallery-item {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  cursor: pointer;
  aspect-ratio: 1;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.gallery-item:hover img {
  transform: scale(1.05);
}

.gallery-item .overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.8);
  padding: 0.8rem;
  transform: translateY(100%);
  transition: transform 0.3s;
}

.gallery-item:hover .overlay {
  transform: translateY(0);
}

.gallery-item .overlay p {
  color: #fff;
  margin: 0;
  font-size: 0.85rem;
  line-height: 1.4;
}

.features-section {
  margin-top: 5rem;
  text-align: center;
  width: 100%;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.5rem;
  width: 100%;
  margin-top: 2rem;
}

.feature {
  padding: 1.5rem;
  background-color: #1a1a1a;
  border-radius: 8px;
  transition: transform 0.3s;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.feature:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
  display: inline-block;
  width: 50px;
  height: 50px;
  line-height: 50px;
  border-radius: 50%;
  background: #232323;
}

.feature h3 {
  font-size: 1.2rem;
  margin-bottom: 0.8rem;
  color: #e67e22;
}

.feature p {
  color: #aaa;
  font-size: 0.95rem;
  line-height: 1.5;
}

.site-footer {
  width: 100%;
  text-align: center;
  padding: 2rem;
  margin-top: 4rem;
  border-top: 1px solid #232323;
}

.site-footer p {
  color: #666;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .site-header {
    padding: 0.8rem 1rem;
  }
  
  .main-title {
    font-size: 1.8rem;
  }
  
  .subtitle {
    font-size: 1rem;
    padding: 0 1rem;
  }
  
  .prompt-container {
    padding: 1rem;
  }
  
  .options-row {
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 1.2rem;
  }
  
  .option-label {
    width: auto;
    text-align: left;
    margin-bottom: 0.5rem;
    margin-right: 0;
  }
  
  .options-buttons {
    width: 100%;
  }
  
  .image-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .action-btn {
    width: 100%;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
