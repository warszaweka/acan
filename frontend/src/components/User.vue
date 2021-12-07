<template>
  <b-container
    class="py-3"
    >
    <b-row>
      <b-col>
        <div v-if="user">
          <div
            class="mb-3"
            >
            <span>
              {{ user.firstName }}
            </span>
            <span>
              {{ user.lastName }}
            </span>
          </div>
          <div
            class="mb-3"
            >
            {{ user.email }}
          </div>
          <div
            class="mb-3"
            >
            {{ user.phone }}
          </div>
          <div>
            <b-button
              v-on:click.prevent="logout"
              class="mx-3"
              >
              {{ logout_button_text }}
            </b-button>
            <b-button
              :to="{ name: 'set_password' }"
              class="mx-3"
              >
              {{ set_password_button_text }}
            </b-button>
            <b-button
              :to="{ name: 'set_mailing_list' }"
              class="mx-3"
              >
              {{ set_mailing_list_button_text }}
            </b-button>
          </div>
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
      user: null,
      language: 'uk',
    };
  },
  computed: {
    logout_button_text() {
      return this.language === 'ru' ? 'Выйти' : 'Вийти';
    },
    set_password_button_text() {
      return this.language === 'ru' ? 'Изменить пароль' : 'Змінити пароль';
    },
    set_mailing_list_button_text() {
      return this.language === 'ru' ? 'Изменить настройки рассылки' : 'Змінити налаштування розсилання';
    },
  },
  methods: {
    async logout() {
      await this.$apollo.mutate({
        mutation: gql`
          mutation {
            logout
          }
        `,
      });
      await this.$apollo.getClient().resetStore();
      this.$router.push({
        name: 'home',
      });
    },
  },
  apollo: {
    user: gql`
      query {
        user {
          email
          phone
          firstName
          lastName
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
