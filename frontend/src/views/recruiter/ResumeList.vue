<template>
  <div class="resume-list">
    <div class="list-header">
      <button class="btn btn-outline" @click="$router.back()">← 返回</button>
      <h2>{{ jobTitle }} - 简历投递</h2>
    </div>

    <div class="card">
      <table class="table">
        <thead>
          <tr>
            <th>候选人</th>
            <th>学历</th>
            <th>经验</th>
            <th>技能</th>
            <th>状态</th>
            <th>投递时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="resume in resumes" :key="resume.id">
            <td>{{ resume.candidate_name }}</td>
            <td>{{ resume.education }}</td>
            <td>{{ resume.experience }}</td>
            <td>{{ resume.skills }}</td>
            <td>
              <span :class="['status-tag', `status-${resume.status}`]">{{ getStatusText(resume.status) }}</span>
            </td>
            <td>{{ formatDate(resume.created_at) }}</td>
            <td>
              <button class="btn btn-outline" @click="$router.push(`/recruiter/resume/${resume.id}`)">详情</button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="resumes.length === 0" class="empty-state">
        <div class="empty-icon">📭</div>
        <p>暂无简历投递</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { jobApi, resumeApi } from '../../api'

const route = useRoute()
const resumes = ref([])
const jobTitle = ref('')

const getStatusText = (status) => {
  const map = { applied: '已投递', pending: '待沟通', interview: '已约聊', rejected: '已拒绝' }
  return map[status] || status
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

const loadData = async () => {
  try {
    const [jobRes, resumesRes] = await Promise.all([
      jobApi.getJob(route.params.id),
      resumeApi.getResumes({ job_id: route.params.id })
    ])
    jobTitle.value = jobRes.data.title
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
.resume-list {
  max-width: 1200px;
  margin: 0 auto;
}

.list-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.list-header h2 {
  margin: 0;
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