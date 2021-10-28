import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    csrf: false,
  },
  mutations: {
    csrfon(state) {
      state.csrf = true
    },
  },
})
