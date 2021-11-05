<template>
  <div>
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
        }
      }
    `,
  },
};
</script>
