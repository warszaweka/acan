import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from './components/Home.vue';
import Courses from './components/Courses.vue';
import Login from './components/Login.vue';
import Signup from './components/Signup.vue';
import EmailVerify from './components/EmailVerify.vue';
import RequestPasswordReset from './components/RequestPasswordReset.vue';
import PasswordReset from './components/PasswordReset.vue';
import User from './components/User.vue';
import SetPassword from './components/SetPassword.vue';
import Purchase from './components/Purchase.vue';
import PublicOffer from './components/PublicOffer.vue';
import PrivacyPolicy from './components/PrivacyPolicy.vue';

Vue.use(VueRouter);

export default new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Home,
      name: 'home',
    },
    {
      path: '/courses',
      component: Courses,
      name: 'courses',
    },
    {
      path: '/course/:id',
      component: Courses,
      name: 'course',
    },
    {
      path: '/lesson/:id',
      component: Courses,
      name: 'lesson',
    },
    {
      path: '/login',
      component: Login,
      name: 'login',
    },
    {
      path: '/signup',
      component: Signup,
      name: 'signup',
    },
    {
      path: '/email_verify/:uidb64/:token',
      component: EmailVerify,
      name: 'email_verify',
    },
    {
      path: '/request_password_reset',
      component: RequestPasswordReset,
      name: 'request_password_reset',
    },
    {
      path: '/password_reset/:uidb64/:token',
      component: PasswordReset,
      name: 'password_reset',
    },
    {
      path: '/user',
      component: User,
      name: 'user',
    },
    {
      path: '/set_password',
      component: SetPassword,
      name: 'set_password',
    },
    {
      path: '/purchase/:id',
      component: Purchase,
      name: 'purchase',
    },
    {
      path: '/public_offer',
      component: PublicOffer,
      name: 'public_offer',
    },
    {
      path: '/privacy_policy',
      component: PrivacyPolicy,
      name: 'privacy_policy',
    },
  ],
  linkActiveClass: 'active',
});
