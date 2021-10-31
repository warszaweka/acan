import Vue from 'vue';
import VueApollo from 'vue-apollo';
import { ApolloClient } from 'apollo-client';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { from } from 'apollo-link';
import { RetryLink } from 'apollo-link-retry';
import { onError } from 'apollo-link-error';
import { createHttpLink } from 'apollo-link-http';
import { setContext } from '@apollo/client/link/context';
import { from as rfrom } from 'rxjs';
import { getToken, refreshToken } from './csrf';
import environment from './environment';

Vue.use(VueApollo);

const apolloClient = new ApolloClient({
  cache: new InMemoryCache(),
  link: from([
    new RetryLink(),
    onError(((obj) => rfrom((async function asyncRefreshToken() {
      await refreshToken();
      throw obj.networkError;
    })()))),
    setContext((request, previousContext) => {
      const context = previousContext;
      if (!Object.prototype.hasOwnProperty.call(context, 'headers')) {
        context.headers = {};
      }
      context.headers['X-CSRFTOKEN'] = getToken();
      return context;
    }),
    createHttpLink({
      uri: environment.graphql,
      credentials: 'include',
    }),
  ]),
});

const apolloProvider = new VueApollo({
  defaultClient: apolloClient,
});

export { apolloClient, apolloProvider };
