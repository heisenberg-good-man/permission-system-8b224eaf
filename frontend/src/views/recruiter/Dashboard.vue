<template>
  <div class="dashboard">
    <header class="header">
      <div class="header-left">
        <h1>招聘工作台</h1>
        <span class="user-info">欢迎, {{ currentUser?.name }}</span>
      </div>
      <button class="btn btn-outline" @click="handleLogout">退出登录</button>
    </header>

    <nav class="sidebar">
      <div class="nav-item" :class="{ active: ['/recruiter', '/recruiter/jobs'].includes($route.path) }">
        <router-link to="/recruiter">职位管理</router-link>
      </div>
      <div class="nav-item" :class="{ active: $route.path === '/recruiter/applications' }">
        <router-link to="/recruiter/applications">简历投递</router-link>
      </div>
    </nav>

    <main class="main-content">
      <div v-if="showStats" class="stats-row">
        <div class="stat-card">
          <div class="stat-icon">📋</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.jobs_count }}</div>
            <div class="stat-label">发布职位</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📥</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.resumes_count }}</div>
            <div class="stat-label">收到投递</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">⏳</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.pending_count }}</div>
            <div class="stat-label">待沟通</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.interview_count }}</div>
            <div class="stat-label">已约聊</div>
          </div>
        </div>
      </div>
      <router-view @update-stats="loadStats" />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { statsApi } from '../../api'

defineExpose({ loadStats })

const router = useRouter()
const route = useRoute()
const { state, logout } = useUserStore()

const currentUser = computed(() => state.currentUser)
const stats = ref({
  jobs_count: 0,
  resumes_count: 0,
  pending_count: 0,
  interview_count: 0
})

const showStats = computed(() => {
  return ['/recruiter', '/recruiter/applications'].includes(route.path)
})

const handleLogout = () => {
  logout()
  router.push('/')
}

const loadStats = async () => {
  if (!currentUser.value) return
  try {
    const response = await statsApi.getStats(currentUser.value.id)
    stats.value = response.data
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.dashboard {
  display: flex;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-left h1 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.user-info {
  color: #999;
  font-size: 14px;
}

.sidebar {
  width: 200px;
  background: white;
  padding-top: 60px;
  min-height: 100vh;
  border-right: 1px solid #ebeef5;
}

.nav-item {
  padding: 12px 20px;
  cursor: pointer;
  border-left: 3px solid transparent;
}

.nav-item.active {
  background-color: #ecf5ff;
  border-left-color: #409eff;
}

.nav-item a {
  text-decoration: none;
  color: #666;
  font-size: 14px;
}

.nav-item.active a {
  color: #409eff;
}

.main-content {
  flex: 1;
  padding-top: 60px;
  padding: 60px 20px 20px 20px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 32px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #999;
}
</style>