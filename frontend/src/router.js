import {createRouter, createWebHistory} from "vue-router";
import App from "@/CommentSearch";
import CoLiBert from "@/CoLiBert";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Comment Search', component: App },
    { path: '/colibert', name: 'CoLiBERT Search', component: CoLiBert },
  ]
});


export default router;
