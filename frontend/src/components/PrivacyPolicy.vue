<template>
  <b-container
    class="py-3"
    >
    <b-row>
      <b-col>
        <h2
          class="text-center mb-5"
          >
          {{ privacy_policy_header }}
        </h2>
        <div
          v-html="privacy_policy"
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
    privacy_policy_header() {
      return this.language === 'ru' ? 'Политика конфиденциальности' : 'Політика конфіденційності';
    },
    privacy_policy() {
      return this.language === 'ru' ? 'Политика конфиденциальности' : 'Політика конфіденційності';
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
