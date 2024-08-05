<template>
  <q-layout view="hHh lpR fFf">
    <q-header class="text-center">
      <q-toolbar>
        <q-btn flat icon="home" round to="/"></q-btn>
        <q-toolbar-title>Settings</q-toolbar-title>
      </q-toolbar>
    </q-header>
    <q-page-container></q-page-container>

    <div class="q-pa-md">
      <q-form class="q-gutter-md" @submit="">
        <q-input v-model="dataPath" :rules="[ val => val && val.length > 0 || 'Please enter the DB path']" autocapitalize="off" autocomplete="off" autocorrect="off"
                 filled hint="Path to the data DB"
                 label="Data DB path *" lazy-rules spellcheck="false">
          <q-btn flat icon="folder" rounded @click="dataPathDialog"></q-btn>
        </q-input>

        <q-input v-model="recordsPath" :rules="[ val => val && val.length > 0 || 'Please enter the DB path']" autocapitalize="off" autocomplete="off" autocorrect="off"
                 filled hint="Path to the records DB"
                 label="Records DB path *" lazy-rules spellcheck="false">
          <q-btn flat icon="folder" rounded @click="recordsPathDialog"></q-btn>
        </q-input>

        <q-input v-model="audioPath" :rules="[ val => val && val.length > 0 || 'Please enter the DB path']" autocapitalize="off" autocomplete="off" autocorrect="off"
                 filled hint="Path to the audio folder"
                 label="Audio path *" lazy-rules spellcheck="false">
          <q-btn flat icon="folder" rounded @click="audioPathDialog"></q-btn>
        </q-input>
      </q-form>

    </div>
  </q-layout>
</template>

<script>
export default {
  name: "SettingsPage",

  data() {
    return {
      dataPath: '',
      recordsPath: '',
      audioPath: ''
    }
  },

  async created() {
    this.dataPath = await window.electron.getData();
    this.recordsPath = await window.electron.getRecords();
    this.audioPath = await window.electron.getAudio();
  },

  methods: {
    dataPathDialog() {
      window.electron.setData().then(result => {
        this.dataPath = result
      })
    },
    recordsPathDialog() {
      window.electron.setRecords().then(result => {
        this.recordsPath = result
      })
    },
    audioPathDialog() {
      window.electron.setAudio().then(result => {
        this.audioPath = result
      })
    }
  }
}
</script>
