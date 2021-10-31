<template>
  <div>
    <h1>
      Course
    </h1>
    <div v-if="course">
      <h2>
        {{course.title}} {{course.purchased ? "purchased" : ""}}
      </h2>
      <p>
        {{course.description}}
      </p>
      <ul>
        <li v-for="lesson in course.lessonSet" :key="lesson.order">
          <router-link :to="`/lesson/${lesson.id}`">
            {{lesson.order}} {{lesson.title}}
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag'

export default {
  data() {
    return {
      course: null,
    }
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
        }
      }
    },
  },
}
</script>
