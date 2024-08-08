<template>
  <q-scroll-area ref="scrollArea" class="q-pa-md" style="height: 100%">
    <div ref="parent">
      <div v-for="(item, index) in passage" style="text-align: justify;">
        <h4 v-if="index === 0" align="center" class="q-my-sm">
          {{ item }}
        </h4>

        <p v-else-if="item.length === 1">
        <span v-if="index === paragraph_idx"
              ref="targetElement" class="q-px-sm q-mx-xs text-bold bg-secondary rounded-borders text-white">➜</span>
          <span v-else class="q-px-sm q-mx-sm"></span>
          <span>{{ item[0] }}</span>
        </p>

        <p v-else>
          <span ref="targetElement" class="q-px-sm q-mx-xs text-bold bg-secondary rounded-borders text-white">➜</span>
          <span v-for="i in item">
          <span v-if="i.startsWith('@#')">
            <span id="span" class="text-bold">{{ i.replace('@#', '') }}</span>
          </span>
          <span v-else>{{ i }}</span>
        </span>
        </p>
      </div>
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
    passage: Array, // Changed to Array as you're iterating over it
    paragraph_idx: Number // Changed to Number for consistency
  },

  methods: {
    autoScroll() {
      const target = this.$refs.targetElement[0]
      const parent = this.$refs.parent;
      if (target && parent) {
        const elementRect = target.getBoundingClientRect();
        const parentRect = parent.getBoundingClientRect();
        const topPercentage = ((elementRect.top - parentRect.top) / parentRect.height);
        this.$refs.scrollArea.setScrollPercentage('vertical', topPercentage * 2, 200)
      }
    }
  },

  mounted() {
    this.$nextTick(() => {
      this.autoScroll();
    });
  },

  watch: {
    passage() {
      this.$nextTick(() => {
        this.autoScroll();
      });
    }
  }
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
  -webkit-box-decoration-break: clone
  box-decoration-break: clone
  padding: 4px

</style>
