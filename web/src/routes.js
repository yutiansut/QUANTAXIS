import Vue from 'vue'
import VueRouter from 'vue-router'
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


export default router;