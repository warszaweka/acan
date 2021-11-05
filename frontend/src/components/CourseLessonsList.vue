<template>
  <div>
    <b-nav v-if="course" vertical>
      <b-nav-item v-for="lesson in course.lessonSet" :key="lesson.order"
                  :to="{ name: 'lesson', params: { course_id: id, lesson_id: lesson.id } }"
                  active-class="active">
        <span>
          {{ lesson.order }}
        </span>
        <span>
          {{ lesson.title }}
        </span>
      </b-nav-item>
    </b-nav>
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
            lessonSet {
              id
              order
              title
            }
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
