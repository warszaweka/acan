<template>
  <div>
    <b-card v-if="lesson">
      <b-card-title>
        <span>
          {{ lesson.order }}
        </span>
        <span>
          {{ lesson.title }}
        </span>
      </b-card-title>
      <b-card-text>
        {{ lesson.description }}
      </b-card-text>
    </b-card>
  </div>
</template>

<script>
import gql from 'graphql-tag';

export default {
  data() {
    return {
      lesson: null,
    };
  },
  props: [
    'id',
  ],
  apollo: {
    lesson: {
      query: gql`
        query($id: String!) {
          lesson(id: $id) {
            order
            title
            description
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
