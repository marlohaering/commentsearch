<template>
  <router-view />
</template>

<script>
export default {
  name: "App"
}
</script>

<style>
:root {
  --light: #F4F7F6;
  --light-hinted: #CFD2D7;
  --primary: #5D6A80;
  --dark: #3B4A62;
}

html, body {
  height: 100%;
}

body {
  margin: 0;
  overflow-y: scroll;
  background-color: var(--primary);
}

#app {
  font-family: 'Roboto Slab', serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100%;
  padding-top: 9rem;
  box-sizing: border-box;
}
</style>
