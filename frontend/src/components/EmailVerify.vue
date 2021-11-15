<template>
  <b-container
    class="py-3"
    >
    <b-row>
      <b-col>
        <div>
          <b-button
            v-on:click.prevent="emailVerify"
            >
            {{ email_verify_button_text }}
          </b-button>
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
    email_verify_button_text() {
      return this.language === 'ru' ? 'Верифицировать почту' : 'Веріфікувати пошту';
    },
  },
  methods: {
    async emailVerify() {
      await this.$apollo.mutate({
        mutation: gql`
          mutation($uidb64: String!, $token: String!) {
            emailVerify(uidb64: $uidb64, token: $token)
          }
        `,
        variables: {
          uidb64: this.$route.params.uidb64,
          token: this.$route.params.token,
        },
      });
      this.$router.push({
        name: 'login',
      });
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
