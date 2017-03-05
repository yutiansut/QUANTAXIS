import Vue from 'vue'
import VueRouter from 'vue-router'
import store from "./store/"
Vue.use(VueRouter)
Vue.use(Vuex)

const routes = [ {
    path: '/',
    name: 'homePage',
    component: require('./components/HomePage.vue')
  },
   {
    path: '/todo',
    name: 'todoPage',
    component: require('./components/todo.vue')
  },
   {
    path: '/sign',
    name: 'signPage',
    component: require('./components/Sign.vue')
  },
   {
    path: '/personal',
    name: 'personal',
    meta: {
      requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
    },
    component: require('./components/Personal.vue'),
    children:[
      {'path': '/personal/index',component: require('./components/Personal/index.vue')},
      {'path': '/personal/notebook',component: require('./components/Personal/notebook.vue')},
      {'path': '/personal/axios',component: require('./components/Personal/axios.vue')},
      {'path': '/personal/visual',component: require('./components/Personal/visual.vue')}
    ]
  },
  {
    path: '/start',
    name: 'startPage',
    component: require('./components/Start.vue')
  },
  {
    path: '*',
    redirect: '/'
  }];



const router = new VueRouter({
    routes
});

router.beforeEach(({meta, path}, from, next) => {
    var { auth = true } = meta
    var isLogin = Boolean(store.state.user.name) //true用户已登录， false用户未登录

    if (auth && !isLogin && path !== '/sign') {
        return next({ path: '/sign' })
    }
    next()
})

export default router;