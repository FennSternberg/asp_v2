export default {
  namespaced: true,
  state: {
    inputChoice: "WL",
    internal_contact: null,
    r: "0.5",
    plug_travel_min:"50",
    plug_travel_max:"85"
  },
  mutations: {
    updateField(state, payload) {
      state[payload.field] = payload.value;
    },
  },
};
