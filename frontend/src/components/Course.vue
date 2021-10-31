<template>
  <div>
    <div v-if="course">
      <div>
        {{ course.title }}
      </div>
      <div v-if="course.purchased">
        purchased
      </div>
      <div>
        {{ course.description }}
      </div>
      <ul>
        <li v-for="lesson in course.lessonSet" :key="lesson.order">
          <router-link :to="{ name: 'lesson', params: { id: lesson.id } }">
            <span>
              {{ lesson.order }}
            </span>
            <span>
              {{ lesson.title }}
            </span>
          </router-link>
        </li>
      </ul>
    </div>
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
  apollo: {
    course: {
      query: gql`
        query($id: String!) {
          course(id: $id) {
            title
            description
            lessonSet {
              id
              order
              title
            }
            purchased
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
