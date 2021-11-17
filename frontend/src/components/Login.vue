<template>
  <b-container
    class="py-3"
    >
    <b-row>
      <b-col>
        <b-form
          @submit.prevent="login"
          id="login"
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
            {{ login_button_text }}
          </b-button>
          <b-button
            :to="{ name: 'request_password_reset' }"
            class="mx-3"
            >
            {{ request_password_reset_button_text }}
          </b-button>
          <b-button
            :to="{ name: 'signup' }"
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
import { refreshToken } from '../apollo';

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
    login_button_text() {
      return this.language === 'ru' ? 'Войти' : 'Увійти';
    },
    email_label() {
      return this.language === 'ru' ? 'Электро́нная по́чта' : 'Електронна пошта';
    },
    password_label() {
      return this.language === 'ru' ? 'Пароль' : 'Пароль';
    },
    error_text() {
      if (this.error === 'Unverified email') {
        return this.language === 'ru' ? 'Неверифицированная почта' : 'Неверіфікована пошта';
      }
      return this.language === 'ru' ? 'Недействительные данные' : 'Недійсні дані';
    },
    request_password_reset_button_text() {
      return this.language === 'ru' ? 'Сбросить пароль' : 'Скинути пароль';
    },
    signup_button_text() {
      return this.language === 'ru' ? 'Зарегистрироваться' : 'Зареєструватися';
    },
  },
  methods: {
    async login() {
      const { data: { login } } = (await this.$apollo.mutate({
        mutation: gql`
          mutation($email: String!, $password: String!) {
            login(email: $email, password: $password) {
              user {
                email
              }
              courses {
                id
                lessonSet {
                  description
                  video
                  addon
                }
                purchased
              }
              error
            }
          }
        `,
        variables: {
          email: this.email,
          password: this.password,
        },
        update(store, result) {
          if (!result.data.login.error) {
            store.writeQuery({
              query: gql`
                query {
                  user {
                    email
                  }
                  courses {
                    id
                    lessonSet {
                      id
                      description
                      video
                      addon
                    }
                    purchased
                  }
                }
              `,
              data: {
                user: result.data.login.user,
                courses: result.data.login.courses,
              },
            });
          }
        },
      }));
      if (login.error) {
        this.error = login.error;
      } else {
        refreshToken();
        this.$router.push({
          name: 'home',
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
#login {
  max-width: 35em;
}
</style>
