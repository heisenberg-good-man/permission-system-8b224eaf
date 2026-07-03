<template>
  <div class="dashboard">
    <header class="header">
      <div class="header-left">
        <h1>求职中心</h1>
        <span class="user-info">欢迎, {{ currentUser?.name }}</span>
      </div>
      <button class="btn btn-outline" @click="handleLogout">退出登录</button>
    </header>

    <nav class="sidebar">
      <div class="nav-item" :class="{ active: $route.path === '/candidate' }">
        <router-link to="/candidate">浏览职位</router-link>
      </div>
      <div class="nav-item" :class="{ active: $route.path === '/candidate/applications' }">
        <router-link to="/candidate/applications">我的投递</router-link>
      </div>
    </nav>

    <main class="main-content">
      <div v-if="showStats && stats" class="stats-row">
        <div class="stat-card">
          <div class="stat-icon">📋</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.jobs_count }}</div>
            <div class="stat-label">职位总数</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📤</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.resumes_count }}</div>
            <div class="stat-label">已投递</div>
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
        <div class="stat-card">
          <div class="stat-icon">📤</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.sent_offer_count }}</div>
            <div class="stat-label">待回应Offer</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.accepted_offer_count }}</div>
            <div class="stat-label">已接受Offer</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">❌</div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.rejected_offer_count }}</div>
            <div class="stat-label">已拒绝Offer</div>
          </div>
        </div>
      </div>
      <router-view @update-stats="loadStats" />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { statsApi } from '../../api'

const router = useRouter()
const { state, logout } = useUserStore()

const currentUser = computed(() => state.currentUser)
const stats = ref(null)
const showStats = computed(() => {
  return ['/candidate', '/candidate/applications'].includes(router.currentRoute.value.path)
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

defineExpose({ loadStats })
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