<template>
  <div>
    <h1>
      Courses
    </h1>
    <ul>
      <li v-for="course in courses" :key="course.id">
        <router-link :to="`/course/${course.id}`">
          {{course.title}} {{course.purchased ? "purchased" : ""}}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import gql from 'graphql-tag'

export default {
  data() {
    return {
      courses: [],
    }
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
}
</script>
