<template>
  <div>
    <h1>Better Comment Search</h1>
    <div>
      <input type="text" v-on:keyup.enter="postSeedText" v-model="seedText" />
      <button type="button" @click="postSeedText">Add</button>
    </div>
    <ul>
      <li class="comment" v-for="comment in comments" :key="comment.id">{{comment.body}}

        <button type="button" @click="postCommentAnnotation(comment.id, true)">Positive</button>
        <button type="button" @click="postCommentAnnotation(comment.id, false)">Negative</button>

      </li>
    </ul>
  </div>
</template>

<script>

import {postSeedText, postCommentAnnotation} from './api'

export default {
  name: 'App',

  data() {
    return {
      sessionId: '',
      seedText: '',
      comments: []

    }
  },

  mounted() {
    this.sessionId = Math.floor(10000 * Math.random());
  }, 
  
  methods: {
    async postSeedText() {
      const response = await postSeedText(this.sessionId, this.seedText);
      this.comments = await response.json();
    },

    async postCommentAnnotation(id, positive) {
      const response = await postCommentAnnotation(this.sessionId, id, positive);
      this.comments =  await response.json();

    } 
  }
}
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

.comment {
  border: solid black 1px;
  margin: 5px;
}
</style>
