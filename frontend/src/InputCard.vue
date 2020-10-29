<template>
  <Card>
    <template #default>
      <textarea
          :placeholder="placeholder"
          rows="4"
          :value="modelValue"
          @input="$emit('update:modelValue', $event.target.value)"
          @keydown.enter.prevent
          @keyup.enter="$emit('submit')"
          class="textarea"
          autofocus
      />
    </template>

    <template #actions>
      <Action @click="$emit('submit')"><SendIcon /></Action>
    </template>
  </Card>
</template>

<script>
import Action from '@/Action';
import Card from '@/Card';
import {SendIcon} from "@zhuowenli/vue-feather-icons";

export default {
  name: "InputCard",
  components: { Action, Card, SendIcon },
  props: ['placeholder', 'modelValue'],
}
</script>

<style scoped>
  .textarea {
    width: 100%;
    padding: 0;
    border: none;
    background-color: transparent;
    font: inherit;
    resize: none;
    outline: none;
  }
</style>
