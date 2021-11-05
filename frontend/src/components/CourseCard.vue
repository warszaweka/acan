<template>
  <div>
    <b-card v-if="course">
      <b-card-title>
        {{ course.title }}
      </b-card-title>
      <b-card-sub-title v-if="course.purchased">
        Purchased
      </b-card-sub-title>
      <b-card-text>
        {{ course.description }}
      </b-card-text>
    </b-card>
  </div>
</template>

<script>
import gql from 'graphql-tag';

export default {
  data() {
    return {
      course: null,
    };
  },
  props: [
    'id',
  ],
  apollo: {
    course: {
      query: gql`
        query($id: String!) {
          course(id: $id) {
            id
            title
            description
            purchased
          }
        }
      `,
      variables() {
        return {
          id: this.id,
        };
      },
    },
  },
};
</script>
