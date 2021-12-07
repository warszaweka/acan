<template>
  <b-container
    class="py-3"
    >
    <b-row>
      <b-col>
        <b-form
          @submit.prevent="setMailingList"
          id="set_mailing_list"
          >
          <b-form-checkbox
            v-model="mailing_list_agreement"
            >
            {{ mailing_list_agreement_label }}
          </b-form-checkbox>
          <b-button
            type="submit"
            class="mx-3"
            >
            {{ set_mailing_list_button_text }}
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
      mailing_list_agreement: false,
      user: null,
      language: 'uk',
    };
  },
  computed: {
    mailing_list_agreement_label() {
      return this.language === 'ru' ? 'Я согласен(-на) на рассылку' : 'Я згоден(-на) з розсиланням';
    },
    set_mailing_list_button_text() {
      return this.language === 'ru' ? 'Изменить настройки рассылки' : 'Змінити налаштування розсилання';
    },
  },
  methods: {
    async setMailingList() {
      await this.$apollo.mutate({
        mutation: gql`
          mutation($mailingList: Boolean!) {
            setMailingList(mailingList: $mailingList)
          }
        `,
        variables: {
          mailingList: this.mailing_list_agreement,
        },
      });
      await this.$apollo.getClient().resetStore();
      this.$router.push({
        name: 'user',
      });
    },
  },
  apollo: {
    user: {
      query: gql`
        query {
          user {
            mailingList
          }
        }
      `,
      result({ data: { user: { mailingList } } }) {
        this.mailing_list_agreement = mailingList;
      },
    },
    language: gql`
      query {
        language
      }
    `,
  },
};
</script>

<style lang="scss" scoped>
#set_mailing_list {
  max-width: 35em;
}
</style>
