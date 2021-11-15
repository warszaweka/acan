<template>
  <b-container
    class="py-3"
    >
    <b-row>
      <b-col>
        <b-form
          @submit.prevent="setPassword"
          id="set_password"
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
            {{ set_password_button_text }}
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
    set_password_button_text() {
      return this.language === 'ru' ? 'Изменить пароль' : 'Змінити пароль';
    },
    password_label() {
      return this.language === 'ru' ? 'Пароль' : 'Пароль';
    },
  },
  methods: {
    async setPassword() {
      await this.$apollo.mutate({
        mutation: gql`
          mutation($password: String!) {
            setPassword(password: $password)
          }
        `,
        variables: {
          password: this.password,
        },
      });
      this.$router.push({
        name: 'user',
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
#set_password {
  max-width: 35em;
}
</style>
