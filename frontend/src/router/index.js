import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/recruiter',
    name: 'RecruiterDashboard',
    component: () => import('../views/recruiter/Dashboard.vue'),
    children: [
      {
        path: '',
        name: 'RecruiterJobs',
        component: () => import('../views/recruiter/JobList.vue')
      },
      {
        path: 'job/create',
        name: 'RecruiterCreateJob',
        component: () => import('../views/recruiter/JobForm.vue')
      },
      {
        path: 'job/:id/edit',
        name: 'RecruiterEditJob',
        component: () => import('../views/recruiter/JobForm.vue')
      },
      {
        path: 'job/:id/resumes',
        name: 'RecruiterJobResumes',
        component: () => import('../views/recruiter/ResumeList.vue')
      },
      {
        path: 'resume/:id',
        name: 'RecruiterResumeDetail',
        component: () => import('../views/recruiter/ResumeDetail.vue')
      },
      {
        path: 'applications',
        name: 'RecruiterApplications',
        component: () => import('../views/recruiter/ApplicationList.vue')
      }
    ]
  },
  {
    path: '/candidate',
    name: 'CandidateDashboard',
    component: () => import('../views/candidate/Dashboard.vue'),
    children: [
      {
        path: '',
        name: 'CandidateJobs',
        component: () => import('../views/candidate/JobList.vue')
      },
      {
        path: 'job/:id',
        name: 'CandidateJobDetail',
        component: () => import('../views/candidate/JobDetail.vue')
      },
      {
        path: 'applications',
        name: 'CandidateApplications',
        component: () => import('../views/candidate/ApplicationList.vue')
      },
      {
        path: 'application/:id',
        name: 'CandidateApplicationDetail',
        component: () => import('../views/candidate/ApplicationDetail.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router