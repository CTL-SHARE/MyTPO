<template>
  <div v-for="(item, index) in parseHTML(passage)">
    <h4 v-if="index === 0" align="center" class="q-my-sm">
      {{ item }}
    </h4>

    <p v-else-if="item.length === 1" style="text-indent: 5%">
      {{ item[0] }}
    </p>

    <p v-else id="insertP">
      <span v-for="(slice) in item">
        <span v-if="slice.includes('【')"
              :id="'insertSpan'+(selection === slice.replace('【', '').replace('】', '') ? ' selectedSpan' : '')"
              @click="(selection === slice.replace('【', '').replace('】', '')) ? (selection = '') : (selection = slice.replace('【', '').replace('】', '')) ; $emit('change-val')">
          {{ selection === slice.replace('【', '').replace('】', '') ? ' ' + insert_txt + ' ' : slice }}
        </span>
        <span v-else>{{ slice }}</span>
      </span>
    </p>
  </div>
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

  methods: {
    parseHTML(html) {
      const result = [];
      // Match headings and paragraphs, capturing them with their content
      const parts = html.match(/<h[1-6]>.*?<\/h[1-6]>|<p>.*?<\/p>/gs) || [];
      parts.forEach(part => {
        // Check if part contains a heading
        if (/^<h[1-6]>/.test(part)) {
          const headingMatch = part.match(/<h[1-6]>(.*?)<\/h[1-6]>/s);
          if (headingMatch) {
            const headingText = headingMatch[1].trim();
            if (headingText) {
              result.push(headingText);
            }
          }
        }
        // Check if part contains a paragraph
        else if (/^<p>/.test(part)) {
          const paragraphMatch = part.match(/<p>(.*?)<\/p>/s);
          if (paragraphMatch) {
            let content = paragraphMatch[1].trim();
            // Array to hold the text segments
            const segments = [];
            let lastIndex = 0;
            // Match <i> tags and handle text segments
            const iRegex = /<i[^>]*>(.*?)<\/i>/gs;
            let iMatch;
            while ((iMatch = iRegex.exec(content)) !== null) {
              // Add text before <i> tag
              if (iMatch.index > lastIndex) {
                const beforeITag = content.slice(lastIndex, iMatch.index).trim();
                if (beforeITag) {
                  segments.push(beforeITag);
                }
              }
              // Add <i> tag content
              const iTagContent = iMatch[1].trim();
              if (iTagContent) {
                segments.push(iTagContent);
              }
              lastIndex = iMatch.index + iMatch[0].length;
            }
            // Add remaining text after last <i> tag
            if (lastIndex < content.length) {
              const afterLastITag = content.slice(lastIndex).trim();
              if (afterLastITag) {
                segments.push(afterLastITag);
              }
            }
            // Check if there are <i> tags
            if (segments.length > 0) {
              result.push(segments);
            }
          }
        }
      });

      return result;
    }
  }
}
</script>


<style lang="sass" scoped>
@import "src/css/quasar.variables"

#insertP::before
  content: '➜'
  color: $secondary
  margin: 10px 10px 10px 10px
  text-indent: 0

#insertSpan
  color: $primary
  cursor: pointer

#insertSpan\ selectedSpan
  cursor: pointer
  color: $secondary
  text-decoration: underline
  text-decoration-color: $secondary

</style>
