<template>
  <b-container
    class="py-3"
    >
    <b-row>
      <b-col>
        <b-form
          @submit.prevent="coupon_form"
          id="coupon-form"
          >
          <b-alert
            v-if="error"
            show
            >
            {{ error_text }}
          </b-alert>
          <b-form-group
            :label="coupon_label"
            label-for="coupon"
            >
            <b-form-input
              id="coupon"
              v-model="coupon"
              type="text"
              >
            </b-form-input>
          </b-form-group>
          <b-button
            type="submit"
            class="mx-3"
            >
            {{ coupon_form_button_text }}
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
      coupon: '',
      error: false,
    };
  },
  computed: {
    coupon_form_button_text() {
      return this.language === 'ru' ? 'Продолжить' : 'Продовжити';
    },
    coupon_label() {
      return this.language === 'ru' ? 'Промокод' : 'Промокод';
    },
    error_text() {
      return this.language === 'ru' ? 'Недействительный промокод' : 'Недійсний промокод';
    },
  },
  methods: {
    async coupon_form() {
      const { data: { createOrder } } = await this.$apollo.mutate({
        mutation: gql`
          mutation ($id: String!, $coupon: String) {
            createOrder(id: $id, coupon: $coupon) {
              data
              signature
            }
          }
        `,
        variables: {
          id: this.$route.params.id,
          ...(this.coupon === '' ? {} : {
            coupon: this.coupon,
          }),
        },
      });
      if (createOrder === null) {
        this.error = true;
      } else {
        this.$router.push({
          name: 'payment',
          params: {
            id: this.$route.params.id,
            data: createOrder.data,
            signature: createOrder.signature,
          },
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
#coupon-form {
  max-width: 35em;
}
</style>
