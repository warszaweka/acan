<template>
  <b-container
    class="py-3"
    >
    <b-row>
      <b-col>
        <b-form
          @submit.prevent="requestPasswordReset"
          id="request_password_reset"
          >
          <b-alert
            v-if="error"
            show
            >
            {{ error_text }}
          </b-alert>
          <b-form-group
            :label="email_label"
            label-for="email"
            >
            <b-form-input
              id="email"
              v-model="email"
              type="email"
              required
              >
            </b-form-input>
          </b-form-group>
          <b-button
            type="submit"
            class="mx-3"
            >
            {{ request_password_reset_button_text }}
          </b-button>
        </b-form>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import gql from 'graphql-tag';

export default {
  data() {
    return {
      email: '',
      language: 'uk',
      error: null,
    };
  },
  computed: {
    request_password_reset_button_text() {
      return this.language === 'ru' ? 'Сбросить пароль' : 'Скинути пароль';
    },
    email_label() {
      return this.language === 'ru' ? 'Электро́нная по́чта' : 'Електронна пошта';
    },
    error_text() {
      return this.language === 'ru' ? 'Неиспользуемая почта' : 'Невикористовуєма пошта';
    },
  },
  methods: {
    async requestPasswordReset() {
      const { data: { requestPasswordReset } } = (await this.$apollo.mutate({
        mutation: gql`
          mutation($email: String!) {
            requestPasswordReset(email: $email)
          }
        `,
        variables: {
          email: this.email,
        },
      }));
      if (requestPasswordReset) {
        this.error = requestPasswordReset;
      } else {
        this.$router.push({
          name: 'login',
        });
      }
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

<style lang="scss" scoped>
#request_password_reset {
  max-width: 35em;
}
</style>
