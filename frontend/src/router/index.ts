import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Chat from '@/views/Chat.vue'
import KnowledgeBase from '@/views/KnowledgeBase.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/chat'
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

  // 已登录用户访问登录/注册页，重定向到聊天页
  if ((to.path === '/login' || to.path === '/register') && userStore.token) {
    next('/chat')
    return
  }

  next()
})

export default router
