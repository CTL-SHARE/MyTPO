<script setup>
import {useRouter} from 'vue-router';

const router = useRouter();

</script>

<template>
  <div>
    <q-btn class="q-ma-md" color="primary" icon="visibility"
           inline-label label="Preview" @click="console.log(selection)"></q-btn>
    <q-btn class="q-mx-md" color="secondary" icon="fast_forward"
           inline-label label="Mock" @click="console.log(selection)"></q-btn>
    <span v-show="selection.length === 1" class="q-mx-md">1 passage selected</span>
    <span v-show="selection.length >= 2" class="q-mx-md">{{ selection.length }} passages selected</span>
  </div>

  <q-table ref="table" :columns="cols" :rows="rows" :selected.sync="selection" row-key="examid" selection="multiple"
           separator="cell">
    <template v-slot:header="props">
      <q-tr :props="props">
        <q-th class="q-mx-md">
        </q-th>
        <q-th
          v-for='col in props.cols'
          :key='col.name'
          :props='props'
          class="q-mx-md"
        >
          {{ col.label }}
        </q-th>
      </q-tr>
    </template>

    <template v-slot:body="props">
      <q-tr :props="props" align="center">
        <q-td class="q-mx-md">
          <q-checkbox :model-value="props.selected" dense @update:model-value="updateRows(props.row)"></q-checkbox>
        </q-td>
        <q-td key="title" :props="props" class="q-mx-md">{{ props.row.title }}</q-td>
        <q-td key="progress" :props="props" class="q-mx-md">
          <q-linear-progress :value="props.row.finish / props.row.full" color="positive" rounded></q-linear-progress>
          <div>{{ props.row.finish }} / {{ props.row.full }}</div>
        </q-td>
        <q-td v-for='col in props.cols.slice(2, props.cols.length - 1)'
              :key='col.name'
              :props='props'
              class="q-mx-md"
        >{{ col.value }}
        </q-td>
        <q-td key="actions" :props="props" class="q-mx-md">
          <q-btn :to="'/'+this.view_type+'/preview/'+props.row.examid+(props.row.pid? ('/'+props.row.pid) : '')" class="q-mx-md"
                 icon="visibility"
                 inline-label label="Preview">
          </q-btn>
          <q-btn :to="'/'+this.view_type+'/mock/'+props.row.examid+(props.row.pid? ('/'+props.row.pid) : '')" class="q-mx-md"
                 icon="fast_forward"
                 inline-label label="Mock"></q-btn>
        </q-td>

      </q-tr>
    </template>

  </q-table>
</template>

<script>
export default {
  name: "IndexTable",
  data() {
    return {
      selection: []
    }
  },
  props: {
    view_type: {
      type: String,
      required: true
    },
    cols: {
      type: JSON,
      required: true
    },
    rows: {
      type: JSON,
      required: true
    },
  },
  methods: {
    updateRows(row) {
      const index = this.selection.findIndex(item => item.examid === row.examid);
      if (index === -1) {
        this.selection.push(row);
      } else {
        this.selection.splice(index, 1);
      }
    }
  }
}
</script>

<style scoped>

</style>
