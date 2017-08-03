import Vue from 'vue'
import Router from 'vue-router'
import Homepage from '@/components/HomePage'
import Personal from '@/components/Personal'
import Sign from '@/components/Sign'
import Start from '@/components/Start'


Vue.use(Router)

export default new Router({
  routes: [{
      path: '/',
      name: 'homePage',
      component: require('@/components/HomePage.vue')
    },
    {
      path: '/sign',
      name: 'signPage',
      component: require('@/components/Sign.vue')
    },
    {
      path: '/personal',
      name: 'personal',
      meta: {
        requireAuth: true, // 添加该字段，表示进入这个路由是需要登录的
      },
      component: require('@/components/Personal.vue'),
      children: [{
          'path': '/personal/index',
          component: require('@/components/Personal/index.vue')
        },
        {
          'path': '/personal/notebook',
          component: require('@/components/Personal/notebook.vue')
        },
        {
          'path': '/personal/markdown',
          component: require('@/components/Personal/markdown.vue')
        },
        {
          'path': '/personal/monitor',
          component: require('@/components/Personal/monitor.vue')
        },
        {
          'path': '/personal/history/:id',
          name: 'history',
          component: require('@/components/Personal/history.vue')
        },
        {
          'path': '/personal/shipane',
          component: require('@/components/Personal/shipane.vue')
        },
        {
          'path': '/personal/trade',
          component: require('@/components/Personal/trade.vue')
        },
        {
          'path': '/personal/backtest',
          component: require('@/components/Personal/backtest.vue')
        },
        {
          'path': '/personal/stocklist',
          component: require('@/components/Personal/stocklist.vue')
        },
        {
          'path': '/personal/capital',
          component: require('@/components/Personal/capital.vue')
        },
        {
          'path': '/personal/analysis',
          component: require('@/components/Personal/analysis.vue')
        },
        {
          'path': '/personal/api',
          component: require('@/components/Personal/api.vue')
        },
        {
          'path': '/personal/setting',
          component: require('@/components/Personal/setting.vue')
        },
        {
          'path': '/personal/visual/:id',
          name: 'visual',
          component: require('@/components/Personal/visual.vue')
        }
      ]
    },
    {
      path: '/start',
      name: 'startPage',
      component: require('@/components/Start.vue')
    }
  ]
})
