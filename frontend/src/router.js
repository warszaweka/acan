import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from './components/Home.vue';
import Courses from './components/Courses.vue';
import Course from './components/Course.vue';
import Lesson from './components/Lesson.vue';
import User from './components/User.vue';
import Login from './components/Login.vue';
import NotFound from './components/NotFound.vue';
import { setPrev } from './login';

Vue.use(VueRouter);

export default new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/courses',
      name: 'courses',
      component: Courses,
    },
    {
      path: '/course/:id',
      name: 'course',
      component: Course,
    },
    {
      path: '/lesson/:id',
      name: 'lesson',
      component: Lesson,
    },
    {
      path: '/user',
      name: 'user',
      component: User,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      beforeEnter(to, from, next) {
        setPrev(from);
        next();
      },
    },
    {
      path: '*',
      name: 'not_found',
      component: NotFound,
    },
  ],
});
