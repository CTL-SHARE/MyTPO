<template>
  <q-scroll-area ref="scrollArea" class="q-pa-md" style="height: 100%">
    <div v-for="(item, index) in passage" style="text-align: justify;">
      <h4 v-if="index === 0" align="center" class="q-my-sm">
        {{ item }}
      </h4>

      <p v-else-if="item.length === 1">
        <span v-if="index === paragraph_idx"
              class="q-px-sm q-mx-xs text-bold bg-secondary rounded-borders text-white">➜</span>
        <span v-else class="q-px-sm q-mx-sm"></span>
        <span>{{ item[0] }}</span>
      </p>

      <p v-else ref="targetElement">
        <span class="q-px-sm q-mx-xs text-bold bg-secondary rounded-borders text-white">➜</span>
        <span v-for="i in item">
          <span v-if="i.startsWith('@#')">
            <span id="span" class="q-px-sm q-mx-xs q-py-xs text-bold">{{ i.replace('@#', '') }}</span>
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
    paragraph_idx: -1
  },

  methods: {}
}
</script>


<style lang="sass" scoped>
@import "src/css/quasar.variables"

#indicator
  font-weight: bold
  margin-left: 5px
  margin-right: 5px
  color: $primary

#span
  display: inline
  border-radius: 3px
  background-color: $secondary
  color: white


</style>
