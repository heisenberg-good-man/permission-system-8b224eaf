<template>
  <div class="job-detail">
    <div class="detail-header">
      <button class="btn btn-outline" @click="$router.back()">← 返回</button>
      <h2>职位详情</h2>
    </div>

    <div class="card" v-if="job">
      <div class="job-title-section">
        <h1>{{ job.title }}</h1>
        <div class="job-tags">
          <span class="tag salary">{{ job.salary }}</span>
          <span class="tag">{{ job.location }}</span>
          <span class="tag">{{ job.experience }}</span>
          <span class="tag">{{ job.education }}</span>
        </div>
        <span :class="['status-tag', `status-${job.status}`]">{{ getStatusText(job.status) }}</span>
      </div>

      <div class="job-info">
        <div class="info-section">
          <h3>公司信息</h3>
          <p>{{ job.company }}</p>
        </div>

        <div class="info-section">
          <h3>职位描述</h3>
          <p>{{ job.description }}</p>
        </div>
      </div>

      <div class="apply-section">
        <button 
          v-if="!hasApplied" 
          class="btn btn-primary apply-btn" 
          @click="showApplyForm = true"
        >
          投递简历
        </button>
        <button 
          v-else 
          class="btn btn-outline apply-btn" 
          @click="$router.push('/candidate/applications')"
        >
          已投递，查看状态
        </button>
      </div>
    </div>

    <div v-if="showApplyForm" class="modal-overlay" @click.self="showApplyForm = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>投递简历</h3>
          <button class="modal-close" @click="showApplyForm = false">×</button>
        </div>
        
        <form @submit.prevent="handleApply">
          <div class="form-group">
            <label>姓名 *</label>
            <input v-model="applyForm.candidate_name" type="text" placeholder="请输入姓名" required />
          </div>
          
          <div class="form-group">
            <label>联系电话 *</label>
            <input v-model="applyForm.phone" type="tel" placeholder="请输入联系电话" required />
          </div>
          
          <div class="form-group">
            <label>邮箱 *</label>
            <input v-model="applyForm.email" type="email" placeholder="请输入邮箱" required />
          </div>
          
          <div class="row">
            <div class="form-group col">
              <label>学历 *</label>
              <select v-model="applyForm.education" required>
                <option value="">请选择</option>
                <option value="高中">高中</option>
                <option value="大专">大专</option>
                <option value="本科">本科</option>
                <option value="硕士">硕士</option>
                <option value="博士">博士</option>
              </select>
            </div>
            <div class="form-group col">
              <label>工作经验 *</label>
              <input v-model="applyForm.experience" type="text" placeholder="例如：3年" required />
            </div>
          </div>
          
          <div class="form-group">
            <label>技能特长 *</label>
            <input v-model="applyForm.skills" type="text" placeholder="请输入技能，用逗号分隔" required />
          </div>
          
          <div class="form-group">
            <label>简历内容 *</label>
            <textarea v-model="applyForm.resume_text" placeholder="请输入简历内容或自我介绍" required></textarea>
          </div>
          
          <div class="form-actions">
            <button type="button" class="btn btn-outline" @click="showApplyForm = false">取消</button>
            <button type="submit" class="btn btn-primary">确认投递</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { jobApi, resumeApi } from '../../api'

const emit = defineEmits(['update-stats'])

const route = useRoute()
const router = useRouter()
const { state } = useUserStore()

const job = ref(null)
const resumes = ref([])
const showApplyForm = ref(false)

const applyForm = ref({
  candidate_name: state.currentUser?.name || '',
  phone: '',
  email: state.currentUser?.email || '',
  education: '',
  experience: '',
  skills: '',
  resume_text: ''
})

const getStatusText = (status) => {
  const map = { active: '招聘中', inactive: '已关闭' }
  return map[status] || status
}

const hasApplied = ref(false)

const handleApply = async () => {
  try {
    const data = {
      ...applyForm.value,
      job_id: route.params.id,
      candidate_id: state.currentUser?.id || 2,
      status: 'applied'
    }
    await resumeApi.createResume(data)
    showApplyForm.value = false
    hasApplied.value = true
    emit('update-stats')
  } catch (error) {
    console.error('Apply failed:', error)
    alert('投递失败，请重试')
  }
}

const loadData = async () => {
  try {
    const [jobRes, resumesRes] = await Promise.all([
      jobApi.getJob(route.params.id),
      resumeApi.getResumes({ candidate_id: state.currentUser?.id })
    ])
    job.value = jobRes.data
    resumes.value = resumesRes.data
    hasApplied.value = resumes.value.some(r => r.job_id == route.params.id)
  } catch (error) {
    console.error('Failed to load data:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.job-detail {
  max-width: 800px;
  margin: 0 auto;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.detail-header h2 {
  margin: 0;
}

.job-title-section {
  margin-bottom: 24px;
}

.job-title-section h1 {
  margin: 0 0 12px 0;
  font-size: 28px;
}

.job-tags {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.tag {
  padding: 4px 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-size: 14px;
}

.tag.salary {
  background-color: #fef0f0;
  color: #f56c6c;
  font-weight: bold;
}

.job-info {
  margin-bottom: 24px;
}

.info-section {
  margin-bottom: 20px;
}

.info-section:last-child {
  margin-bottom: 0;
}

.info-section h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #333;
}

.info-section p {
  margin: 0;
  color: #666;
  line-height: 1.8;
}

.apply-section {
  text-align: center;
}

.apply-btn {
  padding: 12px 40px;
  font-size: 16px;
}

.row {
  display: flex;
  gap: 16px;
}

.row .col {
  flex: 1;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}
</style>