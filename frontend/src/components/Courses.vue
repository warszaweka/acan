<template>
  <b-container
    class="flex-fill"
    >
    <b-row no-gutters>
      <b-col>
        <b-list-group
          flush
          >
          <b-list-group-item
            v-for="course in courses"
            :key="course.id"
            :to="{ name: 'course', params: { course_id: course.id } }"
            >
            <span>
              {{ course.title }}
            </span>
            <b-badge
              v-if="course.purchased"
              >
              {{ purchased_label }}
            </b-badge>
          </b-list-group-item>
        </b-list-group>
      </b-col>
      <b-col>
        <router-view>
        </router-view>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import gql from 'graphql-tag';

export default {
  data() {
    return {
      courses: [],
    };
  },
  computed: {
    purchased_label() {
      return this.language === 'ru' ? 'Куплено' : 'Куплено';
    },
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
};
</script>
