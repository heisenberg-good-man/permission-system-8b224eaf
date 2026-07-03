<template>
  <div class="application-list">
    <div class="list-header">
      <h2>简历投递</h2>
      <select v-model="statusFilter" class="filter-select">
        <option value="">全部状态</option>
        <option value="applied">已投递</option>
        <option value="pending">待沟通</option>
        <option value="interview">已约聊</option>
        <option value="rejected">已拒绝</option>
      </select>
    </div>

    <div class="card">
      <table class="table">
        <thead>
          <tr>
            <th>职位名称</th>
            <th>候选人</th>
            <th>状态</th>
            <th>投递时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredApplications" :key="item.resume.id">
            <td>{{ item.job.title }}</td>
            <td>{{ item.resume.candidate_name }}</td>
            <td>
              <span :class="['status-tag', `status-${item.resume.status}`]">{{ getStatusText(item.resume.status) }}</span>
            </td>
            <td>{{ formatDate(item.resume.created_at) }}</td>
            <td>
              <button class="btn btn-outline" @click="$router.push(`/recruiter/resume/${item.resume.id}`)">查看</button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="filteredApplications.length === 0" class="empty-state">
        <div class="empty-icon">📭</div>
        <p>暂无简历投递</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../../stores/user'
import { jobApi, resumeApi } from '../../api'

const emit = defineEmits(['update-stats'])

const { state } = useUserStore()
const jobs = ref([])
const resumes = ref([])
const statusFilter = ref('')

const getStatusText = (status) => {
  const map = { applied: '已投递', pending: '待沟通', interview: '已约聊', rejected: '已拒绝' }
  return map[status] || status
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

const filteredApplications = computed(() => {
  const myJobs = jobs.value.filter(j => j.recruiter_id === state.currentUser?.id)
  const jobIds = myJobs.map(j => j.id)
  
  let result = resumes.value
    .filter(r => jobIds.includes(r.job_id))
    .map(r => ({
      resume: r,
      job: myJobs.find(j => j.id === r.job_id)
    }))
  
  if (statusFilter.value) {
    result = result.filter(item => item.resume.status === statusFilter.value)
  }
  
  return result
})

const loadData = async () => {
  try {
    const [jobsRes, resumesRes] = await Promise.all([
      jobApi.getJobs(),
      resumeApi.getResumes()
    ])
    jobs.value = jobsRes.data
    resumes.value = resumesRes.data
  } catch (error) {
    console.error('Failed to load data:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.application-list {
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

.filter-select {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}
</style>