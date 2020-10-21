<template>
  <div class="card">
    <div class="main">
      <slot name="main" />
    </div>
    <div class="divider" />
    <div class="actions">
      <slot name="actions" />
    </div>
  </div>
</template>

<script>
export default {
  name: "Card",
}
</script>

<style scoped>
  .card {
    display: flex;
    max-width: 35rem;
    min-height: 2rem;
    margin-left: auto;
    margin-right: auto;

    background-color: var(--light);
    border-radius: 0.3rem;
    box-shadow: 0 3px 3px rgba(0, 0, 0, 0.35), 0 6px 10px rgba(0, 0, 0, 0.25)
  }

  .main {
    flex: 1;
    margin: 1.6rem 1.4rem 1.6rem 2.5rem;
  }

  .divider {
    width: 2px;
    background-color: var(--light-hinted);
    margin: 0.8rem 0;
  }

  .actions {
    align-self: center;
  }
</style>
