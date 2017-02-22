export default [
  {
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
      {'path': '/personal/axios',component: require('./components/Personal/axios.vue')}
    ]
  },
  {
    path: '/start',
    name: 'startPage',
    component: require('./components/Start.vue')
  },
  {
    path: '/lp',
    name: 'landing-page',
    component: require('./components/LandingPageView.vue')
  },
  {
    path: '*',
    redirect: '/'
  }
]
