<template>
  <h1>CoLiBERT Search.</h1>

  <InputCard
      v-model="query"
      placeholder="Query comment body"
      @submit="postQueryText"
  />

  <Card v-for="comment in comments" :key="comment" class="proposal-card">
    {{ comment }}
  </Card>
</template>

<script>
import Card from "@/Card";
import InputCard from "@/InputCard";
import * as api from "@/api";

export default {
  name: "CoLiBert",
  components: {Card, InputCard},
  data() {
    return {
      query: "",
      comments: [],
    }
  },
  methods: {
    async postQueryText() {
      const response = await api.postCoLiBertQuery(this.query);
      this.comments = await response.json();
    }
  }
}
</script>

<style scoped>
  h1 {
    font-weight: 300;
    font-size: 4rem;
    color: var(--light);
    margin: 0 0 3rem;
    text-align: center;
  }

  .proposal-card {
    margin-top: 1.9rem;
  }
</style>
