import 'regenerator-runtime/runtime'
import Vue from 'vue'
import router from './router'
import apolloProvider from './apollo'
import store from './store'
import './csrf'
import App from './components/App.vue'

new Vue({
  router,
  store,
  apolloProvider,
  render: h => h(App),
}).$mount('#app')
