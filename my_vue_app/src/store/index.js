import { createStore } from "vuex";
import form from "./modules/form"; // Import the form module

export default createStore({
  modules: {
    form, // Include the form module
  },
});
