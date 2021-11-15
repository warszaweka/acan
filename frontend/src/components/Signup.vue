<template>
  <b-container
    class="py-3"
    >
    <b-row>
      <b-col>
        <b-form
          @submit.prevent="signup"
          id="signup"
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
            {{ signup_button_text }}
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
      password: '',
      language: 'uk',
      error: null,
    };
  },
  computed: {
    signup_button_text() {
      return this.language === 'ru' ? 'Зарегистрироваться' : 'Зареєструватися';
    },
    email_label() {
      return this.language === 'ru' ? 'Электро́нная по́чта' : 'Електронна пошта';
    },
    password_label() {
      return this.language === 'ru' ? 'Пароль' : 'Пароль';
    },
    error_text() {
      if (this.error === 'Used email') {
        return this.language === 'ru' ? 'Используемая почта' : 'Використовуєма пошта';
      }
      return this.language === 'ru' ? 'Недействительная почта' : 'Недійсна пошта';
    },
  },
  methods: {
    async signup() {
      const { data: { signup } } = (await this.$apollo.mutate({
        mutation: gql`
          mutation($email: String!, $password: String!) {
            signup(email: $email, password: $password)
          }
        `,
        variables: {
          email: this.email,
          password: this.password,
        },
      }));
      if (signup) {
        this.error = signup;
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
#signup {
  max-width: 35em;
}
</style>
