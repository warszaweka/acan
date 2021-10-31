<template>
  <div>
    <h1>
      Lesson
    </h1>
    <div v-if="lesson">
      <h2>
        {{lesson.order}} {{lesson.title}}
      </h2>
      <p>
        {{lesson.description}}
      </p>
      <div v-if="lesson.course.purchased">
        <video-player :relative-path="lesson.video"/>
        <div>
          {{lesson.file}}
        </div>
      </div>
      <router-link :to="`/course/${lesson.course.id}`">
        {{lesson.course.title}} {{lesson.course.purchased ? "purchased" : ""}}
      </router-link>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag'
import VideoPlayer from './VideoPlayer.vue'

export default {
  data() {
    return {
      lesson: null,
    }
  },
  components: {
    VideoPlayer,
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
            file
          }
        }
      `,
      variables() {
        return {
          id: this.$route.params.id,
        }
      },
    },
  },
}
</script>
