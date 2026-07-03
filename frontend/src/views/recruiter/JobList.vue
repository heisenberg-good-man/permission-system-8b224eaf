<template>
  <div class="job-list">
    <div class="list-header">
      <h2>职位管理</h2>
      <button class="btn btn-primary" @click="$router.push('/recruiter/job/create')">
        + 发布职位
      </button>
    </div>

    <div class="card">
      <table class="table">
        <thead>
          <tr>
            <th>职位名称</th>
            <th>公司</th>
            <th>地点</th>
            <th>薪资</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobs" :key="job.id">
            <td>
              <a href="#" @click.prevent="viewResumes(job.id)">{{ job.title }}</a>
            </td>
            <td>{{ job.company }}</td>
            <td>{{ job.location }}</td>
            <td>{{ job.salary }}</td>
            <td>
              <span :class="['status-tag', `status-${job.status}`]">{{ getStatusText(job.status) }}</span>
            </td>
            <td>
              <button class="btn btn-outline" @click="$router.push(`/recruiter/job/${job.id}/edit`)">编辑</button>
              <button class="btn btn-danger" @click="handleDelete(job.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="jobs.length === 0" class="empty-state">
        <div class="empty-icon">📭</div>
        <p>暂无职位，点击上方按钮发布新职位</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { jobApi } from '../../api'

const emit = defineEmits(['update-stats'])

const router = useRouter()
const { state } = useUserStore()
const jobs = ref([])

const getStatusText = (status) => {
  const map = { active: '招聘中', inactive: '已关闭' }
  return map[status] || status
}

const loadJobs = async () => {
  try {
    const response = await jobApi.getJobs({ recruiter_id: state.currentUser?.id })
    jobs.value = response.data
  } catch (error) {
    console.error('Failed to load jobs:', error)
  }
}

const handleDelete = async (id) => {
  if (!confirm('确定要删除这个职位吗？')) return
  try {
    await jobApi.deleteJob(id)
    loadJobs()
    emit('update-stats')
  } catch (error) {
    console.error('Delete failed:', error)
  }
}

const viewResumes = (jobId) => {
  router.push(`/recruiter/job/${jobId}/resumes`)
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