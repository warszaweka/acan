<template>
  <b-container
    class="py-3"
    >
    <b-row>
      <b-col>
        <h2
          class="text-center mb-5"
          >
          {{ public_offer_header }}
        </h2>
        <div
          v-html="public_offer"
          >
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import gql from 'graphql-tag';

export default {
  data() {
    return {
      language: 'uk',
    };
  },
  computed: {
    public_offer_header() {
      return this.language === 'ru' ? 'Публичная оферта' : 'Публічна оферта';
    },
    public_offer() {
      return this.language === 'ru' ? 'Публичная оферта' : 'Публічна оферта';
    },
  },
  apollo: {
    language: gql`
      query {
        language
      }
    `,
  },
};
</script>
