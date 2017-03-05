export default [
  {
    path: '/',
    name: 'homePage',
    component: require('components/HomePage')
  },
   {
    path: '/todo',
    name: 'todoPage',
    component: require('components/todo')
  },
   {
    path: '/sign',
    name: 'signPage',
    component: require('components/Sign')
  },
   {
    path: '/personal',
    name: 'personal',
    meta: {
      requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
    },
    component: require('components/Personal'),
    children:[
      {'path': '/personal/index',component: require('components/Personal/index')},
      {'path': '/personal/notebook',component: require('components/Personal/notebook')},
      {'path': '/personal/axios',component: require('components/Personal/axios')},
      {'path': '/personal/visual',component: require('components/Personal/visual')}
    ]
  },
  {
    path: '/start',
    name: 'startPage',
    component: require('components/Start')
  },
  {
    path: '*',
    redirect: '/'
  }
]
