import {createRouter, createWebHistory} from 'vue-router';
import IndexPage from "src/pages/IndexPage.vue";

import ReadingPreview from 'components/Reading/ReadingPreview.vue';
import ReadingMock from 'components/Reading/ReadingMock.vue';

import ListeningConversationPreview from "components/Listening/ListeningConversationPreview.vue";
import ListeningConversationMock from "components/Listening/ListeningConversationMock.vue";
import ListeningLecturePreview from "components/Listening/ListeningLecturePreview.vue";
import ListeningLectureMock from "components/Listening/ListeningLectureMock.vue";

import SpeakingQ1Preview from "components/Speaking/SpeakingQ1Preview.vue";
import SpeakingQ1Mock from "components/Speaking/SpeakingQ1Mock.vue";
import SpeakingQ2Preview from "components/Speaking/SpeakingQ2Preview.vue";
import SpeakingQ2Mock from "components/Speaking/SpeakingQ2Mock.vue";
import SpeakingQ3Preview from "components/Speaking/SpeakingQ3Preview.vue";
import SpeakingQ3Mock from "components/Speaking/SpeakingQ3Mock.vue";
import SpeakingQ4Preview from "components/Speaking/SpeakingQ4Preview.vue";
import SpeakingQ4Mock from "components/Speaking/SpeakingQ4Mock.vue";

import WritingIntegratedPreview from "components/Writing/WritingIntegratedPreview.vue";
import WritingIndependentMock from "components/Writing/WritingIndependentMock.vue";
import WritingIndependentPreview from "components/Writing/WritingIndependentPreview.vue";
import WritingIntegratedMock from "components/Writing/WritingIntegratedMock.vue";

import RecordsPage from 'src/pages/RecordsPage.vue';

const routes = [
  {
    path: '/',
    component: IndexPage,
  },
  {
    path: '/read/preview/:examid/:pid',
    name: 'ReadingPreiew',
    component: ReadingPreview,
    props: true
  },
  {
    path: '/read/mock/:examid/:pid',
    name: 'ReadingMock',
    component: ReadingMock,
    props: true
  },
  {
    path: '/listen/conv/preview/:examid/:pid',
    name: 'ListeningConversationPreview',
    component: ListeningConversationPreview,
    props: true
  },
  {
    path: '/listen/conv/mock/:examid/:pid',
    name: 'ListeningConversationMock',
    component: ListeningConversationMock,
    props: true
  },
  {
    path: '/listen/lec/preview/:examid/:pid',
    name: 'ListeningLecturePreview',
    component: ListeningLecturePreview,
    props: true
  },
  {
    path: '/listen/lec/mock/:examid/:pid',
    name: 'ListeningLectureMock',
    component: ListeningLectureMock,
    props: true
  },
  {
    path: '/speak/q1/preview/:examid',
    name: 'SpeakingQ1Preview',
    component: SpeakingQ1Preview,
    props: true
  },
  {
    path: '/speak/q1/mock/:examid',
    name: 'SpeakingQ1Mock',
    component: SpeakingQ1Mock,
    props: true
  },
  {
    path: '/speak/q2/preview/:examid',
    name: 'SpeakingQ2Preview',
    component: SpeakingQ2Preview,
    props: true
  },
  {
    path: '/speak/q2/mock/:examid',
    name: 'SpeakingQ2Mock',
    component: SpeakingQ2Mock,
    props: true
  },
  {
    path: '/speak/q3/preview/:examid',
    name: 'SpeakingQ3Preview',
    component: SpeakingQ3Preview,
    props: true
  },
  {
    path: '/speak/q3/mock/:examid',
    name: 'SpeakingQ3Mock',
    component: SpeakingQ3Mock,
    props: true
  },
  {
    path: '/speak/q4/preview/:examid',
    name: 'SpeakingQ4Preview',
    component: SpeakingQ4Preview,
    props: true
  },
  {
    path: '/speak/q4/mock/:examid',
    name: 'SpeakingQ4Mock',
    component: SpeakingQ4Mock,
    props: true
  },
  {
    path: '/write/integrated/preview/:examid',
    name: 'WritingIntegratedPreview',
    component: WritingIntegratedPreview,
    props: true
  },
  {
    path: '/write/integrated/mock/:examid',
    name: 'WritingIntegratedMock',
    component: WritingIntegratedMock,
    props: true
  },
  {
    path: '/write/independent/preview/:examid',
    name: 'WritingIndependentPreview',
    component: WritingIndependentPreview,
    props: true
  },
  {
    path: '/write/independent/mock/:examid',
    name: 'WritingIndependentMock',
    component: WritingIndependentMock,
    props: true
  },
  {
    path: '/records',
    name: "RecordsPage",
    component: RecordsPage
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
