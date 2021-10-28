<template>
  <div id="courses">
    <h1>Courses</h1>
    <ul>
      <li v-for="course in courses" :key="course.id">
        {{course.title}}
      </li>
    </ul>
  </div>
</template>

<script>
import gql from 'graphql-tag'

export default {
  data: {
    courses: [],
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
}
</script>
