import Vue from 'vue';
import VueApollo from 'vue-apollo';
import { ApolloClient } from 'apollo-client';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { from } from 'apollo-link';
import { setContext } from 'apollo-link-context';
import axios from 'axios';
import { createHttpLink } from 'apollo-link-http';
import environment from './environment';

Vue.use(VueApollo);

let token;

function refreshToken() {
  token = (async () => (await axios.get(environment.csrf, {
    withCredentials: true,
  })).data.token)();
}

refreshToken();

const apolloProvider = new VueApollo({
  defaultClient: new ApolloClient({
    cache: new InMemoryCache(),
    link: from([
      setContext(async () => ({
        headers: {
          'X-CSRFTOKEN': await token,
        },
      })),
      createHttpLink({
        uri: environment.graphql,
        credentials: 'include',
      }),
    ]),
  }),
});

export { refreshToken, apolloProvider };
