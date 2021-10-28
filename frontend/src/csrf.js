import axios from 'axios'
import store from './store'
import environment from './environment'

let token

export default function() {
  return token
}

axios.get(environment.csrf, {
  withCredentials: true,
})
  .then(function (response) {
    token = response.data.token
    store.commit('csrfon')
  })
