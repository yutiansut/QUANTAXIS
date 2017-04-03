import Vue from 'vue'
import Electron from 'vue-electron'
import Resource from 'vue-resource'
import Router from 'vue-router'
import axios from 'axios';
import App from './App'
import routes from './routes'
import MuseUI from 'muse-ui'
import 'muse-ui/dist/muse-ui.css'
import './theme-carbon.css'
import echarts from 'echarts'


Vue.use(Electron)
Vue.use(Resource)
Vue.use(Router)
Vue.config.debug = true
Vue.use(MuseUI)


const router = new Router({
  scrollBehavior: () => ({ y: 0 }),
  routes
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(r => r.meta.requireAuth)) {
        if (sessionStorage.user) {
          console.log(sessionStorage.user)
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

/* eslint-disable no-new */
new Vue({
  router,
  ...App
}).$mount('#app')
