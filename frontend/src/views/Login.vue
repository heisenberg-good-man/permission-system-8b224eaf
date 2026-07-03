<template>
  <div class="login-container">
    <div class="login-card">
      <h1>招聘平台</h1>
      <p class="subtitle">选择您的身份登录</p>
      
      <div class="role-selector">
        <div 
          class="role-card" 
          :class="{ active: selectedRole === 'recruiter' }"
          @click="selectedRole = 'recruiter'"
        >
          <div class="role-icon">💼</div>
          <h3>招聘方</h3>
          <p>发布职位、查看简历、与候选人沟通</p>
        </div>
        
        <div 
          class="role-card" 
          :class="{ active: selectedRole === 'candidate' }"
          @click="selectedRole = 'candidate'"
        >
          <div class="role-icon">👤</div>
          <h3>应聘方</h3>
          <p>浏览职位、投递简历、与招聘方沟通</p>
        </div>
      </div>

      <div class="user-list">
        <h4>{{ selectedRole === 'recruiter' ? '招聘方账号' : '应聘方账号' }}</h4>
        <div class="user-cards">
          <div 
            v-for="user in filteredUsers" 
            :key="user.id"
            class="user-card"
            :class="{ active: selectedUser?.id === user.id }"
            @click="selectedUser = user"
          >
            <div class="user-avatar">{{ user.name.charAt(0) }}</div>
            <div class="user-info">
              <div class="user-name">{{ user.name }}</div>
              <div class="user-email">{{ user.email }}</div>
            </div>
          </div>
        </div>
      </div>

      <button 
        class="btn btn-primary login-btn" 
        :disabled="!selectedUser"
        @click="handleLogin"
      >
        登录
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { userApi } from '../api'
import { useUserStore } from '../stores/user'

const router = useRouter()
const { login } = useUserStore()

const selectedRole = ref('recruiter')
const selectedUser = ref(null)
const users = ref([])

const filteredUsers = computed(() => {
  return users.value.filter(u => u.role === selectedRole.value)
})

const loadUsers = async () => {
  try {
    const response = await userApi.getUsers()
    users.value = response.data
    if (users.value.length > 0) {
      selectedUser.value = filteredUsers.value[0]
    }
  } catch (error) {
    console.error('Failed to load users:', error)
  }
}

const handleLogin = async () => {
  if (!selectedUser.value) return
  
  try {
    const response = await userApi.login(selectedUser.value.email, 'password')
    login(response.data.user, response.data.token)
    
    if (selectedUser.value.role === 'recruiter') {
      router.push('/recruiter')
    } else {
      router.push('/candidate')
    }
  } catch (error) {
    console.error('Login failed:', error)
    alert('登录失败，请重试')
  }
}

loadUsers()
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-card h1 {
  text-align: center;
  color: #333;
  margin-bottom: 8px;
  font-size: 28px;
}

.subtitle {
  text-align: center;
  color: #999;
  margin-bottom: 30px;
}

.role-selector {
  display: flex;
  gap: 16px;
  margin-bottom: 30px;
}

.role-card {
  flex: 1;
  padding: 20px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;
}

.role-card:hover {
  border-color: #409eff;
}

.role-card.active {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.role-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.role-card h3 {
  margin: 0 0 8px 0;
  color: #333;
}

.role-card p {
  margin: 0;
  color: #666;
  font-size: 13px;
}

.user-list h4 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 16px;
}

.user-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.user-card {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.user-card:hover {
  border-color: #409eff;
}

.user-card.active {
  border-color: #409eff;
  background-color: #ecf5ff;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  margin-right: 12px;
}

.user-info {
  flex: 1;
}

.user-name {
  font-weight: 500;
  color: #333;
}

.user-email {
  font-size: 12px;
  color: #999;
}

.login-btn {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  border-radius: 8px;
}

.login-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>