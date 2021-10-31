<template>
  <div>
    <label for="username">
      Username
    </label>
    <input v-model="username" id="username"/>
    <label for="password">
      Password
    </label>
    <input type="password" v-model="password" id="password"/>
    <button v-on:click="login">
      Login
    </button>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import { getPrev, setPrev } from '../login';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {
      if ((await this.$apollo.mutate({
        mutation: gql`
          mutation ($username: String!, $password: String!) {
            login(username: $username, password: $password) {
              username
            }
          }
        `,
        variables: {
          username: this.username,
          password: this.password,
        },
        update: (store, result) => {
          store.writeQuery({
            query: gql`
              query {
                user {
                  username
                }
              }
            `,
            data: {
              user: result.data.login,
            },
          });
        },
      })).data.login) {
        const prev = getPrev();
        if (prev) {
          setPrev(null);
          this.$router.push(prev);
        } else {
          this.$router.push({
            name: 'home',
          });
        }
      }
    },
  },
};
</script>
