import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './components/Home.vue'
import Courses from './components/Courses.vue'
import Course from './components/Course.vue'
import Lesson from './components/Lesson.vue'
import User from './components/User.vue'
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
      path: '/course/:id',
      name: 'Course',
      component: Course,
    },
    {
      path: '/lesson/:id',
      name: 'Lesson',
      component: Lesson,
    },
    {
      path: '/user',
      name: 'User',
      component: User,
    },
    { 
      path: '*', 
      name: 'NotFound',
      component: NotFound,
    },
  ],
})
