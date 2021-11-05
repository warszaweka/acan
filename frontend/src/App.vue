<template>
  <div
    class="min-vh-100 d-flex flex-column"
    >
    <b-navbar
      sticky
      toggleable="sm"
      >
      <b-navbar-brand
        :to="{ name: 'home' }"
        >
        {{ home_label }}
      </b-navbar-brand>
      <b-navbar-toggle
        target="nav-collapse"
        >
      </b-navbar-toggle>
      <b-collapse
        id="nav-collapse"
        is-nav
        >
        <b-navbar-nav>
          <b-nav-item
            :to="{ name: 'courses' }"
            >
            {{ courses_label }}
          </b-nav-item>
          <b-nav-item
            v-if="user"
            :to="{ name: 'user' }"
            >
            {{ user_label }}
          </b-nav-item>
          <b-nav-item
            v-else
            :to="{ name: 'login' }"
            >
            {{ login_label }}
          </b-nav-item>
          <b-nav-item-dropdown
            :text="language_label"
            right
            >
            <b-dropdown-item-button
              v-on:click="setLanguage('uk')"
              :active="language === 'uk'"
              >
              Українська
            </b-dropdown-item-button>
            <b-dropdown-item-button
              v-on:click="setLanguage('ru')"
              :active="language === 'ru'"
              >
              Русский
            </b-dropdown-item-button>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <router-view>
    </router-view>
    <div>
      <b-container>
        <b-row>
          <b-col>
            <div>
              <b-link
                href="tel:+380500189388"
                >
                +380500189388
              </b-link>
            </div>
            <div>
              <b-link
                href="tel:+380687039775"
                >
                +380687039775
              </b-link>
            </div>
            <div>
              <b-link
                href="mailto:analytics.academy.2021@gmail.com"
                >
                analytics.academy.2021@gmail.com
              </b-link>
            </div>
          </b-col>
          <b-col>
            <div>
              <b-link
                :to="{ name: 'public_offer' }"
                >
                {{ public_offer_label }}
              </b-link>
            </div>
            <div>
              <b-link
                :to="{ name: 'privacy_policy' }"
                >
                {{ privacy_policy_label }}
              </b-link>
            </div>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
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
    home_label() {
      return this.language === 'ru' ? 'Академия аналитики' : 'Академія аналітики';
    },
    courses_label() {
      return this.language === 'ru' ? 'Курсы' : 'Курси';
    },
    user_label() {
      return this.language === 'ru' ? 'Пользователь' : 'Користувач';
    },
    login_label() {
      return this.language === 'ru' ? 'Войти' : 'Увійти';
    },
    public_offer_label() {
      return this.language === 'ru' ? 'Публичная оферта' : 'Публічна оферта';
    },
    privacy_policy_label() {
      return this.language === 'ru' ? 'Политика конфиденциальности' : 'Політика конфіденційності';
    },
    language_label() {
      return this.language === 'ru' ? 'Язык' : 'Мова';
    },
  },
  methods: {
    async setLanguage(language) {
      await this.$apollo.mutate({
        mutation: gql`
          mutation ($language: String!) {
            setLanguage(language: $language) {
              id
              title
              shortDescription
              description
              lessonSet {
                id
                title
                description
              }
            }
          }
        `,
        variables: {
          language,
        },
        update: (store, result) => {
          store.writeQuery({
            query: gql`
              query {
                courses {
                  id
                  title
                  shortDescription
                  description
                  lessonSet {
                    id
                    title
                    description
                  }
                }
                language
              }
            `,
            data: {
              courses: result.data.setLanguage,
              language,
            },
          });
        },
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
