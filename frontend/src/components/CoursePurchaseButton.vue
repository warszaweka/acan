<template>
  <span>
    <b-button
      v-if="course"
      v-on:click.prevent="purchase"
      >
      <span>
        {{ course.cost }}
      </span>
      <span>
        UAH
      </span>
    </b-button>
  </span>
</template>

<script>
import gql from 'graphql-tag';

export default {
  data() {
    return {
      course: null,
      user: null,
    };
  },
  props: [
    'id',
  ],
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
  },
};
</script>
