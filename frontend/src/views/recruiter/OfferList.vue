<template>
  <div class="offer-list-page">
    <div class="page-header">
      <h2>Offer列表</h2>
    </div>

    <div class="filter-bar">
      <input v-model="keywordFilter" type="text" placeholder="搜索候选人姓名、职位..." />
      <select v-model="statusFilter" class="form-control">
        <option value="">全部状态</option>
        <option value="draft">待发送</option>
        <option value="sent">已发送</option>
        <option value="accepted">候选人已接受</option>
        <option value="rejected">候选人已拒绝</option>
        <option value="withdrawn">已撤回</option>
      </select>
      <select v-model="jobFilter" class="form-control">
        <option value="">全部职位</option>
        <option v-for="job in jobs" :key="job.id" :value="job.id">{{ job.title }}</option>
      </select>
      <button class="btn btn-outline" @click="clearFilters">重置</button>
    </div>

    <table class="table">
      <thead>
        <tr>
          <th>职位名称</th>
          <th>候选人</th>
          <th>薪资</th>
          <th>入职日期</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="offer in filteredOffers" :key="offer.id">
          <td>{{ getJobTitle(offer.job_id) }}</td>
          <td>{{ offer.candidate_name }}</td>
          <td>{{ offer.salary }}</td>
          <td>{{ offer.start_date }}</td>
          <td><span :class="['status-tag', `status-${offer.status}`]">{{ getStatusText(offer.status) }}</span></td>
          <td>
            <button class="btn btn-sm btn-primary" @click="viewOffer(offer)">查看</button>
            <button v-if="offer.status === 'draft'" class="btn btn-sm btn-info" @click="editOffer(offer)">编辑</button>
            <button v-if="offer.status === 'draft'" class="btn btn-sm btn-success" @click="sendOffer(offer)">发送</button>
            <button v-if="offer.status === 'sent'" class="btn btn-sm btn-danger" @click="withdrawOffer(offer)">撤回</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="filteredOffers.length === 0" class="empty-state">
      <p>暂无Offer</p>
    </div>

    <div v-if="showOfferModal" class="modal-overlay" @click.self="closeOfferModal">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editingOffer ? '编辑Offer' : 'Offer详情' }}</h3>
          <button class="btn-close" @click="closeOfferModal">×</button>
        </div>
        <div class="modal-body" v-if="currentOffer">
          <div v-if="editingOffer" class="form-group">
            <label>薪资范围</label>
            <input type="text" v-model="offerForm.salary" class="form-control" />
          </div>
          <div v-else>
            <div class="detail-row">
              <span class="label">职位名称</span>
              <span class="value">{{ getJobTitle(currentOffer.job_id) }}</span>
            </div>
            <div class="detail-row">
              <span class="label">候选人</span>
              <span class="value">{{ currentOffer.candidate_name }}</span>
            </div>
          </div>
          <div v-if="editingOffer" class="form-group">
            <label>入职日期</label>
            <input type="date" v-model="offerForm.start_date" class="form-control" />
          </div>
          <div v-else>
            <div class="detail-row">
              <span class="label">薪资范围</span>
              <span class="value">{{ currentOffer.salary }}</span>
            </div>
            <div class="detail-row">
              <span class="label">入职日期</span>
              <span class="value">{{ currentOffer.start_date }}</span>
            </div>
          </div>
          <div v-if="editingOffer" class="form-group">
            <label>工作地点</label>
            <input type="text" v-model="offerForm.work_location" class="form-control" />
          </div>
          <div v-else>
            <div class="detail-row">
              <span class="label">工作地点</span>
              <span class="value">{{ currentOffer.work_location }}</span>
            </div>
          </div>
          <div v-if="editingOffer" class="form-group">
            <label>试用期</label>
            <input type="text" v-model="offerForm.probation_period" class="form-control" />
          </div>
          <div v-else>
            <div class="detail-row">
              <span class="label">试用期</span>
              <span class="value">{{ currentOffer.probation_period || '-' }}</span>
            </div>
          </div>
          <div v-if="editingOffer" class="form-group">
            <label>直属部门</label>
            <input type="text" v-model="offerForm.department" class="form-control" />
          </div>
          <div v-else>
            <div class="detail-row">
              <span class="label">直属部门</span>
              <span class="value">{{ currentOffer.department || '-' }}</span>
            </div>
          </div>
          <div v-if="editingOffer" class="form-group">
            <label>补充说明</label>
            <textarea v-model="offerForm.notes" class="form-control" rows="3"></textarea>
          </div>
          <div v-else>
            <div class="detail-row">
              <span class="label">补充说明</span>
              <span class="value">{{ currentOffer.notes || '-' }}</span>
            </div>
            <div v-if="currentOffer.reject_reason" class="detail-row">
              <span class="label">拒绝原因</span>
              <span class="value reject-reason">{{ currentOffer.reject_reason }}</span>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="closeOfferModal">关闭</button>
          <button v-if="editingOffer" class="btn btn-primary" @click="saveOffer">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../../stores/user'
import { offerApi, jobApi } from '../../api'

const { state } = useUserStore()

const offers = ref([])
const jobs = ref([])
const keywordFilter = ref('')
const statusFilter = ref('')
const jobFilter = ref('')
const showOfferModal = ref(false)
const currentOffer = ref(null)
const editingOffer = ref(null)

const offerForm = ref({
  salary: '',
  start_date: '',
  work_location: '',
  probation_period: '',
  department: '',
  notes: ''
})

const getStatusText = (status) => {
  const map = { draft: '待发送', sent: '已发送', accepted: '候选人已接受', rejected: '候选人已拒绝', withdrawn: '已撤回' }
  return map[status] || status
}

const getJobTitle = (jobId) => {
  const job = jobs.value.find(j => j.id === jobId)
  return job ? job.title : ''
}

const filteredOffers = computed(() => {
  return offers.value.filter(offer => {
    const matchKeyword = !keywordFilter.value || 
      offer.candidate_name.includes(keywordFilter.value) || 
      getJobTitle(offer.job_id).includes(keywordFilter.value)
    const matchStatus = !statusFilter.value || offer.status === statusFilter.value
    const matchJob = !jobFilter.value || offer.job_id === parseInt(jobFilter.value)
    return matchKeyword && matchStatus && matchJob
  })
})

const loadOffers = async () => {
  try {
    const response = await offerApi.getOffers({ recruiter_id: state.currentUser?.id || 1 })
    offers.value = response.data
  } catch (error) {
    console.error('Load offers failed:', error)
  }
}

const loadJobs = async () => {
  try {
    const response = await jobApi.getJobs({ recruiter_id: state.currentUser?.id || 1 })
    jobs.value = response.data
  } catch (error) {
    console.error('Load jobs failed:', error)
  }
}

const clearFilters = () => {
  keywordFilter.value = ''
  statusFilter.value = ''
  jobFilter.value = ''
}

const viewOffer = (offer) => {
  currentOffer.value = offer
  editingOffer.value = null
  showOfferModal.value = true
}

const editOffer = (offer) => {
  currentOffer.value = offer
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

const closeOfferModal = () => {
  showOfferModal.value = false
  currentOffer.value = null
  editingOffer.value = null
}

const saveOffer = async () => {
  if (!editingOffer.value) return
  try {
    const data = {
      ...editingOffer.value,
      ...offerForm.value
    }
    await offerApi.updateOffer(editingOffer.value.id, data)
    closeOfferModal()
    loadOffers()
  } catch (error) {
    console.error('Save offer failed:', error)
  }
}

const sendOffer = async (offer) => {
  try {
    await offerApi.updateOffer(offer.id, { ...offer, status: 'sent' })
    loadOffers()
  } catch (error) {
    console.error('Send offer failed:', error)
  }
}

const withdrawOffer = async (offer) => {
  try {
    await offerApi.updateOffer(offer.id, { ...offer, status: 'withdrawn' })
    loadOffers()
  } catch (error) {
    console.error('Withdraw offer failed:', error)
  }
}

onMounted(() => {
  loadOffers()
  loadJobs()
})
</script>

<style scoped>
.offer-list-page {
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-bar input {
  padding: 10px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  flex: 1;
  min-width: 200px;
}

.filter-bar .form-control {
  padding: 10px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  min-width: 150px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.table th,
.table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.table th {
  background-color: #fafafa;
  font-weight: 600;
  color: #666;
}

.table tr:hover {
  background-color: #f5f7fa;
}

.btn-sm {
  padding: 4px 12px;
  font-size: 12px;
  margin-right: 8px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
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

.detail-row {
  display: flex;
  margin-bottom: 12px;
}

.detail-row .label {
  width: 100px;
  color: #999;
  font-size: 14px;
}

.detail-row .value {
  flex: 1;
  font-size: 14px;
}

.reject-reason {
  color: #f56c6c;
}
</style>