import { createApp } from 'vue';
import App from './App.vue';
import Login from './components/Login.vue';

const app = createApp(App);

app.component('Login-app', Login);

app.mount('#app');