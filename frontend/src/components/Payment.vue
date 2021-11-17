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
  mounted() {
    window.LiqPayCheckoutCallback = () => {
      window.LiqPayCheckout.init({
        data: this.$route.params.data,
        signature: this.$route.params.signature,
        embedTo: '#liqpay_checkout',
        mode: 'embed',
      }).on('liqpay.callback', async (data) => {
        if (data.result === 'ok') {
          await this.$apollo.getClient().refetchQueries({
            include: [
              gql`
                query {
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
            ],
          });
        }
        this.$router.push({
          name: 'home',
        });
      });
    };
    const liqpayScript = document.createElement('script');
    liqpayScript.setAttribute('src', '//static.liqpay.ua/libjs/checkout.js');
    document.head.appendChild(liqpayScript);
  },
};
</script>
