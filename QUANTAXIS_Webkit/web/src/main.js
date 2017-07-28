// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import MuseUI from 'muse-ui'
import 'muse-ui/dist/muse-ui.css'
import 'muse-ui/dist/theme-carbon.css'
// import './carbon.css'
import echarts from 'echarts'

Vue.config.productionTip = false
Vue.use(MuseUI)
/* eslint-disable no-new */

router.beforeEach((to, from, next) => {
  if (to.matched.some(r => r.meta.requireAuth)) {
    if (sessionStorage.user) {
      console.log(sessionStorage.user)
      next();
    } else {
      next({
        path: '/sign',
        query: {
          redirect: to.fullPath
        }
      })
    }
  } else {
    next();
  }
})
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: {
    App
  }
})
