<template>
  <b-container
    fluid
    class="py-3"
    >
    <b-row
      no-gutters
      >
      <b-col
        md="5"
        xl="3"
        >
        <b-list-group
          flush
          >
          <b-list-group-item
            v-for="course in courses"
            :key="course.id"
            :to="course.soon ? null : { name: 'course', params: { id: course.id } }"
            :active="$route.name === 'course' && $data.course && $data.course.id === course.id
            || $route.name === 'lesson' && $data.lesson && $data.lesson.course.id === course.id"
            >
            <span>
              {{ course.title }}
            </span>
            <b-badge
              v-if="course.purchased"
              >
              {{ purchased_badge }}
            </b-badge>
            <b-badge
              v-if="course.soon"
              >
              {{ soon_badge }}
            </b-badge>
          </b-list-group-item>
        </b-list-group>
      </b-col>
      <b-col
        v-if="($route.name === 'course' || $route.name === 'lesson') && course"
        md="7"
        xl="4"
        class="py-5"
        >
        <h2
          class="text-center mb-5"
          >
          {{ course.title }}
        </h2>
        <div
          class="mb-5"
          >
          {{ course.description }}
        </div>
        <div
          v-if="!course.purchased"
          class="mb-5"
          >
          <course-purchase-button
            :id="course.id"
            >
          </course-purchase-button>
        </div>
        <b-list-group
          flush
          >
          <b-list-group-item
            v-for="lesson in course.lessonSet"
            :key="lesson.id"
            :to="course.purchased ? { name: 'lesson', params: { id: lesson.id } } : null"
            :active="$route.name === 'lesson' && $data.lesson && $data.lesson.id === lesson.id"
            >
            <span
              class="font-weight-bold"
              >
              {{ lesson.order }}
            </span>
            <span>
              {{ lesson.title }}
            </span>
          </b-list-group-item>
        </b-list-group>
      </b-col>
      <b-col
        v-if="$route.name === 'lesson' && lesson"
        xl="5"
        >
        <h2
          class="text-center mb-5"
          >
            <span
              class="font-weight-bold"
              >
              {{ lesson.order }}
            </span>
            <span>
              {{ lesson.title }}
            </span>
        </h2>
        <div
          v-html="lesson.description"
          class="mb-5"
          >
        </div>
        <div
          class="mb-5"
          >
          <video-player
            :path="lesson.video"
            >
          </video-player>
        </div>
        <div>
          <b-button
            v-if="lesson.addon"
            :href="addon_button_url"
            class="mx-3"
            >
            {{ addon_button_text }}
          </b-button>
          <b-button
            v-if="lesson.previous"
            :to="{ name: 'lesson', params: { id: lesson.previous.id } }"
            class="mx-3"
            >
            {{ previous_button_text }}
          </b-button>
          <b-button
            v-if="lesson.next"
            :to="{ name: 'lesson', params: { id: lesson.next.id } }"
            class="mx-3"
            >
            {{ next_button_text }}
          </b-button>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import gql from 'graphql-tag';
import CoursePurchaseButton from './CoursePurchaseButton.vue';
import VideoPlayer from './VideoPlayer.vue';
import environment from '../environment';

export default {
  components: {
    CoursePurchaseButton,
    VideoPlayer,
  },
  data() {
    return {
      courses: [],
      course: null,
      lesson: null,
      language: 'uk',
      media: environment.media,
    };
  },
  computed: {
    purchased_badge() {
      return this.language === 'ru' ? 'Куплено' : 'Куплено';
    },
    soon_badge() {
      return this.language === 'ru' ? 'Скоро' : 'Незабаром';
    },
    addon_button_text() {
      return this.language === 'ru' ? 'Дополнительные материалы' : 'Додаткові матеріали';
    },
    addon_button_url() {
      return `${this.media}/${this.lesson.addon}`;
    },
    previous_button_text() {
      return this.language === 'ru' ? 'Предыдущий' : 'Попередній';
    },
    next_button_text() {
      return this.language === 'ru' ? 'Следующий' : 'Наступний';
    },
  },
  apollo: {
    courses: gql`
      query {
        courses {
          id
          soon
          title
          purchased
        }
      }
    `,
    course: {
      query: gql`
        query($id: String!) {
          course(id: $id) {
            id
            soon
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
        return this.$route.name === 'course' ? {
          id: this.$route.params.id,
        } : {
          id: this.lesson.course.id,
        };
      },
      skip() {
        return !(this.$route.name === 'course' || (this.$route.name === 'lesson' && this.lesson));
      },
    },
    lesson: {
      query: gql`
        query($id: String!) {
          lesson(id: $id) {
            id
            order
            title
            course {
              id
            }
            description
            video
            addon
            previous {
              id
            }
            next {
              id
            }
          }
        }
      `,
      variables() {
        return {
          id: this.$route.params.id,
        };
      },
      skip() {
        return this.$route.name !== 'lesson';
      },
    },
    language: gql`
      query {
        language
      }
    `,
  },
};
</script>
