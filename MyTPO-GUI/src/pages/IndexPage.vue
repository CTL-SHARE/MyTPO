<template>
  <q-layout>
    <q-header class="text-center" elevated>
      <q-toolbar>
        <q-toolbar-title class="text-h6">Welcome to MyTPO!</q-toolbar-title>
        <q-btn-dropdown dense flat>
          <q-btn class="row" flat icon="format_list_bulleted" label="Records" no-caps to="/records"></q-btn>
          <q-btn class="row" flat icon="settings" label="Settings" no-caps to="/settings"></q-btn>
        </q-btn-dropdown>
      </q-toolbar>

    </q-header>

    <q-page-container>
      <q-page class="column justify-start">
        <div class="column col absolute-full q-pa-md">
          <q-dialog v-model="noDB" maximized persistent>
            <q-card>
              <q-card-section>
                <div class="text-h6">Error</div>
              </q-card-section>

              <q-card-section class="q-pt-none">
                No database located. Please fix in settings.
              </q-card-section>

              <q-card-actions align="right">
                <q-btn color="primary" flat label="Go to settings" to="/settings"/>
              </q-card-actions>
            </q-card>
          </q-dialog>

          <div class="q-pa-lg q-mb-lg">
            <q-tabs v-model="tab_main" active-color="primary" align="justify" class="text-grey"
                    indicator-color="primary"
                    no-caps>
              <q-tab icon="menu_book" label="Reading" name="reading"></q-tab>
              <q-tab icon="headphones" label="Listening" name="listening"></q-tab>
              <q-tab icon="mic" label="Speaking" name="speaking"></q-tab>
              <q-tab icon="edit_note" label="Writing" name="writing"></q-tab>
              <q-tab icon="monitor" label="Full-length Practice" name="full-length"></q-tab>
            </q-tabs>

            <q-tab-panels v-model="tab_main" animated>
              <q-tab-panel name="reading">
                <IndexTable :cols="read_cols" :rows="read_data" view_type="read"></IndexTable>
              </q-tab-panel>

              <q-tab-panel name="listening">
                <q-tabs v-model="tab_listen" active-color="secondary" align="justify" class="text-grey"
                        indicator-color="secondary"
                        inline-label no-caps>
                  <q-tab icon="forum" label="Conversation" name="conversation"></q-tab>
                  <q-tab icon="school" label="Lecture" name="lecture"></q-tab>
                </q-tabs>

                <q-tab-panels
                  v-model="tab_listen" animated swipeable>
                  <q-tab-panel name="conversation">
                    <IndexTable :cols="listen_cols" :rows="listen_conversation_data"
                                view_type="listen/conv"></IndexTable>
                  </q-tab-panel>

                  <q-tab-panel name="lecture">
                    <IndexTable :cols="listen_cols" :rows="listen_lecture_data" view_type="listen/lec"></IndexTable>
                  </q-tab-panel>

                </q-tab-panels>

              </q-tab-panel>


              <q-tab-panel name="speaking">
                <q-tabs v-model="tab_speak" active-color="secondary" align="justify" class="text-grey"
                        indicator-color="secondary"
                        inline-label no-caps>
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
                    <IndexTable :cols="speak_write_cols" :rows="speak_q1_data" view_type="speak/q1"></IndexTable>
                  </q-tab-panel>
                  <q-tab-panel name="q2">
                    <IndexTable :cols="speak_write_cols" :rows="speak_q2_data" view_type="speak/q2"></IndexTable>
                  </q-tab-panel>
                  <q-tab-panel name="q3">
                    <IndexTable :cols="speak_write_cols" :rows="speak_q3_data" view_type="speak/q3"></IndexTable>
                  </q-tab-panel>
                  <q-tab-panel name="q4">
                    <IndexTable :cols="speak_write_cols" :rows="speak_q4_data" view_type="speak/q4"></IndexTable>
                  </q-tab-panel>
                </q-tab-panels>
              </q-tab-panel>


              <q-tab-panel name="writing">
                <q-tabs v-model="tab_write" active-color="secondary" align="justify" class="text-grey"
                        indicator-color="secondary"
                        inline-label no-caps>
                  <q-tab icon="compare" label="Integrated" name="integrated"></q-tab>
                  <q-tab icon="group_add" label="Academic Discussion" name="discussion"></q-tab>
                </q-tabs>

                <q-tab-panels v-model="tab_write" animated swipeable>
                  <q-tab-panel name="integrated">
                    <IndexTable :cols="speak_write_cols" :rows="write_integrated_data"
                                view_type="write/integrated"></IndexTable>
                  </q-tab-panel>
                  <q-tab-panel name="discussion">
                    <IndexTable :cols="speak_write_cols" :rows="write_independent_data"
                                view_type="write/independent"></IndexTable>
                  </q-tab-panel>
                </q-tab-panels>

              </q-tab-panel>


              <q-tab-panel name="full-length">
                <div>Full-length Practice Content</div>
              </q-tab-panel>

            </q-tab-panels>

          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import {ref} from 'vue';
import IndexTable from 'src/components/IndexTable.vue';

// table data
const read_cols = [
  {name: 'caption', label: 'Title', field: 'caption', align: 'center'},
  {name: 'progress', label: 'Progress', field: 'progress', align: 'center'},
  {name: 'examid', label: 'ExamID', field: 'examid', align: 'center'},
  {name: 'pid', label: 'PassageID', field: 'pid', align: 'center'},
  {name: 'actions', label: '', field: 'actions', align: 'center'}
]

const listen_cols = [
  {name: 'caption', label: 'Title', field: 'caption', align: 'center'},
  {name: 'progress', label: 'Progress', field: 'progress', align: 'center'},
  {name: 'examid', label: 'ExamID', field: 'examid', align: 'center'},
  {name: 'audioid', label: 'AudioID', field: 'audioid', align: 'center'},
  {name: 'actions', label: '', field: 'actions', align: 'center'}
]

const speak_write_cols = [
  {name: 'caption', label: 'Title', field: 'caption', align: 'center'},
  {name: 'progress', label: 'Progress', field: 'progress', align: 'center'},
  {name: 'examid', label: 'ExamID', field: 'examid', align: 'center'},
  {name: 'actions', label: '', field: 'actions', align: 'center'}
]

export default {
  components: {
    IndexTable
  },

  data() {
    return {
      noDB: false,
      read_cols,
      read_data: [],
      listen_cols,
      listen_conversation_data: [],
      listen_lecture_data: [],
      speak_write_cols,
      speak_q1_data: [],
      speak_q2_data: [],
      speak_q3_data: [],
      speak_q4_data: [],
      write_independent_data: [],
      write_integrated_data: []
    }
  },

  setup() {
    return {
      tab_main: ref('reading'),
      tab_speak: ref('q1'),
      tab_listen: ref('conversation'),
      tab_write: ref('integrated'),
    };
  },

  async created() {
    const result = await window.electron.testDBConn();
    if (result[0] === false || result[1] === false || result[2] === false) {
      this.noDB = true
    } else {
      this.read_data = await window.electron.dataSQL('select distinct caption, examid, pid from reading order by examid, pid')
      this.listen_conversation_data = await window.electron.dataSQL('select distinct caption, examid, audioid from listening_conversation order by examid, audioid')
      this.listen_lecture_data = await window.electron.dataSQL('select distinct caption, examid, audioid from listening_lecture order by examid, audioid')
      this.speak_q1_data = await window.electron.dataSQL('select distinct caption, examid from speaking_q1 order by examid')
      this.speak_q2_data = await window.electron.dataSQL('select distinct caption, examid from speaking_q2 order by examid')
      this.speak_q3_data = await window.electron.dataSQL('select distinct caption, examid from speaking_q3 order by examid')
      this.speak_q4_data = await window.electron.dataSQL('select distinct caption, examid from speaking_q4 order by examid')
      this.write_independent_data = await window.electron.dataSQL('select distinct caption, examid from writing_independent order by examid')
      this.write_integrated_data = await window.electron.dataSQL('select distinct caption, examid from writing_integrated order by examid')
    }
  }
}
</script>
