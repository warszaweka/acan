import Vue from 'vue';
import router from './router';
import { apolloProvider } from './apollo';
import App from './components/App.vue';

new Vue({
  router,
  apolloProvider,
  render(h) {
    return h(App);
  },
}).$mount('#app');
