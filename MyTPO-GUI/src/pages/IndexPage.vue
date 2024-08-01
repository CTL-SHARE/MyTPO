<template>
  <q-layout view="hHh lpR fFf">
    <q-header class="text-h2 text-center q-pa-xl q-mb-xl">
      <div class="q-mt-lg q-mb-lg flex items-center justify-center" style="height: 100%;">
        Welcome to MyTPO!
      </div>
    </q-header>

    <q-page-container></q-page-container>

    <div align="right">
      <q-btn class="q-ma-sm" icon="format_list_bulleted" label="Records" to="/records"></q-btn>
    </div>

    <div class="q-pa-lg q-mb-lg">
      <q-tabs v-model="tab_main" active-color="primary" align="justify" class="text-grey" indicator-color="primary">
        <q-tab icon="menu_book" label="Reading" name="reading"></q-tab>
        <q-tab icon="headphones" label="Listening" name="listening"></q-tab>
        <q-tab icon="mic" label="Speaking" name="speaking"></q-tab>
        <q-tab icon="edit_note" label="Writing" name="writing"></q-tab>
        <q-tab icon="monitor" label="Full-length Practice" name="full-length"></q-tab>
      </q-tabs>

      <q-tab-panels v-model="tab_main" animated>
        <q-tab-panel name="reading">
          <IndexTable :cols="par_2_cols" :rows="par_2_rows" view_type="read"></IndexTable>
        </q-tab-panel>

        <q-tab-panel name="listening">
          <q-tabs v-model="tab_listen" active-color="secondary" align="justify" class="text-grey"
                  indicator-color="secondary"
                  inline-label>
            <q-tab icon="forum" label="Conversation" name="conversation"></q-tab>
            <q-tab icon="school" label="Lecture" name="lecture"></q-tab>
          </q-tabs>

          <q-tab-panels
            v-model="tab_listen" animated swipeable>
            <q-tab-panel name="conversation">
              <IndexTable :cols="par_2_cols" :rows="par_2_rows" view_type="listen/conv"></IndexTable>
            </q-tab-panel>

            <q-tab-panel name="lecture">
              <IndexTable :cols="par_2_cols" :rows="par_2_rows" view_type="listen/lec"></IndexTable>
            </q-tab-panel>

          </q-tab-panels>

        </q-tab-panel>


        <q-tab-panel name="speaking">
          <q-tabs v-model="tab_speak" active-color="secondary" align="justify" class="text-grey"
                  indicator-color="secondary"
                  inline-label>
            <q-tab label="Task1" name="q1"></q-tab>
            <q-tab label="Task2" name="q2"></q-tab>
            <q-tab label="Task3" name="q3"></q-tab>
            <q-tab label="Task4" name="q4"></q-tab>
          </q-tabs>

          <q-tab-panels
            v-model="tab_speak"
            animated
            swipeable>
            <q-tab-panel name="q1">
              <IndexTable :cols="par_1_cols" :rows="par_1_rows" view_type="speak/q1"></IndexTable>
            </q-tab-panel>
            <q-tab-panel name="q2">
              <IndexTable :cols="par_1_cols" :rows="par_1_rows" view_type="speak/q2"></IndexTable>
            </q-tab-panel>
            <q-tab-panel name="q3">
              <IndexTable :cols="par_1_cols" :rows="par_1_rows" view_type="speak/q3"></IndexTable>
            </q-tab-panel>
            <q-tab-panel name="q4">
              <IndexTable :cols="par_1_cols" :rows="par_1_rows" view_type="speak/q4"></IndexTable>
            </q-tab-panel>
          </q-tab-panels>
        </q-tab-panel>


        <q-tab-panel name="writing">
          <q-tabs v-model="tab_write" active-color="secondary" align="justify" class="text-grey"
                  indicator-color="secondary"
                  inline-label>
            <q-tab icon="compare" label="Integrated" name="integrated"></q-tab>
            <q-tab icon="group_add" label="Class Discussion" name="discussion"></q-tab>
          </q-tabs>

          <q-tab-panels v-model="tab_write" animated swipeable>
            <q-tab-panel name="integrated">
              <IndexTable :cols="par_1_cols" :rows="par_1_rows" view_type="write/integrated"></IndexTable>
            </q-tab-panel>
            <q-tab-panel name="discussion">
              <IndexTable :cols="par_1_cols" :rows="par_1_rows" view_type="write/independent"></IndexTable>
            </q-tab-panel>
          </q-tab-panels>

        </q-tab-panel>


        <q-tab-panel name="full-length">
          <div>Full-length Practice Content</div>
        </q-tab-panel>

      </q-tab-panels>

    </div>
  </q-layout>
</template>

<script>
import {ref} from 'vue';
import IndexTable from 'src/components/IndexTable.vue';

// debug only
const par_2_cols = [
  {name: 'title', label: 'Title', field: 'title', align: 'center'},
  {name: 'progress', label: 'Progress', field: 'progress', align: 'center'},
  {name: 'examid', label: 'ExamID', field: 'examid', align: 'center'},
  {name: 'pid', label: 'PassageID', field: 'pid', align: 'center'},
  {name: 'actions', label: '', field: 'actions', align: 'center'}
]
const par_2_rows = [
  {title: 'test title 1', examid: '1', pid: '123', finish: 12, full: 14},
  {title: 'test title 2', examid: '2', pid: '123', finish: 12, full: 14},
  {title: 'test title 3', examid: '3', pid: '123', finish: 12, full: 14},
  {title: 'test title 4', examid: '4', pid: '123', finish: 12, full: 14},
  {title: 'test title 5', examid: '5', pid: '123', finish: 3, full: 5},
  {title: 'test title 6', examid: '6', pid: '123', finish: 12, full: 14},
  {title: 'test title 7', examid: '7', pid: '123', finish: 12, full: 14},
  {title: 'test title 8', examid: '8', pid: '321', finish: 0, full: 10},
  {title: 'test title 9', examid: '9', pid: '321', finish: 0, full: 10},
  {title: 'test title 10', examid: '10', pid: '321', finish: 0, full: 10},
]

const par_1_cols = [
  {name: 'title', label: 'Title', field: 'title', align: 'center'},
  {name: 'progress', label: 'Progress', field: 'progress', align: 'center'},
  {name: 'examid', label: 'ExamID', field: 'examid', align: 'center'},
  {name: 'actions', label: '', field: 'actions', align: 'center'}
]

const par_1_rows = [
  {title: 'write 1', examid: '1', finish: 1, full: 1},
  {title: 'write 2', examid: '2', finish: 0, full: 1},
]

export default {
  components: {
    IndexTable
  },
  setup() {
    return {
      tab_main: ref('reading'),
      tab_speak: ref('q1'),
      tab_listen: ref('conversation'),
      tab_write: ref('integrated'),
      par_2_rows,
      par_2_cols,
      par_1_rows,
      par_1_cols,
    };
  },
}
</script>
