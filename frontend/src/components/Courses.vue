<template>
  <div>
    <ul>
      <li v-for="course in courses" :key="course.id">
        <router-link :to="{ name: 'course', params: { id: course.id } }">
          <span>
            {{ course.title }}
          </span>
          <span v-if="course.purchased">
            purchased
          </span>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import gql from 'graphql-tag';

export default {
  data() {
    return {
      courses: [],
    };
  },
  apollo: {
    courses: gql`
      query {
        courses {
          id
          title
          purchased
        }
      }
    `,
  },
};
</script>
