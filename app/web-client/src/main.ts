import Vue from "vue";
import App from "./App.vue";
import VueCompositionApi from "@vue/composition-api";
import router from "./router";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import locale from "element-ui/lib/locale";
import lang from "element-ui/lib/locale/lang/ja";
import "normalize.css";
import "./styles/element-customization.scss";

locale.use(lang);

Vue.config.productionTip = false;
Vue.use(ElementUI);
Vue.use(VueCompositionApi);

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
