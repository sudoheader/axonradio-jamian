import Vue from 'vue'
import Router from 'vue-router'
import WebPlayer from '@/components/WebPlayer'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'WebPlayer',
      component: WebPlayer
    }
  ]
})
