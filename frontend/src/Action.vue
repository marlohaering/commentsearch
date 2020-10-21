<template>
  <button class="action-button">
    <slot />
  </button>
</template>

<script>
export default {
  name: "Action"
}
</script>

<style scoped>
  .action-button {
    border: none;
    background-color: transparent;
    color: var(--primary);
    display: flex;
    padding: 0.4rem 1.4rem;
    cursor: pointer;
    outline: none;
    transition: color 0.2s ease;
  }

  .action-button:hover {
    color: var(--dark);
  }

  .action-button:active {
    transition: color 0.05s ease;
    color: black;
  }
</style>
