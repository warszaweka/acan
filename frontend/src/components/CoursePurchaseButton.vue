<template>
  <span>
    <span
      v-if="course"
      >
      <b-button
        v-on:click.prevent="purchase"
        >
        <span>
          {{ course.cost }}
        </span>
        <span
          v-if="course.previousCost"
          id="previous-cost"
          >{{ course.previousCost }}</span>
        <span>
          UAH
        </span>
        <b-badge
          v-if="course.discountDeadline"
          variant="light"
          >
          <span>
            {{ till_text }}
          </span>
          <span>
            {{ course.discountDeadline }}
          </span>
        </b-badge>
      </b-button>
    </span>
  </span>
</template>

<script>
import gql from 'graphql-tag';

export default {
  data() {
    return {
      course: null,
      user: null,
      language: 'uk',
    };
  },
  props: [
    'id',
  ],
  computed: {
    till_text() {
      return this.language === 'ru' ? 'До' : 'До';
    },
  },
  methods: {
    async purchase() {
      if (this.user) {
        this.$router.push({
          name: 'coupon',
          params: {
            id: this.course.id,
          },
        });
      } else {
        this.$router.push({
          name: 'login',
        });
      }
    },
  },
  apollo: {
    course: {
      query: gql`
        query($id: String!) {
          course(id: $id) {
            id
            cost
            previousCost
            discountDeadline
          }
        }
      `,
      variables() {
        return {
          id: this.id,
        };
      },
    },
    user: gql`
      query {
        user {
          email
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

<style lang="scss" scoped>
#previous-cost {
  text-decoration: line-through red;
}
</style>
