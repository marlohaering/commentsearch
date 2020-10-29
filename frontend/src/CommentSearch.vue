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
      <InputCard
        v-model="seedText"
        placeholder="Seed comment"
        @submit="postSeedText"
        v-if="showSeedInput"
      />

      <Card v-for="comment in comments" :key="comment.id" class="proposal-card">
        <template #default>
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
        <template #default>
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
import {ThumbsUpIcon, ThumbsDownIcon, XIcon} from "@zhuowenli/vue-feather-icons";
import Card from "@/Card";
import Action from "@/Action";
import Button from "@/Button";
import InputCard from "@/InputCard";

export default {
  name: "App",
  components: {InputCard, Button, Action, Card, ThumbsUpIcon, ThumbsDownIcon, XIcon},
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

<style scoped>
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

.proposal-card {
  margin-top: 1.9rem;
}
</style>
