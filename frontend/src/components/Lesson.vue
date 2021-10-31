<template>
  <div>
    <div v-if="lesson">
      <div>
        <span>
          {{ lesson.order }}
        </span>
        <span>
          {{ lesson.title }}
        </span>
      </div>
      <div>
        {{ lesson.description }}
      </div>
      <div v-if="lesson.course.purchased">
        <div>
          {{ lesson.video }}
        </div>
        <div v-if="lesson.addon">
          {{ lesson.addon }}
        </div>
      </div>
      <router-link :to="{ name: 'course', params: { id: lesson.course.id } }">
        <span>
          {{ lesson.course.title }}
        </span>
        <span v-if="lesson.course.purchased">
          purchased
        </span>
      </router-link>
    </div>
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
  apollo: {
    lesson: {
      query: gql`
        query($id: String!) {
          lesson(id: $id) {
            course {
              id
              title
              purchased
            }
            order
            title
            description
            video
            addon
          }
        }
      `,
      variables() {
        return {
          id: this.$route.params.id,
        };
      },
    },
  },
};
</script>
