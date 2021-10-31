import axios from 'axios'
import environment from './environment'

let token = ""

async function refresh_token() {
  token = (await axios.get(environment.csrf, {
    withCredentials: true,
  })).data.token
}

export {token, refresh_token}
