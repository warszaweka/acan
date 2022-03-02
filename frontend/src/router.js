import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from './components/Home.vue';
import Widget from './components/Widget.vue';
import Login from './components/Login.vue';
import Signup from './components/Signup.vue';
import EmailVerify from './components/EmailVerify.vue';
import RequestPasswordReset from './components/RequestPasswordReset.vue';
import PasswordReset from './components/PasswordReset.vue';
import User from './components/User.vue';
import SetPassword from './components/SetPassword.vue';
import SetMailingList from './components/SetMailingList.vue';
import Payment from './components/Payment.vue';
import PublicOffer from './components/PublicOffer.vue';
import PrivacyPolicy from './components/PrivacyPolicy.vue';
import Service from './components/Service.vue';

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
      component: Widget,
      name: 'courses',
    },
    {
      path: '/course/:id',
      component: Widget,
      name: 'course',
    },
    {
      path: '/lesson/:id',
      component: Widget,
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
      path: '/set_mailing_list',
      component: SetMailingList,
      name: 'set_mailing_list',
    },
    {
      path: '/payment/:id/:data/:signature',
      component: Payment,
      name: 'payment',
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
    {
      path: '/service',
      component: Service,
      name: 'service',
    },
  ],
  linkActiveClass: 'active',
});
