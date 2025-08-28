export interface User {
  id: string
  email: string
  first_name?: string
  last_name?: string
  role: 'admin' | 'b2b' | 'b2c'
  company_name?: string
  phone_number?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  first_name?: string
  last_name?: string
  role: 'b2b' | 'b2c'
  company_name?: string
  phone_number?: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export const useAuth = () => {
  // État réactif
  const user = useState<User | null>('user', () => null)
  const token = useState<string | null>('token', () => null)
  const isAuthenticated = computed(() => !!token.value && !!user.value)

  // Configuration de l'API
  const config = useRuntimeConfig()
  const apiBaseUrl = config.public.apiBaseUrl

  // Fonction de connexion
  const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
    try {
      const response = await $fetch<AuthResponse>(`${apiBaseUrl}/v1/auth/login`, {
        method: 'POST',
        body: credentials
      })

      // Stocker le token et les informations utilisateur
      token.value = response.access_token
      user.value = response.user

      // Sauvegarder dans le localStorage
      if (process.client) {
        localStorage.setItem('auth_token', response.access_token)
        localStorage.setItem('user_data', JSON.stringify(response.user))
      }

      return response
    } catch (error) {
      console.error('Erreur de connexion:', error)
      throw error
    }
  }

  // Fonction d'inscription
  const register = async (userData: RegisterData): Promise<AuthResponse> => {
    try {
      const response = await $fetch<AuthResponse>(`${apiBaseUrl}/v1/auth/register`, {
        method: 'POST',
        body: userData
      })

      // Stocker le token et les informations utilisateur
      token.value = response.access_token
      user.value = response.user

      // Sauvegarder dans le localStorage
      if (process.client) {
        localStorage.setItem('auth_token', response.access_token)
        localStorage.setItem('user_data', JSON.stringify(response.user))
      }

      return response
    } catch (error) {
      console.error('Erreur d\'inscription:', error)
      throw error
    }
  }

  // Fonction de déconnexion
  const logout = async (): Promise<void> => {
    try {
      // Appel API pour invalider le token (optionnel)
      if (token.value) {
        await $fetch(`${apiBaseUrl}/v1/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token.value}`
          }
        })
      }
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error)
    } finally {
      // Nettoyer l'état local
      token.value = null
      user.value = null

      // Nettoyer le localStorage
      if (process.client) {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('user_data')
      }
    }
  }

  // Fonction pour récupérer le profil utilisateur
  const fetchProfile = async (): Promise<User> => {
    if (!token.value) {
      throw new Error('Token d\'authentification manquant')
    }

    try {
      const response = await $fetch<User>(`${apiBaseUrl}/v1/users/me`, {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })

      user.value = response
      return response
    } catch (error) {
      console.error('Erreur lors de la récupération du profil:', error)
      throw error
    }
  }

  // Fonction pour mettre à jour le profil
  const updateProfile = async (profileData: Partial<User>): Promise<User> => {
    if (!token.value) {
      throw new Error('Token d\'authentification manquant')
    }

    try {
      const response = await $fetch<User>(`${apiBaseUrl}/v1/users/me`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token.value}`
        },
        body: profileData
      })

      user.value = response

      // Mettre à jour le localStorage
      if (process.client) {
        localStorage.setItem('user_data', JSON.stringify(response))
      }

      return response
    } catch (error) {
      console.error('Erreur lors de la mise à jour du profil:', error)
      throw error
    }
  }

  // Fonction pour changer le mot de passe
  const changePassword = async (currentPassword: string, newPassword: string): Promise<void> => {
    if (!token.value) {
      throw new Error('Token d\'authentification manquant')
    }

    try {
      await $fetch(`${apiBaseUrl}/v1/users/change-password`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token.value}`
        },
        body: {
          current_password: currentPassword,
          new_password: newPassword
        }
      })
    } catch (error) {
      console.error('Erreur lors du changement de mot de passe:', error)
      throw error
    }
  }

  // Fonction pour récupérer l'état d'authentification depuis le localStorage
  const restoreAuth = (): void => {
    if (process.client && !token.value) {
      const storedToken = localStorage.getItem('auth_token')
      const storedUser = localStorage.getItem('user_data')

      if (storedToken && storedUser) {
        try {
          token.value = storedToken
          user.value = JSON.parse(storedUser)
        } catch (error) {
          console.error('Erreur lors de la restauration de l\'authentification:', error)
          // Nettoyer les données corrompues
          localStorage.removeItem('auth_token')
          localStorage.removeItem('user_data')
        }
      }
    }
  }

  // Fonction pour vérifier si le token est valide
  const isTokenValid = (): boolean => {
    if (!token.value) return false

    try {
      // Décoder le JWT pour vérifier l'expiration
      const payload = JSON.parse(atob(token.value.split('.')[1]))
      const currentTime = Math.floor(Date.now() / 1000)
      
      return payload.exp > currentTime
    } catch (error) {
      console.error('Erreur lors de la vérification du token:', error)
      return false
    }
  }

  // Fonction pour rafraîchir le token (si l'API le supporte)
  const refreshToken = async (): Promise<boolean> => {
    try {
      const response = await $fetch<{ access_token: string }>(`${apiBaseUrl}/v1/auth/refresh`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })

      token.value = response.access_token

      if (process.client) {
        localStorage.setItem('auth_token', response.access_token)
      }

      return true
    } catch (error) {
      console.error('Erreur lors du rafraîchissement du token:', error)
      return false
    }
  }

  // Initialiser l'authentification au chargement de l'application
  onMounted(() => {
    restoreAuth()
  })

  // Vérifier la validité du token périodiquement
  let tokenCheckInterval: NodeJS.Timeout | null = null

  onMounted(() => {
    if (process.client) {
      tokenCheckInterval = setInterval(() => {
        if (token.value && !isTokenValid()) {
          console.log('Token expiré, déconnexion automatique')
          logout()
        }
      }, 60000) // Vérifier toutes les minutes
    }
  })

  onUnmounted(() => {
    if (tokenCheckInterval) {
      clearInterval(tokenCheckInterval)
    }
  })

  return {
    // État
    user: readonly(user),
    token: readonly(token),
    isAuthenticated,

    // Actions
    login,
    register,
    logout,
    fetchProfile,
    updateProfile,
    changePassword,
    restoreAuth,
    isTokenValid,
    refreshToken
  }
}
