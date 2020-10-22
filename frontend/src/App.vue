<template>
  <div>
    <h1>Better Comment Search.</h1>
    <div class="main-actions" v-if="submittedSeed">
      <Button @click="addSeed">Add Seed</Button>
      <Button @click="showHistory = !showHistory">History</Button>
      <Button @click="reset">Reset</Button>
    </div>

    <div class="content-separator" />

    <template v-if="!showHistory">
      <Card v-if="showSeedInput">
        <template #main>
          <textarea
              placeholder="Seed comment"
              rows="4"
              @keydown.enter.prevent
              @keyup.enter="postSeedText"
              v-model="seedText"
              class="seed-text-textarea"
              autofocus
          />
        </template>
        <template #actions>
          <Action @click="postSeedText"><SendIcon /></Action>
        </template>
      </Card>

      <Card v-for="comment in comments" :key="comment.id" class="proposal-card">
        <template #main>
          {{ comment.body }}
        </template>

        <template #actions>
          <Action @click="postCommentAnnotation(comment.id, true)">
            <ThumbsUpIcon />
          </Action>
          <Action @click="postCommentAnnotation(comment.id, false)">
            <ThumbsDownIcon />
          </Action>
        </template>
      </Card>
    </template>

    <template v-if="showHistory">
      <Card v-for="(conceptElement, idx) in session" :key="conceptElement.id" class="proposal-card">
        <template #main>
          <b>{{conceptElement.positive ? "Positive" : "Negative"}}:</b> {{ conceptElement.body || conceptElement.text }}
        </template>

        <template #actions>
          <Action @click="deleteConcept(idx)"><XIcon /></Action>
        </template>
      </Card>
    </template>
  </div>
</template>

<script>
import { postSeedText, postCommentAnnotation, putUpdateConcept } from "./api";
import {SendIcon, ThumbsUpIcon, ThumbsDownIcon, XIcon} from "@zhuowenli/vue-feather-icons";
import Card from "@/Card";
import Action from "@/Action";
import Button from "@/Button";

export default {
  name: "App",
  components: {Button, Action, Card, SendIcon, ThumbsUpIcon, ThumbsDownIcon, XIcon},
  data() {
    return {
      sessionId: "",
      seedText: "",
      comments: [],
      session: [],
      submittedSeed: false,
      forceShowSeed: false,
      showHistory: false,
    };
  },

  computed: {
    showSeedInput() {
      return this.forceShowSeed || !this.submittedSeed;
    },
  },

  mounted() {
    this.reset();
  },

  methods: {
    addSeed() {
      this.forceShowSeed = !this.forceShowSeed;
    },

    reset() {
      this.sessionId = Math.floor(10000 * Math.random());
      this.seedText = "";
      this.comments = [];
      this.session = [];
      this.forceShowSeed = false;
      this.submittedSeed = false;
      this.showHistory = false;
    },

    async postSeedText() {
      this.forceShowSeed = false;
      this.submittedSeed = true;
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

h1 {
  font-weight: 300;
  font-size: 4rem;
  color: var(--light);
  margin: 0;
  text-align: center;
}

.main-actions {
  text-align: center;
}

.content-separator {
  margin-bottom: 3rem;
}

.seed-text-textarea {
  width: 100%;
  padding: 0;
  border: none;
  background-color: transparent;
  font: inherit;
  resize: none;
  outline: none;
}

.proposal-card {
  margin-top: 1.9rem;
}
</style>
