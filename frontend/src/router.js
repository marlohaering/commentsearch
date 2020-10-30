import {createRouter, createWebHistory} from "vue-router";
import App from "@/CommentSearch";
import CoLiBert from "@/CoLiBert";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: process.env.VUE_APP_PUBLIC_ROOT_PATH, name: 'Comment Search', component: App },
    { path: `${process.env.VUE_APP_PUBLIC_ROOT_PATH}/colibert`, name: 'CoLiBERT Search', component: CoLiBert },
  ]
});


export default router;
