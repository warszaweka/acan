import Vue from 'vue'
import VueApollo from 'vue-apollo'
import {createApolloClient} from 'vue-cli-plugin-apollo/graphql-client'
import {from} from 'apollo-link'
import {RetryLink} from "apollo-link-retry"
import {onError} from 'apollo-link-error'
import {setContext} from '@apollo/client/link/context';
import {from as rfrom} from 'rxjs';
import {token, refresh_token} from './csrf'
import environment from './environment'

Vue.use(VueApollo)

let apolloClient = createApolloClient({
  httpLinkOptions: {
    credentials: 'include',
  },
  httpEndpoint: environment.graphql,
  link: from([
    new RetryLink(),
    new onError(function(obj) {
      return rfrom((async function() {
        await refresh_token()
        throw obj.networkError
      })())
    }),
    setContext(function(request, previousContext) {
      previousContext.headers['X-CSRFTOKEN'] = token
      return previousContext
    })
  ])
}).apolloClient

let apolloProvider = new VueApollo({
  defaultClient: apolloClient,
})

export {apolloClient, apolloProvider}
