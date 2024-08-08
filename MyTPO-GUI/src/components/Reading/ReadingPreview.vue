<template>
  <!--  <div>Hello reading preview world!</div>-->
  <!--  <div>{{ $route.params.examid }}</div>-->
  <!--  <div>{{ $route.params.pid }}</div>-->
  <q-layout>
    <q-header class="text-center" elevated>
      <q-toolbar>
        <q-btn flat icon="home" round to="/"></q-btn>
        <q-btn flat icon="keyboard_arrow_left" label="Previous Passage"/>
        <q-toolbar-title class="text-h6">
          {{ this.query[curr_idx].caption }}: {{ $route.params.pid }} - {{ $route.params.examid }}
        </q-toolbar-title>
        <q-btn flat icon-right="keyboard_arrow_right" label="Next Passage"/>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page class="column justify-start q-pa-md">
        <div class="column col absolute-full q-pa-md">
          <div class="row q-pa-md">
            <q-responsive v-for="(item, index) in query" class="q-pa-lg q-mx-xs" ratio="1" style="scale: 93%">
              <!--Unanswered, current-->
              <q-btn v-if="!isAnswered(index) && index === curr_idx"
                     :label="index + 1" color="secondary" outline
                     @click="curr_idx = index"></q-btn>

              <!--Answered, current-->
              <q-btn
                v-else-if="isAnswered(index) && index === curr_idx"
                :label="index + 1" color="secondary"
                @click="curr_idx = index"></q-btn>

              <!--Unanswered, else-->
              <q-btn v-else-if="!isAnswered(index) && index !== curr_idx"
                     :label="index + 1" outline
                     @click="curr_idx = index"></q-btn>

              <!--Answered, else-->
              <q-btn
                v-else-if="isAnswered(index) && index !== curr_idx"
                :label="index + 1" color="primary"
                @click="curr_idx = index"></q-btn>
            </q-responsive>
          </div>
          <div class="row col">
            <div class="col-6 q-pa-md" style="border: 2px solid lightgrey; border-radius: 20px">
              <div>
                <div v-for="(item, index) in query[curr_idx].prompt"
                     v-if="JSON.stringify(query[curr_idx].choices) === '[]'">
                  <p v-if="index === 1" id="insertedline" class="text-bold">{{ item[0] }}</p>
                  <p v-else>{{ item[0] }}</p>
                </div>
                <div v-for="(item, index) in query[curr_idx].prompt" v-else>
                  <span v-for="i in item" v-if="item.length > 1">
                    <span v-if="i.startsWith('@#') && i !== '@#'" id="highlightSpan"
                          class="q-px-sm q-mx-xs q-py-xs text-bold">{{ i.replace('@#', '') }}</span>
                    <span v-else-if="i === '@#'"
                          class="q-px-sm q-mx-xs text-bold bg-secondary rounded-borders text-white">➜</span>
                    <span v-else>{{ i }}</span>
                  </span>
                  <p v-else>{{ item[0] }}</p>
                </div>
              </div>
              <div>
                <!--单选-->
                <div v-if="query[curr_idx].answers.length === 1 && query[curr_idx].choices.length === 4">
                  <q-list>
                    <q-item v-for="(question, index) in query[curr_idx].choices" v-ripple tag="label">
                      <q-item-section avatar>
                        <q-radio v-model="my_ans[curr_idx]" :val="int_to_char[index]"/>
                      </q-item-section>
                      <q-item-section>
                        <q-item-label>{{ question }}</q-item-label>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </div>

                <!--多选-->
                <div
                  v-else-if="query[curr_idx].answers.length > 1 && query[curr_idx].answers.length < query[curr_idx].choices.length">
                  <q-item v-for="(choice, index) in query[curr_idx].choices" v-ripple tag="label">
                    <q-item-section avatar>
                      <q-checkbox v-model="my_ans[curr_idx]" :val="int_to_char[index]"
                                  @click="my_ans[curr_idx] = my_ans[curr_idx].sort()"/>
                    </q-item-section>
                    <q-item-section>
                      <q-item-label>{{ choice }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </div>

                <div>{{ my_ans }}</div>
              </div>

            </div>

            <div id="passage" class="col-6 q-pa-md" style="border: 2px solid lightgrey; border-radius: 20px">
              <InsertLine v-if="query[curr_idx].choices.length === 0" ref="insertline"
                          :insert_txt="query[curr_idx].prompt[1]" :passage="query[curr_idx].passage"
                          @change-val="my_ans[my_ans.length - 2] = $refs.insertline.selection"/>
              <NormalPassage v-else :paragraph_idx="query[curr_idx].paragraph" :passage="query[curr_idx].passage"/>
            </div>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import JSON5 from 'json5'

import InsertLine from "components/Reading/PassageViews/InsertLine.vue";
import NormalPassage from "components/Reading/PassageViews/NormalPassage.vue";

export default {
  name: "ReadingPreview",
  components: {InsertLine, NormalPassage},

  data() {
    return {
      curr_idx: 0,
      query: [{caption: '', passage: '', prompt: '', choices: '', answers: '', paragraph: 0}],
      my_ans: [],
      int_to_char: {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K'},
    }
  },
  async created() {
    this.query = await window.electron.dataSQL(`select caption, passage, prompt, choices, answers, paragraph
                                                from reading
                                                where examid = ${this.$route.params.examid}
                                                  and pid = ${this.$route.params.pid}
                                                order by num`)


    for (let i of this.query) {
      i.choices = JSON5.parse(i.choices);
      i.answers = JSON5.parse(i.answers);
      i.passage = JSON5.parse(i.passage);
      i.prompt = JSON5.parse(i.prompt);
    }

    this.my_ans = Array(this.query.length).fill([]);
  },
  methods: {
    isAnswered(index) {
      const my_answer = this.my_ans[index];

      if (Array.isArray(my_answer) && my_answer.length > 0) {  // 多选、排序
        return true;
      } else if (typeof my_answer === 'string' && my_answer.length > 0) {  // 单选
        return true;
      }
      return false;
    },
  }
}
</script>

<style lang="sass" scoped>
@import "src/css/quasar.variables"

#insertedline
  color: $secondary
  text-decoration: underline
  text-decoration-color: $secondary

#indicator
  font-weight: bold
  margin-left: 5px
  margin-right: 5px
  color: $primary

#highlightSpan
  display: inline
  border-radius: 3px
  background-color: $secondary
  color: white

#question\ insert:deep(p:nth-of-type(2))
  font-weight: bold
  color: $secondary

</style>
