import 'regenerator-runtime/runtime'
import Vue from 'vue'
import router from './router'
import store from './store'
import {apolloProvider} from './apollo'
import App from './components/App.vue'

new Vue({
  router,
  store,
  apolloProvider,
  beforeCreate() {
    this.$store.dispatch('user')
  },
  render: h => h(App),
}).$mount('#app')
