<template>
  <div class="resume-detail">
    <div class="detail-header">
      <button class="btn btn-outline" @click="$router.back()">← 返回</button>
      <h2>简历详情</h2>
    </div>

    <div class="card" v-if="resume">
      <div class="resume-info">
        <div class="info-row">
          <span class="label">候选人</span>
          <span class="value">{{ resume.candidate_name }}</span>
        </div>
        <div class="info-row">
          <span class="label">联系电话</span>
          <span class="value">{{ resume.phone }}</span>
        </div>
        <div class="info-row">
          <span class="label">邮箱</span>
          <span class="value">{{ resume.email }}</span>
        </div>
        <div class="info-row">
          <span class="label">学历</span>
          <span class="value">{{ resume.education }}</span>
        </div>
        <div class="info-row">
          <span class="label">工作经验</span>
          <span class="value">{{ resume.experience }}</span>
        </div>
        <div class="info-row">
          <span class="label">技能</span>
          <span class="value">{{ resume.skills }}</span>
        </div>
        <div class="info-row">
          <span class="label">投递职位</span>
          <span class="value">{{ jobTitle }}</span>
        </div>
        <div class="info-row">
          <span class="label">当前状态</span>
          <span :class="['status-tag', `status-${resume.status}`]">{{ getStatusText(resume.status) }}</span>
        </div>
        <div class="info-row">
          <span class="label">投递时间</span>
          <span class="value">{{ formatDate(resume.created_at) }}</span>
        </div>
      </div>

      <div class="resume-text">
        <h3>简历内容</h3>
        <p>{{ resume.resume_text }}</p>
      </div>

      <div class="action-buttons">
        <button 
          v-if="resume.status === 'applied'" 
          class="btn btn-warning" 
          @click="updateStatus('pending')"
        >
          标记为待沟通
        </button>
        <button 
          v-if="resume.status === 'applied' || resume.status === 'pending'" 
          class="btn btn-success" 
          @click="updateStatus('interview')"
        >
          标记为已约聊
        </button>
        <button 
          v-if="resume.status !== 'rejected'" 
          class="btn btn-danger" 
          @click="updateStatus('rejected')"
        >
          拒绝
        </button>
      </div>
    </div>

    <div class="card message-section">
      <h3>沟通记录</h3>
      <div class="message-list">
        <div 
          v-for="msg in messages" 
          :key="msg.id" 
          :class="['message-item', msg.sender_role === 'recruiter' ? 'recruiter-msg' : 'candidate-msg']"
        >
          <div class="msg-sender">{{ msg.sender_role === 'recruiter' ? '招聘方' : '候选人' }}</div>
          <div class="msg-content">{{ msg.content }}</div>
          <div class="msg-time">{{ formatDate(msg.created_at) }}</div>
        </div>
      </div>
      <div class="message-input">
        <input 
          v-model="newMessage" 
          type="text" 
          placeholder="输入消息..." 
          @keyup.enter="sendMessage"
        />
        <button class="btn btn-primary" @click="sendMessage">发送</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { resumeApi, jobApi, messageApi } from '../../api'

const emit = defineEmits(['update-stats'])

const route = useRoute()
const router = useRouter()
const { state } = useUserStore()

const resume = ref(null)
const jobTitle = ref('')
const messages = ref([])
const newMessage = ref('')

const getStatusText = (status) => {
  const map = { applied: '已投递', pending: '待沟通', interview: '已约聊', rejected: '已拒绝' }
  return map[status] || status
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

const updateStatus = async (status) => {
  if (!resume.value) return
  try {
    await resumeApi.updateResume(resume.value.id, { ...resume.value, status })
    resume.value.status = status
    emit('update-stats')
  } catch (error) {
    console.error('Update status failed:', error)
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || !resume.value) return
  try {
    const msg = {
      resume_id: resume.value.id,
      sender_id: state.currentUser?.id || 1,
      sender_role: 'recruiter',
      content: newMessage.value
    }
    await messageApi.createMessage(msg)
    newMessage.value = ''
    loadMessages()
  } catch (error) {
    console.error('Send message failed:', error)
  }
}

const loadMessages = async () => {
  if (!resume.value) return
  try {
    const response = await messageApi.getMessages(resume.value.id)
    messages.value = response.data
  } catch (error) {
    console.error('Load messages failed:', error)
  }
}

const loadData = async () => {
  try {
    const [resumeRes, jobRes] = await Promise.all([
      resumeApi.getResume(route.params.id),
      jobApi.getJob(route.params.job_id)
    ])
    resume.value = resumeRes.data
    jobTitle.value = jobRes.data.title
    loadMessages()
  } catch (error) {
    console.error('Failed to load data:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.resume-detail {
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

.resume-info {
  margin-bottom: 24px;
}

.info-row {
  display: flex;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-row:last-child {
  border-bottom: none;
}

.info-row .label {
  width: 100px;
  color: #999;
  font-weight: 500;
}

.info-row .value {
  flex: 1;
}

.resume-text {
  margin-bottom: 24px;
  padding: 16px;
  background-color: #fafafa;
  border-radius: 8px;
}

.resume-text h3 {
  margin: 0 0 12px 0;
  font-size: 16px;
}

.resume-text p {
  margin: 0;
  line-height: 1.8;
  color: #666;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.message-section {
  margin-top: 20px;
}

.message-list {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 16px;
  padding: 16px;
  background-color: #fafafa;
  border-radius: 8px;
}

.message-item {
  margin-bottom: 16px;
}

.message-item:last-child {
  margin-bottom: 0;
}

.msg-sender {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}

.msg-content {
  padding: 8px 12px;
  border-radius: 8px;
  max-width: 80%;
}

.recruiter-msg .msg-content {
  background-color: #409eff;
  color: white;
  margin-left: auto;
}

.candidate-msg .msg-content {
  background-color: white;
  border: 1px solid #e0e0e0;
}

.msg-time {
  font-size: 11px;
  color: #bbb;
  margin-top: 4px;
}

.message-input {
  display: flex;
  gap: 12px;
}

.message-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}
</style>