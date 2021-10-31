import axios from 'axios';
import environment from './environment';

let token = '';

function getToken() {
  return token;
}

async function refreshToken() {
  token = (await axios.get(environment.csrf, {
    withCredentials: true,
  })).data.token;
}

export { getToken, refreshToken };
