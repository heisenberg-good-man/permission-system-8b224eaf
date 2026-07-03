<template>
  <div class="job-list">
    <div class="list-header">
      <h2>浏览职位</h2>
      <div class="search-bar">
        <input v-model="searchKeyword" type="text" placeholder="搜索职位..." />
        <select v-model="locationFilter">
          <option value="">全部地点</option>
          <option value="北京">北京</option>
          <option value="上海">上海</option>
          <option value="杭州">杭州</option>
          <option value="深圳">深圳</option>
        </select>
      </div>
    </div>

    <div class="job-cards">
      <div 
        v-for="job in filteredJobs" 
        :key="job.id" 
        class="job-card"
        @click="$router.push(`/candidate/job/${job.id}`)"
      >
        <div class="job-header">
          <h3>{{ job.title }}</h3>
          <span class="salary">{{ job.salary }}</span>
        </div>
        <div class="job-meta">
          <span class="company">{{ job.company }}</span>
          <span class="location">{{ job.location }}</span>
          <span class="experience">{{ job.experience }}</span>
          <span class="education">{{ job.education }}</span>
        </div>
        <p class="job-desc">{{ job.description }}</p>
        <div class="job-footer">
          <span :class="['status-tag', `status-${job.status}`]">{{ getStatusText(job.status) }}</span>
          <button class="btn btn-primary">查看详情</button>
        </div>
      </div>
    </div>

    <div v-if="filteredJobs.length === 0" class="empty-state">
      <div class="empty-icon">🔍</div>
      <p>暂无匹配的职位</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { jobApi } from '../../api'

const jobs = ref([])
const searchKeyword = ref('')
const locationFilter = ref('')

const getStatusText = (status) => {
  const map = { active: '招聘中', inactive: '已关闭' }
  return map[status] || status
}

const filteredJobs = computed(() => {
  let result = jobs.value.filter(j => j.status === 'active')
  
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(j => 
      j.title.toLowerCase().includes(keyword) || 
      j.company.toLowerCase().includes(keyword) ||
      j.description.toLowerCase().includes(keyword)
    )
  }
  
  if (locationFilter.value) {
    result = result.filter(j => j.location === locationFilter.value)
  }
  
  return result
})

const loadJobs = async () => {
  try {
    const response = await jobApi.getJobs()
    jobs.value = response.data
  } catch (error) {
    console.error('Failed to load jobs:', error)
  }
}

onMounted(() => {
  loadJobs()
})
</script>

<style scoped>
.job-list {
  max-width: 1200px;
  margin: 0 auto;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.list-header h2 {
  margin: 0;
}

.search-bar {
  display: flex;
  gap: 12px;
}

.search-bar input,
.search-bar select {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.search-bar input {
  width: 200px;
}

.job-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.job-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.job-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.job-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.salary {
  font-size: 18px;
  font-weight: bold;
  color: #f56c6c;
}

.job-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  color: #666;
  font-size: 14px;
}

.job-desc {
  margin: 0 0 16px 0;
  color: #999;
  font-size: 14px;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.job-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.empty-state {
  text-align: center;
  padding: 60px;
  color: #999;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}
</style>