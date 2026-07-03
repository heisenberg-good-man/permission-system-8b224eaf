import { reactive } from 'vue'

const state = reactive({
  currentUser: null,
  token: null
})

export function useUserStore() {
  const login = (user, token) => {
    state.currentUser = user
    state.token = token
    localStorage.setItem('user', JSON.stringify(user))
    localStorage.setItem('token', token)
  }

  const logout = () => {
    state.currentUser = null
    state.token = null
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }

  const init = () => {
    const storedUser = localStorage.getItem('user')
    const storedToken = localStorage.getItem('token')
    if (storedUser && storedToken) {
      state.currentUser = JSON.parse(storedUser)
      state.token = storedToken
    }
  }

  return {
    state,
    login,
    logout,
    init
  }
}