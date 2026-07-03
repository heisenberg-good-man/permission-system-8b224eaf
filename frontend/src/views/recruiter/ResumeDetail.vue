<template>
  <div class="resume-detail">
    <div class="detail-header">
      <button class="btn btn-outline" @click="$router.back()">← 返回</button>
      <h2>简历详情</h2>
    </div>

    <div class="card" v-if="resume">
      <div class="resume-header">
        <div class="candidate-name">{{ resume.candidate_name }}</div>
        <span :class="['status-tag', `status-${resume.status}`]">{{ getStatusText(resume.status) }}</span>
      </div>

      <div class="resume-summary">
        <div class="summary-item">
          <span class="summary-label">学历</span>
          <span class="summary-value">{{ resume.education }}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">经验</span>
          <span class="summary-value">{{ resume.experience }}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">技能</span>
          <span class="summary-value">{{ resume.skills }}</span>
        </div>
      </div>

      <div class="resume-section">
        <h3>基本信息</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">联系电话</span>
            <span class="value">{{ resume.phone }}</span>
          </div>
          <div class="info-item">
            <span class="label">邮箱</span>
            <span class="value">{{ resume.email }}</span>
          </div>
          <div class="info-item">
            <span class="label">投递职位</span>
            <span class="value">{{ jobTitle }}</span>
          </div>
          <div class="info-item">
            <span class="label">投递时间</span>
            <span class="value">{{ formatDate(resume.created_at) }}</span>
          </div>
        </div>
      </div>

      <div class="resume-section">
        <h3>简历内容</h3>
        <div class="resume-text">
          {{ resume.resume_text }}
        </div>
      </div>

      <div class="resume-section">
        <h3>处理状态</h3>
        <div class="status-flow">
          <div :class="['flow-item', { active: resume.status === 'applied', done: ['pending', 'interview', 'rejected'].includes(resume.status) }]">
            <div class="flow-circle">1</div>
            <span>已投递</span>
          </div>
          <div class="flow-arrow" v-if="['pending', 'interview', 'rejected'].includes(resume.status)">→</div>
          <div :class="['flow-item', { active: resume.status === 'pending', done: ['interview', 'rejected'].includes(resume.status) }]">
            <div class="flow-circle">2</div>
            <span>待沟通</span>
          </div>
          <div class="flow-arrow" v-if="['interview', 'rejected'].includes(resume.status)">→</div>
          <div :class="['flow-item', { active: resume.status === 'interview', done: resume.status === 'rejected' }]">
            <div class="flow-circle">3</div>
            <span>已约聊</span>
          </div>
          <div class="flow-arrow" v-if="resume.status === 'rejected'">→</div>
          <div :class="['flow-item', { active: resume.status === 'rejected' }]">
            <div class="flow-circle">✕</div>
            <span>已拒绝</span>
          </div>
        </div>
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
        <button 
          v-if="resume.status === 'pending' || resume.status === 'interview'" 
          class="btn btn-primary" 
          @click="showInterviewModal = true"
        >
          创建面试安排
        </button>
        <button 
          v-if="resume.status === 'interview'" 
          class="btn btn-info" 
          @click="showOfferModal = true"
        >
          发起Offer
        </button>
      </div>
    </div>

    <div class="card" v-if="interviews.length > 0">
      <h3>面试安排</h3>
      <div class="interview-list">
        <div v-for="interview in interviews" :key="interview.id" class="interview-card">
          <div class="interview-header">
            <span class="interview-round">{{ interview.round }}</span>
            <span :class="['status-tag', `status-${interview.status}`]">{{ getInterviewStatusText(interview.status) }}</span>
          </div>
          <div class="interview-info">
            <div class="info-row">
              <span class="label">面试时间</span>
              <span class="value">{{ interview.interview_time }}</span>
            </div>
            <div class="info-row">
              <span class="label">面试方式</span>
              <span class="value">{{ interview.method }}</span>
            </div>
            <div class="info-row">
              <span class="label">面试官</span>
              <span class="value">{{ interview.interviewer }}</span>
            </div>
            <div class="info-row">
              <span class="label">地点/链接</span>
              <span class="value">{{ interview.location }}</span>
            </div>
            <div v-if="interview.remarks" class="info-row">
              <span class="label">备注</span>
              <span class="value">{{ interview.remarks }}</span>
            </div>
            <div v-if="interview.cancel_reason" class="info-row">
              <span class="label">取消原因</span>
              <span class="value cancel-reason">{{ interview.cancel_reason }}</span>
            </div>
          </div>
          <div class="interview-actions">
            <button v-if="interview.status === 'pending'" class="btn btn-sm btn-success" @click="confirmInterview(interview)">确认</button>
            <button v-if="interview.status === 'pending' || interview.status === 'confirmed'" class="btn btn-sm btn-primary" @click="editInterview(interview)">编辑</button>
            <button v-if="interview.status !== 'completed' && interview.status !== 'cancelled'" class="btn btn-sm btn-danger" @click="cancelInterview(interview)">取消</button>
            <button v-if="interview.status === 'confirmed'" class="btn btn-sm btn-success" @click="completeInterview(interview)">标记完成</button>
          </div>
        </div>
      </div>
    </div>

    <div class="card" v-if="offers.length > 0">
      <h3>Offer安排</h3>
      <div class="offer-list">
        <div v-for="offer in offers" :key="offer.id" class="offer-card">
          <div class="offer-header">
            <span class="offer-title">{{ jobTitle }}</span>
            <span :class="['status-tag', `status-${offer.status}`]">{{ getOfferStatusText(offer.status) }}</span>
          </div>
          <div class="offer-info">
            <div class="info-row">
              <span class="label">薪资范围</span>
              <span class="value">{{ offer.salary }}</span>
            </div>
            <div class="info-row">
              <span class="label">入职日期</span>
              <span class="value">{{ offer.start_date }}</span>
            </div>
            <div class="info-row">
              <span class="label">工作地点</span>
              <span class="value">{{ offer.work_location }}</span>
            </div>
            <div v-if="offer.probation_period" class="info-row">
              <span class="label">试用期</span>
              <span class="value">{{ offer.probation_period }}</span>
            </div>
            <div v-if="offer.department" class="info-row">
              <span class="label">直属部门</span>
              <span class="value">{{ offer.department }}</span>
            </div>
            <div v-if="offer.notes" class="info-row">
              <span class="label">补充说明</span>
              <span class="value">{{ offer.notes }}</span>
            </div>
            <div v-if="offer.reject_reason" class="info-row">
              <span class="label">拒绝原因</span>
              <span class="value cancel-reason">{{ offer.reject_reason }}</span>
            </div>
          </div>
          <div class="offer-actions">
            <button v-if="offer.status === 'draft'" class="btn btn-sm btn-primary" @click="editOffer(offer)">编辑</button>
            <button v-if="offer.status === 'draft'" class="btn btn-sm btn-success" @click="sendOffer(offer)">发送</button>
            <button v-if="offer.status === 'sent'" class="btn btn-sm btn-danger" @click="withdrawOffer(offer)">撤回</button>
          </div>
        </div>
      </div>
    </div>

    <div class="card" v-if="feedbacks.length > 0">
      <h3>面试反馈</h3>
      <div class="feedback-list">
        <div v-for="feedback in feedbacks" :key="feedback.id" class="feedback-card">
          <div class="feedback-header">
            <span class="feedback-round">{{ feedback.round }}</span>
            <span :class="['status-tag', `status-${getConclusionStatus(feedback.conclusion)}`]">{{ getConclusionText(feedback.conclusion) }}</span>
          </div>
          <div class="feedback-body">
            <div class="feedback-row">
              <span class="label">面试官</span>
              <span class="value">{{ feedback.interviewer }}</span>
            </div>
            <div class="feedback-row">
              <span class="label">评分</span>
              <span class="value">{{ feedback.score }}</span>
            </div>
            <div v-if="feedback.tags" class="feedback-row">
              <span class="label">评价标签</span>
              <span class="value">
                <span v-for="tag in feedback.tags.split(',')" :key="tag" class="tag">{{ tag.trim() }}</span>
              </span>
            </div>
            <div v-if="feedback.strengths" class="feedback-row">
              <span class="label">优势</span>
              <span class="value">{{ feedback.strengths }}</span>
            </div>
            <div v-if="feedback.risks" class="feedback-row">
              <span class="label">风险点</span>
              <span class="value">{{ feedback.risks }}</span>
            </div>
            <div v-if="feedback.remarks" class="feedback-row">
              <span class="label">结论建议</span>
              <span class="value">{{ feedback.remarks }}</span>
            </div>
          </div>
        </div>
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
        <div v-if="messages.length === 0" class="empty-messages">
          <p>暂无沟通记录</p>
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

    <div v-if="showInterviewModal" class="modal-overlay" @click.self="closeInterviewModal">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editingInterview ? '编辑面试安排' : '创建面试安排' }}</h3>
          <button class="btn-close" @click="closeInterviewModal">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>面试轮次</label>
            <select v-model="formData.round" class="form-control">
              <option value="初试">初试</option>
              <option value="复试">复试</option>
              <option value="终试">终试</option>
            </select>
          </div>
          <div class="form-group">
            <label>面试时间</label>
            <input type="datetime-local" v-model="formData.interview_time" class="form-control" />
          </div>
          <div class="form-group">
            <label>面试方式</label>
            <select v-model="formData.method" class="form-control">
              <option value="线上">线上</option>
              <option value="线下">线下</option>
              <option value="电话">电话</option>
            </select>
          </div>
          <div class="form-group">
            <label>面试官</label>
            <input type="text" v-model="formData.interviewer" class="form-control" placeholder="请输入面试官姓名" />
          </div>
          <div class="form-group">
            <label>地点/会议链接</label>
            <input type="text" v-model="formData.location" class="form-control" placeholder="请输入面试地点或会议链接" />
          </div>
          <div class="form-group">
            <label>备注</label>
            <textarea v-model="formData.remarks" class="form-control" rows="3" placeholder="请输入备注信息"></textarea>
          </div>
          <div v-if="editingInterview && editingInterview.status !== 'completed'" class="form-group">
            <label>取消原因</label>
            <input type="text" v-model="formData.cancel_reason" class="form-control" placeholder="取消面试时填写原因" />
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="closeInterviewModal">取消</button>
          <button class="btn btn-primary" @click="saveInterview">保存</button>
        </div>
      </div>
    </div>

    <div v-if="showOfferModal" class="modal-overlay" @click.self="closeOfferModal">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editingOffer ? '编辑Offer' : '发起Offer' }}</h3>
          <button class="btn-close" @click="closeOfferModal">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>薪资范围</label>
            <input type="text" v-model="offerForm.salary" class="form-control" placeholder="例如：30k-45k" />
          </div>
          <div class="form-group">
            <label>入职日期</label>
            <input type="date" v-model="offerForm.start_date" class="form-control" />
          </div>
          <div class="form-group">
            <label>工作地点</label>
            <input type="text" v-model="offerForm.work_location" class="form-control" placeholder="请输入工作地点" />
          </div>
          <div class="form-group">
            <label>试用期</label>
            <input type="text" v-model="offerForm.probation_period" class="form-control" placeholder="例如：3个月" />
          </div>
          <div class="form-group">
            <label>直属部门</label>
            <input type="text" v-model="offerForm.department" class="form-control" placeholder="请输入直属部门" />
          </div>
          <div class="form-group">
            <label>补充说明</label>
            <textarea v-model="offerForm.notes" class="form-control" rows="3" placeholder="请输入补充说明"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="closeOfferModal">取消</button>
          <button class="btn btn-primary" @click="saveOffer">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { resumeApi, jobApi, messageApi, interviewApi, offerApi, feedbackApi } from '../../api'

const emit = defineEmits(['update-stats'])

const route = useRoute()
const { state } = useUserStore()

const resume = ref(null)
const jobTitle = ref('')
const messages = ref([])
const newMessage = ref('')
const interviews = ref([])
const showInterviewModal = ref(false)
const editingInterview = ref(null)
const offers = ref([])
const showOfferModal = ref(false)
const editingOffer = ref(null)
const feedbacks = ref([])

const formData = ref({
  round: '初试',
  interview_time: '',
  method: '线上',
  interviewer: '',
  location: '',
  remarks: '',
  cancel_reason: ''
})

const offerForm = ref({
  salary: '',
  start_date: '',
  work_location: '',
  probation_period: '',
  department: '',
  notes: ''
})

const getStatusText = (status) => {
  const map = { applied: '已投递', pending: '待沟通', interview: '已约聊', rejected: '已拒绝' }
  return map[status] || status
}

const getInterviewStatusText = (status) => {
  const map = { pending: '待确认', confirmed: '已确认', completed: '已完成', cancelled: '已取消' }
  return map[status] || status
}

const getOfferStatusText = (status) => {
  const map = { draft: '待发送', sent: '已发送', accepted: '候选人已接受', rejected: '候选人已拒绝', withdrawn: '已撤回' }
  return map[status] || status
}

const getConclusionText = (conclusion) => {
  const map = { pending: '待定', pass: '通过', next_round: '进入下一轮', reject: '不通过' }
  return map[conclusion] || conclusion
}

const getConclusionStatus = (conclusion) => {
  const map = { pending: 'pending', pass: 'success', next_round: 'success', reject: 'rejected' }
  return map[conclusion] || 'pending'
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

const loadInterviews = async () => {
  if (!resume.value) return
  try {
    const response = await interviewApi.getInterviews({ resume_id: resume.value.id })
    interviews.value = response.data
  } catch (error) {
    console.error('Load interviews failed:', error)
  }
}

const closeInterviewModal = () => {
  showInterviewModal.value = false
  editingInterview.value = null
  formData.value = {
    round: '初试',
    interview_time: '',
    method: '线上',
    interviewer: '',
    location: '',
    remarks: '',
    cancel_reason: ''
  }
}

const editInterview = (interview) => {
  editingInterview.value = interview
  formData.value = {
    round: interview.round,
    interview_time: interview.interview_time.replace(' ', 'T'),
    method: interview.method,
    interviewer: interview.interviewer,
    location: interview.location,
    remarks: interview.remarks,
    cancel_reason: interview.cancel_reason
  }
  showInterviewModal.value = true
}

const saveInterview = async () => {
  if (!resume.value) return
  try {
    const data = {
      resume_id: resume.value.id,
      job_id: resume.value.job_id,
      candidate_id: resume.value.candidate_id,
      candidate_name: resume.value.candidate_name,
      round: formData.value.round,
      interview_time: formData.value.interview_time.replace('T', ' '),
      method: formData.value.method,
      interviewer: formData.value.interviewer,
      location: formData.value.location,
      remarks: formData.value.remarks,
      cancel_reason: formData.value.cancel_reason,
      status: editingInterview.value ? editingInterview.value.status : 'pending'
    }
    
    if (editingInterview.value) {
      await interviewApi.updateInterview(editingInterview.value.id, data)
    } else {
      await interviewApi.createInterview(data)
    }
    
    closeInterviewModal()
    loadInterviews()
    emit('update-stats')
  } catch (error) {
    console.error('Save interview failed:', error)
  }
}

const confirmInterview = async (interview) => {
  try {
    await interviewApi.updateInterview(interview.id, { ...interview, status: 'confirmed' })
    loadInterviews()
    emit('update-stats')
  } catch (error) {
    console.error('Confirm interview failed:', error)
  }
}

const cancelInterview = async (interview) => {
  const reason = prompt('请输入取消原因：')
  if (!reason) return
  try {
    await interviewApi.updateInterview(interview.id, { ...interview, status: 'cancelled', cancel_reason: reason })
    loadInterviews()
    emit('update-stats')
  } catch (error) {
    console.error('Cancel interview failed:', error)
  }
}

const completeInterview = async (interview) => {
  try {
    await interviewApi.updateInterview(interview.id, { ...interview, status: 'completed' })
    loadInterviews()
    emit('update-stats')
  } catch (error) {
    console.error('Complete interview failed:', error)
  }
}

const loadOffers = async () => {
  if (!resume.value) return
  try {
    const response = await offerApi.getOffers({ resume_id: resume.value.id })
    offers.value = response.data
  } catch (error) {
    console.error('Load offers failed:', error)
  }
}

const loadFeedbacks = async () => {
  if (!resume.value) return
  try {
    const response = await feedbackApi.getFeedbacks({ resume_id: resume.value.id })
    feedbacks.value = response.data
  } catch (error) {
    console.error('Load feedbacks failed:', error)
  }
}

const closeOfferModal = () => {
  showOfferModal.value = false
  editingOffer.value = null
  offerForm.value = {
    salary: '',
    start_date: '',
    work_location: '',
    probation_period: '',
    department: '',
    notes: ''
  }
}

const editOffer = (offer) => {
  editingOffer.value = offer
  offerForm.value = {
    salary: offer.salary,
    start_date: offer.start_date,
    work_location: offer.work_location,
    probation_period: offer.probation_period,
    department: offer.department,
    notes: offer.notes
  }
  showOfferModal.value = true
}

const saveOffer = async () => {
  if (!resume.value) return
  try {
    const data = {
      resume_id: resume.value.id,
      job_id: resume.value.job_id,
      candidate_id: resume.value.candidate_id,
      candidate_name: resume.value.candidate_name,
      salary: offerForm.value.salary,
      start_date: offerForm.value.start_date,
      work_location: offerForm.value.work_location,
      probation_period: offerForm.value.probation_period,
      department: offerForm.value.department,
      notes: offerForm.value.notes,
      status: editingOffer.value ? editingOffer.value.status : 'draft'
    }
    
    if (editingOffer.value) {
      await offerApi.updateOffer(editingOffer.value.id, data)
    } else {
      await offerApi.createOffer(data)
    }
    
    closeOfferModal()
    loadOffers()
    emit('update-stats')
  } catch (error) {
    console.error('Save offer failed:', error)
  }
}

const sendOffer = async (offer) => {
  try {
    await offerApi.updateOffer(offer.id, { ...offer, status: 'sent' })
    loadOffers()
    emit('update-stats')
  } catch (error) {
    console.error('Send offer failed:', error)
  }
}

const withdrawOffer = async (offer) => {
  try {
    await offerApi.updateOffer(offer.id, { ...offer, status: 'withdrawn' })
    loadOffers()
    emit('update-stats')
  } catch (error) {
    console.error('Withdraw offer failed:', error)
  }
}

const loadData = async () => {
  try {
    const resumeRes = await resumeApi.getResume(route.params.id)
    resume.value = resumeRes.data
    
    if (resume.value.job_id) {
      const jobRes = await jobApi.getJob(resume.value.job_id)
      jobTitle.value = jobRes.data.title
    }
    
    loadMessages()
    loadInterviews()
    loadOffers()
    loadFeedbacks()
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

.resume-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.candidate-name {
  font-size: 24px;
  font-weight: bold;
}

.resume-summary {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
  padding: 16px;
  background-color: #fafafa;
  border-radius: 8px;
}

.summary-item {
  display: flex;
  flex-direction: column;
}

.summary-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}

.summary-value {
  font-size: 16px;
  font-weight: 500;
}

.resume-section {
  margin-bottom: 24px;
}

.resume-section h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  color: #333;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.info-item {
  display: flex;
  flex-direction: column;
  padding: 12px;
  background-color: #fafafa;
  border-radius: 8px;
}

.info-item .label {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}

.info-item .value {
  font-size: 14px;
  color: #333;
}

.cancel-reason {
  color: #f56c6c;
}

.resume-text {
  padding: 16px;
  background-color: #fafafa;
  border-radius: 8px;
  line-height: 1.8;
  color: #666;
  white-space: pre-wrap;
}

.status-flow {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background-color: #fafafa;
  border-radius: 8px;
}

.flow-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.flow-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  color: #999;
}

.flow-item.active .flow-circle {
  background-color: #409eff;
  color: white;
}

.flow-item.done .flow-circle {
  background-color: #67c23a;
  color: white;
}

.flow-item span {
  font-size: 12px;
  color: #666;
}

.flow-item.active span {
  color: #409eff;
  font-weight: 500;
}

.flow-arrow {
  color: #999;
  font-size: 18px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
  flex-wrap: wrap;
}

.interview-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.interview-card {
  padding: 16px;
  background-color: #fafafa;
  border-radius: 8px;
}

.interview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.interview-round {
  font-weight: bold;
  font-size: 16px;
}

.interview-info {
  margin-bottom: 12px;
}

.interview-info .info-row {
  display: flex;
  margin-bottom: 8px;
}

.interview-info .info-row:last-child {
  margin-bottom: 0;
}

.interview-info .label {
  width: 100px;
  color: #999;
  font-size: 14px;
}

.interview-info .value {
  flex: 1;
  font-size: 14px;
}

.interview-actions {
  display: flex;
  gap: 8px;
}

.btn-sm {
  padding: 4px 12px;
  font-size: 12px;
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

.empty-messages {
  text-align: center;
  padding: 20px;
  color: #999;
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h3 {
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid #f0f0f0;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

textarea.form-control {
  resize: vertical;
}

.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feedback-card {
  padding: 16px;
  background-color: #fafafa;
  border-radius: 8px;
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.feedback-round {
  font-weight: bold;
  font-size: 16px;
}

.feedback-body {
  margin-bottom: 12px;
}

.feedback-row {
  display: flex;
  margin-bottom: 8px;
}

.feedback-row:last-child {
  margin-bottom: 0;
}

.feedback-row .label {
  width: 100px;
  color: #999;
  font-size: 14px;
}

.feedback-row .value {
  flex: 1;
  font-size: 14px;
}

.tag {
  padding: 4px 12px;
  background-color: #ecf5ff;
  color: #409eff;
  border-radius: 4px;
  font-size: 12px;
  margin-right: 8px;
}
</style>