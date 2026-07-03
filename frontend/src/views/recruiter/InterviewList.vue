<template>
  <div class="interview-list">
    <div class="list-header">
      <h2>面试安排</h2>
    </div>

    <div class="filter-bar">
      <input 
        v-model="keywordFilter" 
        type="text" 
        placeholder="搜索候选人姓名、职位..." 
        class="search-input"
      />
      <select v-model="statusFilter" class="filter-select">
        <option value="">全部状态</option>
        <option value="pending">待确认</option>
        <option value="confirmed">已确认</option>
        <option value="completed">已完成</option>
        <option value="cancelled">已取消</option>
      </select>
      <input 
        v-model="dateFilter" 
        type="date" 
        class="search-input date-input"
      />
    </div>

    <div class="card">
      <table class="table">
        <thead>
          <tr>
            <th>职位名称</th>
            <th>候选人</th>
            <th>面试轮次</th>
            <th>面试时间</th>
            <th>方式</th>
            <th>面试官</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredInterviews" :key="item.interview.id">
            <td>{{ item.job?.title || '未知职位' }}</td>
            <td>{{ item.interview.candidate_name }}</td>
            <td>{{ item.interview.round }}</td>
            <td>{{ item.interview.interview_time }}</td>
            <td>{{ item.interview.method }}</td>
            <td>{{ item.interview.interviewer }}</td>
            <td>
              <span :class="['status-tag', `status-${item.interview.status}`]">{{ getStatusText(item.interview.status) }}</span>
            </td>
            <td>
              <button class="btn btn-sm btn-outline" @click="viewDetail(item.interview)">查看</button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="filteredInterviews.length === 0" class="empty-state">
        <div class="empty-icon">📅</div>
        <p>暂无面试安排</p>
      </div>
    </div>

    <div v-if="showDetailModal" class="modal-overlay" @click.self="closeDetailModal">
      <div class="modal">
        <div class="modal-header">
          <h3>面试详情</h3>
          <button class="btn-close" @click="closeDetailModal">×</button>
        </div>
        <div class="modal-body" v-if="selectedInterview">
          <div class="detail-section">
            <h4>基本信息</h4>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">职位名称</span>
                <span class="value">{{ selectedJob?.title || '未知职位' }}</span>
              </div>
              <div class="info-item">
                <span class="label">候选人</span>
                <span class="value">{{ selectedInterview.candidate_name }}</span>
              </div>
              <div class="info-item">
                <span class="label">面试轮次</span>
                <span class="value">{{ selectedInterview.round }}</span>
              </div>
              <div class="info-item">
                <span class="label">当前状态</span>
                <span :class="['status-tag', `status-${selectedInterview.status}`]">{{ getStatusText(selectedInterview.status) }}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h4>面试安排</h4>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">面试时间</span>
                <span class="value">{{ selectedInterview.interview_time }}</span>
              </div>
              <div class="info-item">
                <span class="label">面试方式</span>
                <span class="value">{{ selectedInterview.method }}</span>
              </div>
              <div class="info-item">
                <span class="label">面试官</span>
                <span class="value">{{ selectedInterview.interviewer }}</span>
              </div>
              <div class="info-item">
                <span class="label">地点/链接</span>
                <span class="value">{{ selectedInterview.location }}</span>
              </div>
            </div>
          </div>

          <div v-if="selectedInterview.remarks" class="detail-section">
            <h4>备注</h4>
            <p>{{ selectedInterview.remarks }}</p>
          </div>

          <div v-if="selectedInterview.cancel_reason" class="detail-section">
            <h4>取消原因</h4>
            <p class="cancel-reason">{{ selectedInterview.cancel_reason }}</p>
          </div>

          <div v-if="feedbacks.length > 0" class="detail-section">
            <h4>面试反馈</h4>
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
        <div class="modal-footer" v-if="selectedInterview">
          <button v-if="selectedInterview.status === 'pending'" class="btn btn-success" @click="confirmInterview">确认面试</button>
          <button v-if="selectedInterview.status === 'pending' || selectedInterview.status === 'confirmed'" class="btn btn-primary" @click="editInterview">编辑</button>
          <button v-if="selectedInterview.status !== 'completed' && selectedInterview.status !== 'cancelled'" class="btn btn-danger" @click="cancelInterview">取消面试</button>
          <button v-if="selectedInterview.status === 'confirmed'" class="btn btn-success" @click="completeInterview">标记完成</button>
          <button v-if="selectedInterview.status === 'completed'" class="btn btn-info" @click="openFeedbackModal">{{ feedbacks.length > 0 ? '编辑反馈' : '添加反馈' }}</button>
          <button class="btn btn-outline" @click="closeDetailModal">关闭</button>
        </div>
      </div>
    </div>

    <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal">
        <div class="modal-header">
          <h3>编辑面试安排</h3>
          <button class="btn-close" @click="closeEditModal">×</button>
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
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="closeEditModal">取消</button>
          <button class="btn btn-primary" @click="saveInterview">保存</button>
        </div>
      </div>
    </div>

    <div v-if="showFeedbackModal" class="modal-overlay" @click.self="closeFeedbackModal">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editingFeedback ? '编辑面试反馈' : '新增面试反馈' }}</h3>
          <button class="btn-close" @click="closeFeedbackModal">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>面试轮次</label>
            <select v-model="feedbackForm.round" class="form-control">
              <option value="初试">初试</option>
              <option value="复试">复试</option>
              <option value="终试">终试</option>
            </select>
          </div>
          <div class="form-group">
            <label>面试官</label>
            <input type="text" v-model="feedbackForm.interviewer" class="form-control" placeholder="请输入面试官姓名" />
          </div>
          <div class="form-group">
            <label>评分 (0-100)</label>
            <input type="number" v-model="feedbackForm.score" class="form-control" min="0" max="100" placeholder="请输入评分" />
          </div>
          <div class="form-group">
            <label>评价标签（逗号分隔）</label>
            <input type="text" v-model="feedbackForm.tags" class="form-control" placeholder="例如：技术能力强,沟通流畅" />
          </div>
          <div class="form-group">
            <label>优势</label>
            <textarea v-model="feedbackForm.strengths" class="form-control" rows="3" placeholder="请输入候选人优势"></textarea>
          </div>
          <div class="form-group">
            <label>风险点</label>
            <textarea v-model="feedbackForm.risks" class="form-control" rows="3" placeholder="请输入风险点"></textarea>
          </div>
          <div class="form-group">
            <label>结论</label>
            <select v-model="feedbackForm.conclusion" class="form-control">
              <option value="pending">待定</option>
              <option value="pass">通过</option>
              <option value="next_round">进入下一轮</option>
              <option value="reject">不通过</option>
            </select>
          </div>
          <div class="form-group">
            <label>结论建议</label>
            <textarea v-model="feedbackForm.remarks" class="form-control" rows="3" placeholder="请输入结论建议"></textarea>
          </div>
          <div v-if="feedbackForm.conclusion === 'reject'" class="form-group">
            <label>对外反馈摘要（将展示给候选人）</label>
            <textarea v-model="feedbackForm.external_feedback" class="form-control" rows="3" placeholder="请输入对外反馈内容"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="closeFeedbackModal">取消</button>
          <button class="btn btn-primary" @click="saveFeedback">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../../stores/user'
import { jobApi, interviewApi, feedbackApi } from '../../api'

const emit = defineEmits(['update-stats'])

const { state } = useUserStore()
const jobs = ref([])
const interviews = ref([])
const keywordFilter = ref('')
const statusFilter = ref('')
const dateFilter = ref('')

const showDetailModal = ref(false)
const showEditModal = ref(false)
const showFeedbackModal = ref(false)
const selectedInterview = ref(null)
const selectedJob = ref(null)
const feedbacks = ref([])
const editingFeedback = ref(null)

const formData = ref({
  round: '初试',
  interview_time: '',
  method: '线上',
  interviewer: '',
  location: '',
  remarks: ''
})

const feedbackForm = ref({
  interview_id: 0,
  resume_id: 0,
  job_id: 0,
  candidate_id: 0,
  candidate_name: '',
  round: '初试',
  interviewer: '',
  score: 0,
  tags: '',
  strengths: '',
  risks: '',
  conclusion: 'pending',
  remarks: '',
  external_feedback: ''
})

const getConclusionText = (conclusion) => {
  const map = { pending: '待定', pass: '通过', next_round: '进入下一轮', reject: '不通过' }
  return map[conclusion] || conclusion
}

const getConclusionStatus = (conclusion) => {
  const map = { pending: 'pending', pass: 'success', next_round: 'success', reject: 'rejected' }
  return map[conclusion] || 'pending'
}

const getStatusText = (status) => {
  const map = { pending: '待确认', confirmed: '已确认', completed: '已完成', cancelled: '已取消' }
  return map[status] || status
}

const filteredInterviews = computed(() => {
  const myJobIds = jobs.value.filter(j => j.recruiter_id === state.currentUser?.id).map(j => j.id)
  
  let result = interviews.value
    .filter(i => myJobIds.includes(i.job_id))
    .map(i => ({
      interview: i,
      job: jobs.value.find(j => j.id === i.job_id)
    }))
  
  if (keywordFilter.value) {
    const keyword = keywordFilter.value.toLowerCase()
    result = result.filter(item => 
      item.interview.candidate_name.toLowerCase().includes(keyword) ||
      item.job?.title.toLowerCase().includes(keyword)
    )
  }
  
  if (statusFilter.value) {
    result = result.filter(item => item.interview.status === statusFilter.value)
  }
  
  if (dateFilter.value) {
    result = result.filter(item => item.interview.interview_time.startsWith(dateFilter.value))
  }
  
  return result
})

const viewDetail = async (interview) => {
  selectedInterview.value = interview
  selectedJob.value = jobs.value.find(j => j.id === interview.job_id)
  showDetailModal.value = true
  loadFeedbacks(interview.id)
}

const closeDetailModal = () => {
  showDetailModal.value = false
  selectedInterview.value = null
  selectedJob.value = null
}

const loadFeedbacks = async (interviewId) => {
  try {
    const response = await feedbackApi.getFeedbacks({ interview_id: interviewId })
    feedbacks.value = response.data
  } catch (error) {
    console.error('Load feedbacks failed:', error)
  }
}

const openFeedbackModal = () => {
  if (!selectedInterview.value) return
  const existingFeedback = feedbacks.value.find(f => f.interview_id === selectedInterview.value.id)
  if (existingFeedback) {
    editingFeedback.value = existingFeedback
    feedbackForm.value = {
      interview_id: existingFeedback.interview_id,
      resume_id: existingFeedback.resume_id,
      job_id: existingFeedback.job_id,
      candidate_id: existingFeedback.candidate_id,
      candidate_name: existingFeedback.candidate_name,
      round: existingFeedback.round,
      interviewer: existingFeedback.interviewer,
      score: existingFeedback.score,
      tags: existingFeedback.tags,
      strengths: existingFeedback.strengths,
      risks: existingFeedback.risks,
      conclusion: existingFeedback.conclusion,
      remarks: existingFeedback.remarks,
      external_feedback: existingFeedback.external_feedback
    }
  } else {
    editingFeedback.value = null
    feedbackForm.value = {
      interview_id: selectedInterview.value.id,
      resume_id: selectedInterview.value.resume_id,
      job_id: selectedInterview.value.job_id,
      candidate_id: selectedInterview.value.candidate_id,
      candidate_name: selectedInterview.value.candidate_name,
      round: selectedInterview.value.round,
      interviewer: selectedInterview.value.interviewer,
      score: 0,
      tags: '',
      strengths: '',
      risks: '',
      conclusion: 'pending',
      remarks: '',
      external_feedback: ''
    }
  }
  showFeedbackModal.value = true
}

const closeFeedbackModal = () => {
  showFeedbackModal.value = false
  editingFeedback.value = null
}

const saveFeedback = async () => {
  try {
    if (editingFeedback.value) {
      await feedbackApi.updateFeedback(editingFeedback.value.id, feedbackForm.value)
    } else {
      await feedbackApi.createFeedback(feedbackForm.value)
    }
    closeFeedbackModal()
    loadFeedbacks(selectedInterview.value.id)
    emit('update-stats')
  } catch (error) {
    console.error('Save feedback failed:', error)
  }
}

const editInterview = () => {
  if (!selectedInterview.value) return
  formData.value = {
    round: selectedInterview.value.round,
    interview_time: selectedInterview.value.interview_time.replace(' ', 'T'),
    method: selectedInterview.value.method,
    interviewer: selectedInterview.value.interviewer,
    location: selectedInterview.value.location,
    remarks: selectedInterview.value.remarks
  }
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
}

const saveInterview = async () => {
  if (!selectedInterview.value) return
  try {
    const data = {
      ...selectedInterview.value,
      round: formData.value.round,
      interview_time: formData.value.interview_time.replace('T', ' '),
      method: formData.value.method,
      interviewer: formData.value.interviewer,
      location: formData.value.location,
      remarks: formData.value.remarks
    }
    
    await interviewApi.updateInterview(selectedInterview.value.id, data)
    closeEditModal()
    closeDetailModal()
    loadData()
    emit('update-stats')
  } catch (error) {
    console.error('Save interview failed:', error)
  }
}

const confirmInterview = async () => {
  if (!selectedInterview.value) return
  try {
    await interviewApi.updateInterview(selectedInterview.value.id, { ...selectedInterview.value, status: 'confirmed' })
    closeDetailModal()
    loadData()
    emit('update-stats')
  } catch (error) {
    console.error('Confirm interview failed:', error)
  }
}

const cancelInterview = async () => {
  if (!selectedInterview.value) return
  const reason = prompt('请输入取消原因：')
  if (!reason) return
  try {
    await interviewApi.updateInterview(selectedInterview.value.id, { ...selectedInterview.value, status: 'cancelled', cancel_reason: reason })
    closeDetailModal()
    loadData()
    emit('update-stats')
  } catch (error) {
    console.error('Cancel interview failed:', error)
  }
}

const completeInterview = async () => {
  if (!selectedInterview.value) return
  try {
    await interviewApi.updateInterview(selectedInterview.value.id, { ...selectedInterview.value, status: 'completed' })
    closeDetailModal()
    loadData()
    emit('update-stats')
  } catch (error) {
    console.error('Complete interview failed:', error)
  }
}

const loadData = async () => {
  try {
    const [jobsRes, interviewsRes] = await Promise.all([
      jobApi.getJobs(),
      interviewApi.getInterviews({ recruiter_id: state.currentUser?.id })
    ])
    jobs.value = jobsRes.data
    interviews.value = interviewsRes.data
  } catch (error) {
    console.error('Failed to load data:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.interview-list {
  max-width: 1200px;
  margin: 0 auto;
}

.list-header {
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

.date-input {
  max-width: 150px;
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

.btn-sm {
  padding: 4px 12px;
  font-size: 12px;
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
  flex-wrap: wrap;
}

.detail-section {
  margin-bottom: 20px;
}

.detail-section h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #999;
}

.detail-section p {
  margin: 0;
  padding: 12px;
  background-color: #fafafa;
  border-radius: 8px;
  line-height: 1.6;
}

.cancel-reason {
  color: #f56c6c;
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
  gap: 12px;
}

.feedback-card {
  padding: 12px;
  background-color: #fafafa;
  border-radius: 6px;
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.feedback-round {
  font-weight: bold;
  font-size: 14px;
}

.feedback-body {
  margin-bottom: 8px;
}

.feedback-row {
  display: flex;
  margin-bottom: 6px;
}

.feedback-row:last-child {
  margin-bottom: 0;
}

.feedback-row .label {
  width: 80px;
  color: #999;
  font-size: 13px;
}

.feedback-row .value {
  flex: 1;
  font-size: 13px;
}

.tag {
  padding: 3px 10px;
  background-color: #ecf5ff;
  color: #409eff;
  border-radius: 4px;
  font-size: 12px;
  margin-right: 6px;
}
</style>