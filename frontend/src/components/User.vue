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
            {{ user.email }}
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
  },
  methods: {
    async logout() {
      await this.$apollo.mutate({
        mutation: gql`
          mutation {
            logout {
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
            }
          }
        `,
        update(store, result) {
          store.writeQuery({
            query: gql`
              query {
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
              }
            `,
            data: {
              user: result.data.logout.user,
              courses: result.data.logout.courses,
            },
          });
        },
      });
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
