<template>
  <!--  <div>Hello reading preview world!</div>-->
  <!--  <div>{{ $route.params.examid }}</div>-->
  <!--  <div>{{ $route.params.pid }}</div>-->
  <q-layout view="hHh lpR fFf">
    <q-header class="text-center">
      <q-toolbar>
        <q-btn flat icon="keyboard_arrow_left" label="Previous Passage"/>
        <q-toolbar-title>
          <div></div>
          <div>{{ title }}:&nbsp; {{ $route.params.pid }} - {{ $route.params.examid }}</div>
        </q-toolbar-title>
        <q-btn flat icon-right="keyboard_arrow_right" label="Next Passage"/>
      </q-toolbar>

    </q-header>
    <q-page-container></q-page-container>

    <div class="row q-px-md q-py-md">
      <div v-for="(item, index) in query">
        <q-responsive class="q-pa-lg q-mx-xs" ratio="1" style="scale: 93%">
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
    </div>

    <div class="row">
      <div class="col-6 q-pa-md">
        <div id="question">{{ query[curr_idx][1] }}</div>

        <!--单选-->
        <div v-if="query[curr_idx][3].length === 1 && query[curr_idx][2].length === 4">
          <q-list>
            <q-item v-for="(question, index) in query[curr_idx][2]" v-ripple tag="label">
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
        <div v-else-if="query[curr_idx][3].length > 1 && query[curr_idx][3].length < query[curr_idx][2].length">
          <q-item v-for="(question, index) in query[curr_idx][2]" v-ripple tag="label">
            <q-item-section avatar>
              <q-checkbox v-model="my_ans[curr_idx]" :val="int_to_char[index]" @click="my_ans[curr_idx].sort()"/>
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ question }}</q-item-label>
            </q-item-section>
          </q-item>
        </div>

        <!--分类-->

        <!--排序-->

        <!--句子插入-->


        <div>{{ my_ans }}</div>
      </div>
      <div id="passage" class="col-6">
        <div v-html="query[curr_idx][0]"></div>
      </div>
    </div>

  </q-layout>
</template>

<script>
export default {
  name: "ReadingPreview",

  data() {
    return {
      title: "Test title",
      curr_idx: 0,
      query: [
        ["passage 1", "question 1: ", ["answer 1", "answer 2", "answer 3", "answer 4"], ["A"]],
        ["passage 2", "question 2: ", ["answer 1", "answer 2", "answer 3", "answer 4"], ["B"]],
        ["passage 3", "question 3: ", ["answer 1", "answer 2", "answer 3", "answer 4"], ["C"]],
        ["passage 4", "question 4: ", ["answer 1", "answer 2", "answer 3", "answer 4"], ["D"]],
        ["passage 5", "question 5: ", ["answer 1", "answer 2", "answer 3", "answer 4"], ["A", "B"]],
        ["passage 6 <span>Test the span</span>", "question 6: ", ["answer 1", "answer 2", "answer 3", "answer 4"], ["A"]],
        ["passage 7", "question 7: ", ["answer 1", "answer 2", "answer 3", "answer 4"], ["A", "B", "#", "D"]],
        ["passage 8", "question 8: ", ["answer 1", "answer 2", "answer 3", "answer 4"], ["C", "B", "A"]],
        [`<div class="en">
 <h2>
  Twins and Epigenetics
 </h2>
 <p>
 </p>
 <p>
  In the fields of psychology and oncology (the study of cancer), understanding the influence of genetic and environmental factors is paramount to understanding complex phenomena such as human behavior or cancer. The challenge that scientists face is how to distinguish the influence of genetics from the influence of environment on a person's mental and physical state. Also known as the issue of nature (genetics) verses nurture (environment), the degree to which each factor plays a role is still largely unknown. To help navigate through the complex web of nature-nurture influence on human physical and mental development, researchers have often used twins as test subjects.
 </p>
 <p>
  There are two different types of twins. Fraternal twins come from two separate eggs and share the same percentage of genomes (genetic makeup) as any siblings from the same parents might share. Fraternal twins do not necessarily look alike and are not always the same gender. Identical  twins, on the other hand, come from the same egg and therefore have the exact same genomes. Identical twins' shared genomes dictate that they are always the same gender and look alike. Because of their identical genome—or identical natural characteristics—and the fact that most twins grow up together, scientists can more easily distinguish which characteristics of physical and mental behavior are more likely influenced by heredity and which are influenced by environmental factors. Fraternal twins are equally as useful, since they can create a baseline for statistical comparison of environmental factors. Research on the nature-nurture issue has advanced considerably in recent years, partially due to an upsurge of studies on pairs of twins, both fraternal and identical. Studying the similarities and differences of twins helps researchers chart the degree to which genetics and environment factor into what makes us who we are.
 </p>
 <p>
  <i class="strong-insert js-scrollto" data-aid="478">
   【A】
  </i>
  Although studying pairs of twins raised together can provide much information, it is possible that more can be learned about the genetic predisposition of physical and behavioral characteristics from the study of twins raised apart. The first study on twins raised apart was prompted in the late 1970s by the reunion of twin brothers Jim Lewis and Jim Springer. Meeting for the first time at the age of 39, the Jim twins had been raised in two different environments. At that time behaviorists, (psychologists who study human behavior) had long concluded that environment plays a huge role in the development of one's personality and preferences.
  <i class="strong-insert js-scrollto" data-aid="479">
   【B】
  </i>
  However, the eerie similarity between the two Jims attracted the attention of scientists and the public alike. The two men were the same weight and height, drank the same brand of beer, smoked the same brand of cigarettes, and they both had the same habit of leaving love notes lying around the house for their wives.
  <i class="strong-insert js-scrollto" data-aid="480">
   【C】
  </i>
  The reunion of the Jim twins prompted a whole new approach to the nature-nurture issue.
  <i class="strong-insert js-scrollto" data-aid="481">
   【D】
  </i>
 </p>
 <p>
  Since then, scientists have come to understand that the nature-nurture issue cannot be clearly separated into genetic influences and environmental influences. Rather, it is a much more complex mixture of nature and nurture that determines the physical and mental characteristics of humans. More specifically, scientists have expanded their evaluation of the nature-nurture issue to include epigenetics (how the genetic code is expressed in an organism). Even though identical twins share the same DNA, epigenetics determines to what extent these genes are expressed. This might explain why one twin gets sick and the other does not. A recent study on identical twins ranging from ages 3 to 74 has revealed that over time, the structure of twins' genes begins to differ. The study compared the DNA samples of participating sets of twins, which revealed that the structure of the DNA of the younger sets of twins was quite similar, but differences in the DNA structures became more noticeable with the older sets of twins. The greatest difference in gene expression was noticed in twins who had grown up apart or who had different medical histories.
 </p>
 <p>
  Studying the epigenetics of twins is useful because it helps scientists identify genes that might cause certain health problems, like obesity and cancer. A study on genetically identical mice demonstrated how minor changes in gene expression can significantly change physical characteristics. In this study, scientists genetically engineered mice with identical genomes. Half the mice before they were born were exposed to a chemical that stimulates a gene linked to obesity. The result was the creation of two genetically identical, but very different looking mice. The exposed mouse was twice the weight of the unexposed mouse. The mice study demonstrates that the change in the expression of just one gene can dramatically change an organism's characteristics.
 </p>
 <p>
 </p>
</div>`, "question 9: ", ["answer 1", "answer 2", "answer 3", "answer 4"], ["A"]],
        ["passage 10", "question 10: ", ["answer 1", "answer 2", "answer 3", "answer 4", "answer 5", "answer 6"], ["A", "B", "C"]]
      ],
      my_ans: [],
      int_to_char: {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K'},
    }
  },
  mounted() {
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

    // switchQuestion(index) {
    // const my_answer = this.my_ans[this.curr_idx];
    // if (Array.isArray(my_answer) && this.query[this.curr_idx][3].length !== this.query[this.curr_idx][2].length) {   // 多选排序
    //   my_answer.sort();
    // }
    // this.curr_idx = index;
    // }
  }
}
</script>

<style lang="sass" scoped>
@import "src/css/quasar.variables"

#passage:deep(span)
  background-color: lightslategray
  color: white

#passage:deep(h1)
  text-align: center
  font-size: $text-title
  font-weight: bold

#passage:deep(h2)
  text-align: center
  font-size: $text-title
  font-weight: bold

#passage:deep(h3)
  text-align: center
  font-size: $text-title
  font-weight: bold

#passage:deep(h4)
  text-align: center
  font-size: $text-title
  font-weight: bold

#passage:deep(h5)
  text-align: center
  font-size: $text-title
  font-weight: bold

#passage:deep(h6)
  text-align: center
  font-size: $text-title
  font-weight: bold

#passage:deep(p)
  font-family: SansSerif, sans-serif

#passage:deep(p):has(i)::before
  content: '➜'
  color: $secondary

#question:deep(span)
  background-color: lightslategray
  color: white

</style>
