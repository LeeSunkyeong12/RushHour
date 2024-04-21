<template>
    <div class="login-form-container">
      <div class="login-form">
        <h2>LOGIN</h2>
        <input type="text" v-model="user.id" class="form-control" placeholder="ID" />
        <input type="password" v-model="user.password" class="form-control" placeholder="PW" />
        <button @click="login" class="login-button">로그인</button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    name: 'Login-app',
    setup() {
      const user = ref({ id: '', password: '' });
  
      const login = () => {
        // Handle the login logic here, such as an API call
        alert('Login attempted for ID: ' + user.value.id);
      };
  
      return { user, login };
    }
  };
  </script>
  
  <style>
  .login-form-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
  }
  .login-form {
    width: 100%;
    max-width: 300px;
    margin: 0 auto;
    padding: 20px;
    background: #f2a365;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  .form-control {
    width: 100%;
    margin-bottom: 10px;
    padding: 10px;
    font-size: 16px;
    border-radius: 5px;
    border: 1px solid #ddd;
    box-sizing: border-box; /* Ensures padding does not affect overall width */
  }
  .login-button {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 5px;
    background-color: #ec9b3b;
    font-size: 16px;
    color: white;
    cursor: pointer;
    box-sizing: border-box; /* Ensures padding does not affect overall width */
  }
  .login-button:hover {
    background-color: #da7b23;
  }
  
  /* Responsive styles */
  @media (min-width: 576px) {
    .login-form {
      max-width: 350px;
    }
  }
  
  @media (min-width: 768px) {
    .login-form {
      max-width: 400px;
    }
  }
  
  @media (min-width: 992px) {
    .login-form {
      max-width: 450px;
    }
  }
  
  @media (min-width: 1200px) {
    .login-form {
      max-width: 500px;
    }
  }
  </style>
  