<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <Login/>
</template>

<script>
import Login from './components/Login.vue';

export default {
  components: {
    Login
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
