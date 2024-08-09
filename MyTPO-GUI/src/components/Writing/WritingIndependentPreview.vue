<template>
  <!--  <div>Hello writing independent preview world!</div>-->
  <!--  <div>{{ $route.params.examid }}</div>-->
  <q-layout>
    <q-header class="text-center" elevated>
      <q-toolbar>
        <q-btn flat icon="home" round to="/"></q-btn>
        <q-btn flat icon="keyboard_arrow_left" label="Previous Passage"/>
        <q-toolbar-title class="text-h6">
          {{ this.query.caption }}: {{ $route.params.examid }}
        </q-toolbar-title>
        <q-btn flat icon-right="keyboard_arrow_right" label="Next Passage"/>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page class="column justify-start q-pa-md">
        <div class="row col absolute-full q-pa-md">
          <div class="col-6 q-pa-md" style="border: 2px solid lightgrey; border-radius: 20px">
            <div v-for="item in query.prompt">
              <p v-if="item.startsWith('@#')" class="text-h6">{{ item.replace('@#', '') }}</p>
              <p v-else>{{ item }}</p>
            </div>
          </div>
          <div class="col-6 q-pa-md" style="border: 2px solid lightgrey; border-radius: 20px">
            <div class="col text-right q-pa-xs">Word count: {{ countWords(my_ans) }}</div>
            <textarea v-model="my_ans" autocapitalize="off" autocomplete="off" autofocus="autofocus" class="row"
                      spellcheck="false" style="width: 100%; height: 95%; resize: none"></textarea>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import JSON5 from 'json5'

export default {
  name: "WritingIntegratedPreview",

  data() {
    return {
      query: {caption: '', prompt: ''},
      my_ans: ''
    }
  },

  async created() {
    this.query = await window.electron.dataSQL(`select caption, prompt
                                                from writing_independent
                                                where examid = ${this.$route.params.examid}`)
    this.query = this.query[0]
    this.query.prompt = JSON5.parse(this.query.prompt)
    console.log(this.query)
  },

  methods: {
    countWords(str) {
      const value = str.trim()
      if (!value) return 0
      return value.split(/\s+/).length
    }
  }
}
</script>
