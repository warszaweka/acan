<template>
  <b-form @submit.prevent="login">
    <b-form-group label="Username" label-for="username">
      <b-form-input id="username" v-model="username" type="text" required/>
    </b-form-group>
    <b-form-group label="Password" label-for="password">
      <b-form-input id="password" v-model="password" type="password" required/>
    </b-form-group>
    <b-button type="submit">
      Login
    </b-button>
    </b-form>
</template>

<script>
import gql from 'graphql-tag';

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
        this.$router.push({
          name: 'home',
        });
      }
    },
  },
};
</script>
