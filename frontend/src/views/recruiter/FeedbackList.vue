<template>
  <div class="feedback-list">
    <div class="list-header">
      <h2>面试反馈</h2>
    </div>

    <div class="filter-bar">
      <input 
        v-model="keywordFilter" 
        type="text" 
        placeholder="搜索候选人姓名、职位..." 
        class="search-input"
      />
      <select v-model="conclusionFilter" class="filter-select">
        <option value="">全部结论</option>
        <option value="pass">通过</option>
        <option value="next_round">进入下一轮</option>
        <option value="pending">待定</option>
        <option value="reject">不通过</option>
      </select>
      <select v-model="roundFilter" class="filter-select">
        <option value="">全部轮次</option>
        <option value="初试">初试</option>
        <option value="复试">复试</option>
        <option value="终试">终试</option>
      </select>
    </div>

    <div class="card">
      <table class="table">
        <thead>
          <tr>
            <th>职位名称</th>
            <th>候选人</th>
            <th>面试轮次</th>
            <th>面试官</th>
            <th>评分</th>
            <th>结论</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredFeedbacks" :key="item.feedback.id">
            <td>{{ item.job?.title || '未知职位' }}</td>
            <td>{{ item.feedback.candidate_name }}</td>
            <td>{{ item.feedback.round }}</td>
            <td>{{ item.feedback.interviewer }}</td>
            <td>{{ item.feedback.score }}</td>
            <td>
              <span :class="['status-tag', `status-${getConclusionStatus(item.feedback.conclusion)}`]">{{ getConclusionText(item.feedback.conclusion) }}</span>
            </td>
            <td>
              <button class="btn btn-sm btn-outline" @click="viewDetail(item.feedback)">查看</button>
              <button class="btn btn-sm btn-primary" @click="editFeedback(item.feedback)">编辑</button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="filteredFeedbacks.length === 0" class="empty-state">
        <div class="empty-icon">📝</div>
        <p>暂无面试反馈</p>
      </div>
    </div>

    <div v-if="showDetailModal" class="modal-overlay" @click.self="closeDetailModal">
      <div class="modal">
        <div class="modal-header">
          <h3>反馈详情</h3>
          <button class="btn-close" @click="closeDetailModal">×</button>
        </div>
        <div class="modal-body" v-if="selectedFeedback">
          <div class="detail-section">
            <h4>基本信息</h4>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">职位名称</span>
                <span class="value">{{ selectedJob?.title || '未知职位' }}</span>
              </div>
              <div class="info-item">
                <span class="label">候选人</span>
                <span class="value">{{ selectedFeedback.candidate_name }}</span>
              </div>
              <div class="info-item">
                <span class="label">面试轮次</span>
                <span class="value">{{ selectedFeedback.round }}</span>
              </div>
              <div class="info-item">
                <span class="label">面试官</span>
                <span class="value">{{ selectedFeedback.interviewer }}</span>
              </div>
              <div class="info-item">
                <span class="label">评分</span>
                <span class="value">{{ selectedFeedback.score }}</span>
              </div>
              <div class="info-item">
                <span class="label">结论</span>
                <span :class="['status-tag', `status-${getConclusionStatus(selectedFeedback.conclusion)}`]">{{ getConclusionText(selectedFeedback.conclusion) }}</span>
              </div>
            </div>
          </div>
          
          <div v-if="selectedFeedback.tags" class="detail-section">
            <h4>评价标签</h4>
            <div class="tags">
              <span v-for="tag in selectedFeedback.tags.split(',')" :key="tag" class="tag">{{ tag.trim() }}</span>
            </div>
          </div>

          <div v-if="selectedFeedback.strengths" class="detail-section">
            <h4>优势</h4>
            <p>{{ selectedFeedback.strengths }}</p>
          </div>

          <div v-if="selectedFeedback.risks" class="detail-section">
            <h4>风险点</h4>
            <p class="risk-text">{{ selectedFeedback.risks }}</p>
          </div>

          <div v-if="selectedFeedback.remarks" class="detail-section">
            <h4>结论建议</h4>
            <p>{{ selectedFeedback.remarks }}</p>
          </div>

          <div v-if="selectedFeedback.external_feedback" class="detail-section">
            <h4>对外反馈摘要</h4>
            <p>{{ selectedFeedback.external_feedback }}</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="closeDetailModal">关闭</button>
        </div>
      </div>
    </div>

    <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editingFeedback ? '编辑面试反馈' : '新增面试反馈' }}</h3>
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
            <label>面试官</label>
            <input type="text" v-model="formData.interviewer" class="form-control" placeholder="请输入面试官姓名" />
          </div>
          <div class="form-group">
            <label>评分 (0-100)</label>
            <input type="number" v-model="formData.score" class="form-control" min="0" max="100" placeholder="请输入评分" />
          </div>
          <div class="form-group">
            <label>评价标签（逗号分隔）</label>
            <input type="text" v-model="formData.tags" class="form-control" placeholder="例如：技术能力强,沟通流畅" />
          </div>
          <div class="form-group">
            <label>优势</label>
            <textarea v-model="formData.strengths" class="form-control" rows="3" placeholder="请输入候选人优势"></textarea>
          </div>
          <div class="form-group">
            <label>风险点</label>
            <textarea v-model="formData.risks" class="form-control" rows="3" placeholder="请输入风险点"></textarea>
          </div>
          <div class="form-group">
            <label>结论</label>
            <select v-model="formData.conclusion" class="form-control">
              <option value="pending">待定</option>
              <option value="pass">通过</option>
              <option value="next_round">进入下一轮</option>
              <option value="reject">不通过</option>
            </select>
          </div>
          <div class="form-group">
            <label>结论建议</label>
            <textarea v-model="formData.remarks" class="form-control" rows="3" placeholder="请输入结论建议"></textarea>
          </div>
          <div v-if="formData.conclusion === 'reject'" class="form-group">
            <label>对外反馈摘要（将展示给候选人）</label>
            <textarea v-model="formData.external_feedback" class="form-control" rows="3" placeholder="请输入对外反馈内容"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="closeEditModal">取消</button>
          <button class="btn btn-primary" @click="saveFeedback">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../../stores/user'
import { jobApi, feedbackApi, interviewApi } from '../../api'

const emit = defineEmits(['update-stats'])

const { state } = useUserStore()
const jobs = ref([])
const feedbacks = ref([])
const keywordFilter = ref('')
const conclusionFilter = ref('')
const roundFilter = ref('')

const showDetailModal = ref(false)
const showEditModal = ref(false)
const selectedFeedback = ref(null)
const selectedJob = ref(null)
const editingFeedback = ref(null)

const formData = ref({
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

const filteredFeedbacks = computed(() => {
  const myJobIds = jobs.value.filter(j => j.recruiter_id === state.currentUser?.id).map(j => j.id)
  
  let result = feedbacks.value
    .filter(f => myJobIds.includes(f.job_id))
    .map(f => ({
      feedback: f,
      job: jobs.value.find(j => j.id === f.job_id)
    }))
  
  if (keywordFilter.value) {
    const keyword = keywordFilter.value.toLowerCase()
    result = result.filter(item => 
      item.feedback.candidate_name.toLowerCase().includes(keyword) ||
      item.job?.title.toLowerCase().includes(keyword)
    )
  }
  
  if (conclusionFilter.value) {
    result = result.filter(item => item.feedback.conclusion === conclusionFilter.value)
  }
  
  if (roundFilter.value) {
    result = result.filter(item => item.feedback.round === roundFilter.value)
  }
  
  return result
})

const viewDetail = async (feedback) => {
  selectedFeedback.value = feedback
  selectedJob.value = jobs.value.find(j => j.id === feedback.job_id)
  showDetailModal.value = true
}

const closeDetailModal = () => {
  showDetailModal.value = false
  selectedFeedback.value = null
  selectedJob.value = null
}

const editFeedback = (feedback) => {
  editingFeedback.value = feedback
  formData.value = {
    interview_id: feedback.interview_id,
    resume_id: feedback.resume_id,
    job_id: feedback.job_id,
    candidate_id: feedback.candidate_id,
    candidate_name: feedback.candidate_name,
    round: feedback.round,
    interviewer: feedback.interviewer,
    score: feedback.score,
    tags: feedback.tags,
    strengths: feedback.strengths,
    risks: feedback.risks,
    conclusion: feedback.conclusion,
    remarks: feedback.remarks,
    external_feedback: feedback.external_feedback
  }
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  editingFeedback.value = null
  formData.value = {
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
  }
}

const saveFeedback = async () => {
  try {
    if (editingFeedback.value) {
      await feedbackApi.updateFeedback(editingFeedback.value.id, formData.value)
    } else {
      await feedbackApi.createFeedback(formData.value)
    }
    closeEditModal()
    loadData()
    emit('update-stats')
  } catch (error) {
    console.error('Save feedback failed:', error)
  }
}

const loadData = async () => {
  try {
    const [jobsRes, feedbacksRes] = await Promise.all([
      jobApi.getJobs(),
      feedbackApi.getFeedbacks({ recruiter_id: state.currentUser?.id })
    ])
    jobs.value = jobsRes.data
    feedbacks.value = feedbacksRes.data
  } catch (error) {
    console.error('Failed to load data:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.feedback-list {
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
  max-width: 600px;
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

.risk-text {
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

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 4px 12px;
  background-color: #ecf5ff;
  color: #409eff;
  border-radius: 4px;
  font-size: 12px;
}
</style>