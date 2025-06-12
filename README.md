# supabase_draw - AI文生图平台

这是一个基于Vue 3和Flask的AI文生图平台，实现了邮箱验证码登录和图片生成功能。

## 项目结构

```
supabase_draw/
├── fontend/                  # Vue前端
│   ├── src/
│   │   ├── api/              # API服务
│   │   │   ├── auth.ts       # 认证相关API
│   │   │   └── image.ts      # 图像生成相关API
│   │   ├── components/       # 组件
│   │   ├── stores/           # Pinia状态管理
│   │   └── views/            # 页面视图
│   └── ...
└── backend/                  # Flask后端
    ├── app.py                # 主应用
    ├── config.py             # 配置文件
    ├── models.py             # 数据库模型
    ├── routes/               # 路由
    │   ├── auth.py           # 认证相关路由
    │   └── image.py          # 图像生成相关路由
    └── utils/                # 工具函数
        └── email_util.py     # 邮件工具
```

## 前后端连接

前端和后端通过RESTful API进行通信，主要包括以下几个方面：

1. **认证流程**:
   - 用户注册/登录前需要先发送邮箱验证码
   - 验证码验证通过后，后端返回JWT令牌
   - 前端存储令牌并在后续请求中使用

2. **API交互**:
   - 前端使用axios发起HTTP请求
   - 请求拦截器自动添加认证头
   - Vite开发服务器配置了API代理，将/api请求转发到后端

3. **数据流**:
   - 前端表单 -> API服务 -> 后端路由 -> 数据库
   - 数据库 -> 后端路由 -> API响应 -> 前端展示

## 启动项目

### 前端

```bash
cd fontend
npm install
npm run dev
```

### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## 数据库设置

1. 创建MySQL数据库:

```sql
CREATE DATABASE douyin_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'douyin_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON douyin_db.* TO 'douyin_user'@'localhost';
FLUSH PRIVILEGES;
```

2. 初始化数据库表:

```bash
cd backend
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 功能特点

- 深色主题UI设计
- 邮箱验证码登录/注册
- JWT认证保护API
- 文生图功能
- 响应式设计，适配各种设备
