import Vue from 'vue'
import VueRouter from 'vue-router'
import store from './vuex/store.js'
import * as types from './vuex/types.js'
Vue.use(VueRouter)


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



// 页面刷新时，重新赋值token
if (window.localStorage.getItem('token')) {
    store.commit(types.LOGIN, window.localStorage.getItem('token'))
}

const router = new VueRouter({
    routes
});

router.beforeEach((to, from, next) => {
    if (to.matched.some(r => r.meta.requireAuth)) {
        if (store.state.token) {
            next();
        }
        else {
            next({
                path: '/sign',
                query: {redirect: to.fullPath}
            })
        }
    }
    else {
        next();
    }
})

export default router;