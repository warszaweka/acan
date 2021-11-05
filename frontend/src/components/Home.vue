<template>
  <b-container
    class="flex-fill"
    >
    <b-row>
      <b-col>
        <b-card-group
          deck
          >
          <b-link
            v-for="course in courses"
            :key="course.id"
            :to="{ name: 'course', params: { course_id: course.id } }"
            >
            <b-card>
              <b-card-title>
                <span>
                  {{ course.title }}
                </span>
                <b-badge
                  v-if="course.purchased"
                  >
                  {{ purchased_label }}
                </b-badge>
              </b-card-title>
              <b-card-text>
                {{ course.shortDescription }}
              </b-card-text>
            </b-card>
          </b-link>
        </b-card-group>
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
      language: 'uk',
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
          shortDescription
          purchased
        }
      }
    `,
    language: gql`
      query {
        language
      }
    `,
  },
};
</script>
