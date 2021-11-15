<template>
  <div
    class="min-vh-100 d-flex flex-column"
    >
    <b-navbar
      sticky
      toggleable="sm"
      variant="light"
      >
      <b-navbar-brand
        :to="{ name: 'home' }"
        >
        <b-img
          :src="require('./assets/images/logo.jpg')"
          height="40"
          >
        </b-img>
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
            {{ courses_link_text }}
          </b-nav-item>
          <b-nav-item
            v-if="user"
            :to="{ name: 'user' }"
            >
            {{ user_link_text }}
          </b-nav-item>
          <b-nav-item
            v-else
            :to="{ name: 'login' }"
            >
            {{ login_link_text }}
          </b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav
          class="ml-auto"
          >
          <b-nav-item-dropdown
            :text="language_button_text"
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
    <div
      class="flex-fill"
      >
      <router-view>
      </router-view>
    </div>
    <div
      class="bg-dark py-3"
      >
      <b-container>
        <b-row>
          <b-col
            md="6"
            class="my-3"
            >
            <div>
              <b-icon
                icon="telephone-fill"
                variant="light"
                >
              </b-icon>
              <b-link
                href="tel:+380500189388"
                class="text-light"
                >
                +380500189388
              </b-link>
            </div>
            <div>
              <b-icon
                icon="telephone-fill"
                variant="light"
                >
              </b-icon>
              <b-link
                href="tel:+380687039775"
                class="text-light"
                >
                +380687039775
              </b-link>
            </div>
            <div>
              <b-icon
                icon="envelope-fill"
                variant="light"
                >
              </b-icon>
              <b-link
                href="mailto:analytics.academy.2021@gmail.com"
                class="text-light"
                >
                analytics.academy.2021@gmail.com
              </b-link>
            </div>
          </b-col>
          <b-col
            md="6"
            class="my-3"
            >
            <div>
              <b-link
                :to="{ name: 'public_offer' }"
                class="text-light"
                >
                {{ public_offer_link_text }}
              </b-link>
            </div>
            <div>
              <b-link
                :to="{ name: 'privacy_policy' }"
                class="text-light"
                >
                {{ privacy_policy_link_text }}
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
    courses_link_text() {
      return this.language === 'ru' ? 'Курсы' : 'Курси';
    },
    user_link_text() {
      return this.language === 'ru' ? 'Кабинет пользователя' : 'Кабінет користувача';
    },
    login_link_text() {
      return this.language === 'ru' ? 'Войти' : 'Увійти';
    },
    language_button_text() {
      return this.language === 'ru' ? 'Язык' : 'Мова';
    },
    public_offer_link_text() {
      return this.language === 'ru' ? 'Публичная оферта' : 'Публічна оферта';
    },
    privacy_policy_link_text() {
      return this.language === 'ru' ? 'Политика конфиденциальности' : 'Політика конфіденційності';
    },
  },
  methods: {
    async setLanguage(language) {
      await this.$apollo.mutate({
        mutation: gql`
          mutation ($language: String!) {
            setLanguage(language: $language) {
              language
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
            }
          }
        `,
        variables: {
          language,
        },
        update(store, { data: { setLanguage } }) {
          store.writeQuery({
            query: gql`
              query {
                language
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
              }
            `,
            data: {
              language: setLanguage.language,
              courses: setLanguage.courses,
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
