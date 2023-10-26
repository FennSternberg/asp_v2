import { createApp } from "vue";
import App from "./thermoforming-verification.vue";
import store from "./store";

const verificationVue = createApp(App);

verificationVue.use(store);

verificationVue.mount("#verificationVue");
