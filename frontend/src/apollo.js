import Vue from 'vue'
import VueApollo from 'vue-apollo'
import { createApolloClient } from 'vue-cli-plugin-apollo/graphql-client'
import token from './csrf'
import environment from './environment'

Vue.use(VueApollo)

export default new VueApollo({
  defaultClient: createApolloClient({
    httpLinkOptions: {
      credentials: 'include',
      fetch(uri, options) {
        options.headers['X-CSRFTOKEN'] = token()
        return fetch(uri, options)
      },
    },
    httpEndpoint: environment.httpEndpoint,
  }).apolloClient,
  defaultOptions: {
    $query: {
      skip() {
        return !this.$store.state.csrf
      },
    },
  },
})
