// src/store/modules/form.js

export default {
  namespaced: true,
  state: {
    inputChoice: "WL",
    internal_contact: null,
    r: "0.5",
  },
  mutations: {
    updateField(state, payload) {
      state[payload.field] = payload.value;
    },
  },
  // ... potentially some actions or getters
};