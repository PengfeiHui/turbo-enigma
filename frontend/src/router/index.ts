import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Chat from '@/views/Chat.vue'
import KnowledgeBase from '@/views/KnowledgeBase.vue'
import Dashboard from '@/views/Dashboard.vue'
import Settings from '@/views/Settings.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      meta: { requiresAuth: false }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/chat',
      name: 'Chat',
      component: Chat,
      meta: { requiresAuth: true }
    },
    {
      path: '/kb-manage',
      name: 'KnowledgeBase',
      component: KnowledgeBase,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/settings',
      name: 'Settings',
      component: Settings,
      meta: { requiresAuth: true }
    },
    {
      path: '/history',
      redirect: '/chat'
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // 需要认证的页面
  if (to.meta.requiresAuth && !userStore.token) {
    next('/login')
    return
  }

  // 需要管理员权限的页面
  if (to.meta.requiresAdmin && !userStore.isAdmin()) {
    next('/chat')
    return
  }

  // 已登录用户访问登录/注册页，重定向到仪表盘
  if ((to.path === '/login' || to.path === '/register') && userStore.token) {
    next('/dashboard')
    return
  }

  next()
})

export default router
