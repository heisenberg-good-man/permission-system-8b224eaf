<template>
  <div class="job-form">
    <div class="form-header">
      <h2>{{ isEdit ? '编辑职位' : '发布职位' }}</h2>
      <button class="btn btn-outline" @click="$router.back()">取消</button>
    </div>

    <div class="card">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>职位名称 *</label>
          <input v-model="form.title" type="text" placeholder="请输入职位名称" required />
        </div>
        
        <div class="form-group">
          <label>公司名称 *</label>
          <input v-model="form.company" type="text" placeholder="请输入公司名称" required />
        </div>
        
        <div class="row">
          <div class="form-group col">
            <label>工作地点 *</label>
            <input v-model="form.location" type="text" placeholder="请输入工作地点" required />
          </div>
          <div class="form-group col">
            <label>薪资范围 *</label>
            <input v-model="form.salary" type="text" placeholder="例如：20k-40k" required />
          </div>
        </div>
        
        <div class="row">
          <div class="form-group col">
            <label>经验要求 *</label>
            <select v-model="form.experience" required>
              <option value="">请选择</option>
              <option value="应届生">应届生</option>
              <option value="1-3年">1-3年</option>
              <option value="3-5年">3-5年</option>
              <option value="5-10年">5-10年</option>
              <option value="10年以上">10年以上</option>
            </select>
          </div>
          <div class="form-group col">
            <label>学历要求 *</label>
            <select v-model="form.education" required>
              <option value="">请选择</option>
              <option value="高中">高中</option>
              <option value="大专">大专</option>
              <option value="本科">本科</option>
              <option value="硕士">硕士</option>
              <option value="博士">博士</option>
            </select>
          </div>
        </div>
        
        <div class="form-group">
          <label>职位描述 *</label>
          <textarea v-model="form.description" placeholder="请输入职位描述" required></textarea>
        </div>
        
        <div class="form-actions">
          <button type="button" class="btn btn-outline" @click="$router.back()">取消</button>
          <button type="submit" class="btn btn-primary">{{ isEdit ? '保存修改' : '发布职位' }}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { jobApi } from '../../api'

const emit = defineEmits(['update-stats'])

const route = useRoute()
const router = useRouter()
const { state } = useUserStore()

const isEdit = computed(() => !!route.params.id)
const form = ref({
  title: '',
  company: '',
  location: '',
  salary: '',
  experience: '',
  education: '',
  description: '',
  recruiter_id: state.currentUser?.id || 1
})

const handleSubmit = async () => {
  try {
    if (isEdit.value) {
      await jobApi.updateJob(route.params.id, form.value)
    } else {
      await jobApi.createJob(form.value)
    }
    emit('update-stats')
    router.push('/recruiter')
  } catch (error) {
    console.error('Submit failed:', error)
    alert('提交失败，请重试')
  }
}

onMounted(async () => {
  if (isEdit.value) {
    try {
      const response = await jobApi.getJob(route.params.id)
      form.value = { ...response.data, recruiter_id: state.currentUser?.id || 1 }
    } catch (error) {
      console.error('Failed to load job:', error)
    }
  }
})
</script>

<style scoped>
.job-form {
  max-width: 800px;
  margin: 0 auto;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.form-header h2 {
  margin: 0;
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