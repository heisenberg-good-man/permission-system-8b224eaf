# 招聘平台 MVP

前后端分离的招聘平台，支持职位发布、简历投递和双方沟通。

## 技术栈

- **后端**: Python 3 + FastAPI + Uvicorn
- **前端**: Vue 3 + Vite + Vue Router + Axios

## 项目结构

```
permission-system-8b224eaf/
├── backend/                    # 后端服务
│   ├── app.py                 # FastAPI 主应用
│   └── requirements.txt       # Python 依赖
├── frontend/                   # 前端应用
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── api/index.js       # API 接口封装
│       ├── stores/user.js     # 用户状态管理
│       ├── router/index.js    # 路由配置
│       └── views/             # 页面组件
│           ├── Login.vue
│           ├── recruiter/     # 招聘方页面
│           └── candidate/     # 应聘方页面
└── README.md
```

## 快速启动

### 后端服务

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务（默认端口 8000）
python app.py

# 访问地址
# http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### 前端服务

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器（默认端口 3000）
npm run dev

# 访问地址
# http://localhost:3000
```

## API 接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/users/login` | POST | 用户登录 |
| `/api/users` | GET | 获取用户列表 |
| `/api/users/{id}` | GET | 获取用户详情 |
| `/api/jobs` | GET/POST | 获取职位列表/创建职位 |
| `/api/jobs/{id}` | GET/PUT/DELETE | 职位详情/更新/删除 |
| `/api/resumes` | GET/POST | 获取简历列表/投递简历 |
| `/api/resumes/{id}` | GET/PUT | 简历详情/更新状态 |
| `/api/messages` | GET/POST | 获取消息列表/发送消息 |
| `/api/interviews` | GET/POST | 获取面试列表/创建面试安排 |
| `/api/interviews/{id}` | GET/PUT | 面试详情/更新面试安排 |
| `/api/stats/{user_id}` | GET | 获取统计数据 |

## 模拟账号

| 角色 | 姓名 | 邮箱 |
|------|------|------|
| 招聘方 | 张三 | zhangsan@company.com |
| 招聘方 | 王五 | wangwu@company.com |
| 应聘方 | 李四 | lisi@example.com |
| 应聘方 | 赵六 | zhaoliu@example.com |

> 登录时所有账号密码统一填写任意字符即可

## 功能说明

### 招聘方
- 职位管理：查看、新增、编辑、删除职位
- 简历投递：查看职位收到的候选人投递列表
- 候选人筛选：按状态、职位、关键词筛选
- 状态管理：标记候选人状态（已投递→待沟通→已约聊→已拒绝）
- 面试安排：创建、编辑、取消、完成面试安排
- 面试列表：按状态、日期筛选面试安排
- 沟通区：与候选人发送和查看消息记录

### 应聘方
- 职位浏览：搜索、筛选职位列表
- 职位详情：查看完整职位信息
- 简历投递：填写并提交简历
- 投递记录：查看所有投递及状态变化
- 面试确认：查看面试安排并确认参加
- 沟通区：与招聘方发送和查看消息记录

### 统计数据
- 发布职位数
- 收到投递数
- 待沟通数量
- 已约聊数量
- 待确认面试数
- 今日面试数
- 已完成面试数

### 面试状态流转

```
待确认 → 已确认 → 已完成
    ↓           ↓
   已取消      已取消
```

## 简历状态流转

```
已投递 → 待沟通 → 已约聊
    ↓           ↓
   已拒绝      已拒绝
```