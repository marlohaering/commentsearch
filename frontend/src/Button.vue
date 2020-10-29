<template>
  <button type="button">
    <slot />
  </button>
</template>

<script>
export default {
  name: "Button"
}
</script>

<style scoped>
  button {
    border: none;
    background-color: transparent;
    color: var(--light);
    padding: 0.4rem 1.1rem;
    text-transform: uppercase;
    font: inherit;
    cursor: pointer;
    outline: none;
  }

  button:hover {
    text-decoration: underline;
  }

  button:active {
    color: var(--light-hinted);
  }
</style>
