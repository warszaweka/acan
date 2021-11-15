<template>
  <b-container
    class="py-3"
    >
    <b-row>
      <b-col>
        <b-form
          @submit.prevent="passwordReset"
          id="password_reset"
          >
          <b-form-group
            :label="password_label"
            label-for="password"
            >
            <b-form-input
              id="password"
              v-model="password"
              type="password"
              required
              >
            </b-form-input>
          </b-form-group>
          <b-button
            type="submit"
            class="mx-3"
            >
            {{ password_reset_button_text }}
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
      password: '',
      language: 'uk',
    };
  },
  computed: {
    password_reset_button_text() {
      return this.language === 'ru' ? 'Сбросить пароль' : 'Скинути пароль';
    },
    password_label() {
      return this.language === 'ru' ? 'Пароль' : 'Пароль';
    },
  },
  methods: {
    async passwordReset() {
      await this.$apollo.mutate({
        mutation: gql`
          mutation($uidb64: String!, $token: String!, $password: String!) {
            passwordReset(uidb64: $uidb64, token: $token, password: $password)
          }
        `,
        variables: {
          uidb64: this.$route.params.uidb64,
          token: this.$route.params.token,
          password: this.password,
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

<style lang="scss" scoped>
#password_reset {
  max-width: 35em;
}
</style>
