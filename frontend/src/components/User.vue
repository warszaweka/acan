<template>
  <div>
    <div v-if="user">
      <div>
        {{ user.username }}
      </div>
      <button v-on:click="logout">
        Logout
      </button>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag';

export default {
  data() {
    return {
      user: null,
    };
  },
  methods: {
    async logout() {
      await this.$apollo.mutate({
        mutation: gql`
          mutation {
            logout {
              username
            }
          }
        `,
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
              user: result.data.logout,
            },
          });
        },
      });
      this.$router.push({
        name: 'home',
      });
    },
  },
  apollo: {
    user: gql`
      query {
        user {
          username
        }
      }
    `,
  },
};
</script>
