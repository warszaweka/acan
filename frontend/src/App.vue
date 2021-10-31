<template>
  <div>
    <ul>
      <li>
        <router-link :to="{ name: 'home' }">
          Home
        </router-link>
      </li>
      <li>
        <router-link :to="{ name: 'courses' }">
          Courses
        </router-link>
      </li>
      <li v-if="user">
        <router-link :to="{ name: 'user' }">
          {{ user.username }}
        </router-link>
      </li>
      <li v-else>
        <router-link :to="{ name: 'login' }">
          Login
        </router-link>
      </li>
    </ul>
    <router-view/>
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
