import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";

Vue.use(VueRouter);

function loadView(viewName: string) {
  return () =>
    import(/* webpackChunkName: "view-[request]" */ `@/views/${viewName}.vue`);
}

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "UserView",
    component: loadView("UserView"),
  },
  {
    path: "/tasks",
    name: "TaskView",
    component: loadView("TaskView"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
