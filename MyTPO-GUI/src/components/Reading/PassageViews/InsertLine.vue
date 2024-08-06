<template>
  <q-scroll-area ref="scrollArea" class="q-pa-md" style="height: 100%">
    <div v-for="(item, index) in passage">
      <h4 v-if="index === 0" align="center" class="q-my-sm">
        {{ item }}
      </h4>

      <p v-else-if="item.length === 1">
        <span class="q-px-sm q-mx-sm"></span>
        {{ item[0] }}
      </p>

      <p v-else id="insertP">
        <span class="q-px-sm q-mx-xs text-bold bg-secondary rounded-borders text-white">➜</span>
        <span v-for="i in item">
          <span v-if="i.startsWith('@#')" :id="'insertSpan'+(selection === i[3] ? ' selectedSpan' : '')"
                class="q-px-sm q-mx-xs text-bold"
                @click="(selection === i[3]) ? (selection = []) : (selection = i[3]) ; $emit('change-val')">
            {{ selection === i[3] ? insert_txt[0] : i[3] }}
          </span>
          <span v-else>{{ i }}</span>
        </span>
      </p>
    </div>
  </q-scroll-area>
</template>

<script>
export default {
  name: 'InsertLine',

  data() {
    return {
      selection: '',
    }
  },

  props: {
    passage: String,
    insert_txt: String
  },

  methods: {}
}
</script>


<style lang="sass" scoped>
@import "src/css/quasar.variables"

#insertSpan
  cursor: pointer
  display: inline
  border-radius: 3px
  background-color: $secondary
  color: white

#insertSpan\ selectedSpan
  cursor: pointer
  color: $secondary
  text-decoration: underline
  text-decoration-color: $secondary

</style>
