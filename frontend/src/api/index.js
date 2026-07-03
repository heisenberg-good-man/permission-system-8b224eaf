import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export const userApi = {
  login(email, password) {
    return api.post('/users/login', { email, password })
  },
  getUsers(role) {
    return api.get('/users', { params: { role } })
  },
  getUser(id) {
    return api.get(`/users/${id}`)
  }
}

export const jobApi = {
  getJobs(params) {
    return api.get('/jobs', { params })
  },
  getJob(id) {
    return api.get(`/jobs/${id}`)
  },
  createJob(data) {
    return api.post('/jobs', data)
  },
  updateJob(id, data) {
    return api.put(`/jobs/${id}`, data)
  },
  deleteJob(id) {
    return api.delete(`/jobs/${id}`)
  }
}

export const resumeApi = {
  getResumes(params) {
    return api.get('/resumes', { params })
  },
  getResume(id) {
    return api.get(`/resumes/${id}`)
  },
  createResume(data) {
    return api.post('/resumes', data)
  },
  updateResume(id, data) {
    return api.put(`/resumes/${id}`, data)
  }
}

export const messageApi = {
  getMessages(resumeId) {
    return api.get('/messages', { params: { resume_id: resumeId } })
  },
  createMessage(data) {
    return api.post('/messages', data)
  }
}

export const interviewApi = {
  getInterviews(params) {
    return api.get('/interviews', { params })
  },
  getInterview(id) {
    return api.get(`/interviews/${id}`)
  },
  createInterview(data) {
    return api.post('/interviews', data)
  },
  updateInterview(id, data) {
    return api.put(`/interviews/${id}`, data)
  }
}

export const statsApi = {
  getStats(userId) {
    return api.get(`/stats/${userId}`)
  }
}

export default api