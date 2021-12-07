<template>
  <b-container
    class="py-3"
    >
    <b-row>
      <b-col>
        <div
          id="liqpay_checkout"
          >
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
      ok: false,
      course: null,
    };
  },
  mounted() {
    window.LiqPayCheckoutCallback = () => {
      window.LiqPayCheckout.init({
        data: this.$route.params.data,
        signature: this.$route.params.signature,
        embedTo: '#liqpay_checkout',
        mode: 'embed',
      }).on('liqpay.callback', async (data) => {
        if (data.result === 'ok') {
          await this.$apollo.getClient().resetStore();
          this.ok = true;
        }
      });
    };
    const liqpayScript = document.createElement('script');
    liqpayScript.setAttribute('src', '//static.liqpay.ua/libjs/checkout.js');
    document.head.appendChild(liqpayScript);
  },
  apollo: {
    course: {
      query: gql`
        query($id: String!) {
          course(id: $id) {
            id
            purchased
          }
        }
      `,
    },
    variables() {
      return {
        id: this.$route.params.id,
      };
    },
    pollInterval: 1000,
    result({ data: { course: { purchased } } }) {
      if (purchased) {
        this.$router.push({
          name: 'home',
        });
      }
    },
    skip() {
      return this.ok;
    },
  },
};
</script>
