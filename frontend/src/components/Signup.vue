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
          <b-form-group
            :label="phone_label"
            label-for="phone"
            >
            <b-form-input
              id="phone"
              v-model="phone"
              type="tel"
              required
              >
            </b-form-input>
          </b-form-group>
          <b-form-group
            :label="first_name_label"
            label-for="first_name"
            >
            <b-form-input
              id="first_name"
              v-model="first_name"
              required
              >
            </b-form-input>
          </b-form-group>
          <b-form-group
            :label="last_name_label"
            label-for="last_name"
            >
            <b-form-input
              id="last_name"
              v-model="last_name"
              required
              >
            </b-form-input>
          </b-form-group>
          <b-form-checkbox
            required
            name="public_offer_privacy_policy_agreement"
            >
            <span>
              {{ public_offer_privacy_policy_agreement_start }}
            </span>
            <b-link
              :to="{ name: 'privacy_policy' }"
              >
              {{ privacy_policy_link_text }}
            </b-link>
            <span>
              {{ public_offer_privacy_policy_agreement_middle }}
            </span>
            <b-link
              :to="{ name: 'pubic_offer' }"
              >
              {{ public_offer_link_text }}
            </b-link>
            <span>
              {{ public_offer_privacy_policy_agreement_finish }}
            </span>
          </b-form-checkbox>
          <b-form-checkbox
            v-model="mailing_list_agreement"
            >
            {{ mailing_list_agreement_label }}
          </b-form-checkbox>
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
      phone: '',
      first_name: '',
      last_name: '',
      mailing_list_agreement: false,
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
    phone_label() {
      return this.language === 'ru' ? 'Номер телефона' : 'Номер телефону';
    },
    first_name_label() {
      return this.language === 'ru' ? 'Имя' : 'Ім\'я';
    },
    last_name_label() {
      return this.language === 'ru' ? 'Фамилия' : 'Прізвище';
    },
    public_offer_privacy_policy_agreement_start() {
      return this.language === 'ru' ? 'Я согласен(-на) с' : 'Я згоден(-на) з';
    },
    privacy_policy_link_text() {
      return this.language === 'ru' ? 'политикой конфиденциальности' : 'політикою конфіденційності';
    },
    public_offer_privacy_policy_agreement_middle() {
      return this.language === 'ru' ? 'и принимаю' : 'та приймаю';
    },
    public_offer_link_text() {
      return this.language === 'ru' ? 'публичный договор оферты' : 'договір публічної оферти';
    },
    public_offer_privacy_policy_agreement_finish() {
      return this.language === 'ru' ? '' : '';
    },
    mailing_list_agreement_label() {
      return this.language === 'ru' ? 'Я согласен(-на) на рассылку' : 'Я згоден(-на) з розсиланням';
    },
    error_text() {
      if (this.error === 'Used email') {
        return this.language === 'ru' ? 'Используемая почта' : 'Використовуєма пошта';
      }
      if (this.error === 'Unvalid email') {
        return this.language === 'ru' ? 'Недействительная почта' : 'Недійсна пошта';
      }
      return this.language === 'ru' ? 'Недействительные данные' : 'Недійсні дані';
    },
  },
  methods: {
    async signup() {
      const { data: { signup } } = (await this.$apollo.mutate({
        mutation: gql`
          mutation($email: String!, $password: String!, $phone: String!, $firstName: String!, $lastName: String!, $mailingList: Boolean!) {
            signup(email: $email, password: $password, phone: $phone, firstName: $firstName, lastName: $lastName, mailingList: $mailingList)
          }
        `,
        variables: {
          email: this.email,
          password: this.password,
          phone: this.phone,
          firstName: this.first_name,
          lastName: this.last_name,
          mailingList: this.mailing_list_agreement,
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
