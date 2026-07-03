<template>
  <div class="application-list">
    <div class="list-header">
      <h2>简历投递</h2>
    </div>

    <div class="filter-bar">
      <input 
        v-model="keywordFilter" 
        type="text" 
        placeholder="搜索候选人姓名、技能..." 
        class="search-input"
      />
      <select v-model="jobFilter" class="filter-select">
        <option value="">全部职位</option>
        <option v-for="job in myJobs" :key="job.id" :value="job.id">{{ job.title }}</option>
      </select>
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
            <th>技能</th>
            <th>学历</th>
            <th>状态</th>
            <th>投递时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredApplications" :key="item.resume.id">
            <td>{{ item.job?.title || '未知职位' }}</td>
            <td>{{ item.resume.candidate_name }}</td>
            <td>{{ item.resume.skills }}</td>
            <td>{{ item.resume.education }}</td>
            <td>
              <span :class="['status-tag', `status-${item.resume.status}`]">{{ getStatusText(item.resume.status) }}</span>
            </td>
            <td>{{ formatDate(item.resume.created_at) }}</td>
            <td>
              <button class="btn btn-outline" @click="viewResume(item.resume.id)">查看</button>
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
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { jobApi, resumeApi } from '../../api'

const emit = defineEmits(['update-stats'])

const router = useRouter()
const { state } = useUserStore()
const jobs = ref([])
const resumes = ref([])
const keywordFilter = ref('')
const jobFilter = ref('')
const statusFilter = ref('')

const myJobs = computed(() => {
  return jobs.value.filter(j => j.recruiter_id === state.currentUser?.id)
})

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
  const jobIds = myJobs.value.map(j => j.id)
  
  let result = resumes.value
    .filter(r => jobIds.includes(r.job_id))
    .map(r => ({
      resume: r,
      job: myJobs.value.find(j => j.id === r.job_id)
    }))
  
  if (keywordFilter.value) {
    const keyword = keywordFilter.value.toLowerCase()
    result = result.filter(item => 
      item.resume.candidate_name.toLowerCase().includes(keyword) ||
      item.resume.skills.toLowerCase().includes(keyword) ||
      item.resume.education.toLowerCase().includes(keyword) ||
      item.resume.experience.toLowerCase().includes(keyword)
    )
  }
  
  if (jobFilter.value) {
    result = result.filter(item => String(item.resume.job_id) === jobFilter.value)
  }
  
  if (statusFilter.value) {
    result = result.filter(item => item.resume.status === statusFilter.value)
  }
  
  return result
})

const viewResume = (resumeId) => {
  router.push(`/recruiter/resume/${resumeId}`)
}

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
  margin-bottom: 16px;
}

.list-header h2 {
  margin: 0;
}

.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  max-width: 300px;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  min-width: 120px;
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