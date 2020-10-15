<template>
  <div>
    <h1>Better Comment Search</h1>
    <div>
      <textarea
        placeholder="Seed text for searching comments"
        rows="10"
        cols="50"
        v-on:keyup.enter="postSeedText"
        v-model="seedText"
      />
      <br />
      <button type="button" @click="postSeedText">Add</button>
    </div>

    <ul>
      <li v-for="(conceptElement, id) in session" :key = 'id'>
        {{conceptElement}}
        <button type="button" @click="deleteConcept(id)">X</button>
      </li>
    </ul>

    <ul>
      <li class="comment" v-for="comment in comments" :key="comment.id">
        {{ comment.body }}

        <button type="button" @click="postCommentAnnotation(comment.id, true)">
          Positive
        </button>
        <button type="button" @click="postCommentAnnotation(comment.id, false)">
          Negative
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
import { postSeedText, postCommentAnnotation, putUpdateConcept } from "./api";

export default {
  name: "App",

  data() {
    return {
      sessionId: "",
      seedText: "",
      comments: [],
      session: [] 
    };
  },

  mounted() {
    this.sessionId = Math.floor(10000 * Math.random());
  },

  methods: {
    async postSeedText() {
      const response = await postSeedText(this.sessionId, this.seedText);
      this.processResponse(response);
      this.seedText = "";
    },

    async postCommentAnnotation(id, positive) {
      const response = await postCommentAnnotation(
        this.sessionId,
        id,
        positive
      );
      this.processResponse(response);
    },

    async deleteConcept(id) {
const response = await putUpdateConcept(
        this.sessionId,
        id
      );
      this.processResponse(response);
    },

    async processResponse(response) {
      const { comments, session } = await response.json();
      this.comments = comments;
      this.session = session;
    },
  },
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

ul {
  list-style: none;
}

.comment {
  border: solid black 1px;
  margin: 5px;
}
</style>
