import {createRouter, createWebHistory} from 'vue-router';

const routes = [
  {
    path: '/',
    component: () => import('src/pages/IndexPage.vue'),
  },
  {
    path: '/read/preview/:examid/:pid',
    name: 'ReadingPreview',
    component: () => import('components/Reading/ReadingPreview.vue'),
    props: true
  },
  {
    path: '/read/mock/:examid/:pid',
    name: 'ReadingMock',
    component: () => import('components/Reading/ReadingMock.vue'),
    props: true
  },
  {
    path: '/listen/conv/preview/:examid/:pid',
    name: 'ListeningConversationPreview',
    component: () => import('components/Listening/ListeningConversationPreview.vue'),
    props: true
  },
  {
    path: '/listen/conv/mock/:examid/:pid',
    name: 'ListeningConversationMock',
    component: () => import('components/Listening/ListeningConversationMock.vue'),
    props: true
  },
  {
    path: '/listen/lec/preview/:examid/:pid',
    name: 'ListeningLecturePreview',
    component: () => import('components/Listening/ListeningLecturePreview.vue'),
    props: true
  },
  {
    path: '/listen/lec/mock/:examid/:pid',
    name: 'ListeningLectureMock',
    component: () => import('components/Listening/ListeningLectureMock.vue'),
    props: true
  },
  {
    path: '/speak/q1/preview/:examid',
    name: 'SpeakingQ1Preview',
    component: () => import('components/Speaking/SpeakingQ1Preview.vue'),
    props: true
  },
  {
    path: '/speak/q1/mock/:examid',
    name: 'SpeakingQ1Mock',
    component: () => import('components/Speaking/SpeakingQ1Mock.vue'),
    props: true
  },
  {
    path: '/speak/q2/preview/:examid',
    name: 'SpeakingQ2Preview',
    component: () => import('components/Speaking/SpeakingQ2Preview.vue'),
    props: true
  },
  {
    path: '/speak/q2/mock/:examid',
    name: 'SpeakingQ2Mock',
    component: () => import('components/Speaking/SpeakingQ2Mock.vue'),
    props: true
  },
  {
    path: '/speak/q3/preview/:examid',
    name: 'SpeakingQ3Preview',
    component: () => import('components/Speaking/SpeakingQ3Preview.vue'),
    props: true
  },
  {
    path: '/speak/q3/mock/:examid',
    name: 'SpeakingQ3Mock',
    component: () => import('components/Speaking/SpeakingQ3Mock.vue'),
    props: true
  },
  {
    path: '/speak/q4/preview/:examid',
    name: 'SpeakingQ4Preview',
    component: () => import('components/Speaking/SpeakingQ4Preview.vue'),
    props: true
  },
  {
    path: '/speak/q4/mock/:examid',
    name: 'SpeakingQ4Mock',
    component: () => import('components/Speaking/SpeakingQ4Mock.vue'),
    props: true
  },
  {
    path: '/write/integrated/preview/:examid',
    name: 'WritingIntegratedPreview',
    component: () => import('components/Writing/WritingIntegratedPreview.vue'),
    props: true
  },
  {
    path: '/write/integrated/mock/:examid',
    name: 'WritingIntegratedMock',
    component: () => import('components/Writing/WritingIntegratedMock.vue'),
    props: true
  },
  {
    path: '/write/independent/preview/:examid',
    name: 'WritingIndependentPreview',
    component: () => import('components/Writing/WritingIndependentPreview.vue'),
    props: true
  },
  {
    path: '/write/independent/mock/:examid',
    name: 'WritingIndependentMock',
    component: () => import('components/Writing/WritingIndependentMock.vue'),
    props: true
  },
  {
    path: '/records',
    name: "RecordsPage",
    component: () => import('src/pages/RecordsPage.vue')
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
