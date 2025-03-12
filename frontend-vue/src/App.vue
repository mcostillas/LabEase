<script setup>
// No setup needed for root component
</script>

<template>
  <router-view />
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
@import '@mdi/font/css/materialdesignicons.css';

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Poppins', sans-serif;
  background: #f5f5f5;
}

button {
  font-family: 'Poppins', sans-serif;
}

input, select {
  font-family: 'Poppins', sans-serif;
  outline: none;
}

input:focus, select:focus {
  border-color: #FF69B4 !important;
}
</style>
