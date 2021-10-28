import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './components/Home.vue'
import Courses from './components/Courses.vue'
import NotFound from './components/NotFound.vue'

Vue.use(VueRouter)

export default new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/courses',
      name: 'Courses',
      component: Courses,
    },
    { 
      path: '*', 
      name: 'NotFound',
      component: NotFound,
    },
  ],
})
