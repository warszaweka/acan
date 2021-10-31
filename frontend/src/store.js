import Vue from 'vue'
import Vuex from 'vuex'
import gql from 'graphql-tag'
import {apolloClient} from './apollo'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null,
  },
  mutations: {
    user(state, user) {
      state.user = user
    },
  },
  actions: {
    async user(context) {
      context.commit(
        'user',
        (await apolloClient.query({
          query: gql`
            query {
              user {
                username
              }
            }
          `,
        })).data.user
      )
    }
  }
})
