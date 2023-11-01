<template>
  <div>
    <h1>Shape and Profile</h1>
    <div class="text-center">
      <BaseRadioGroup
        fieldId="shape"
        :fieldChoices="shapeChoices"
        :fieldValue="selectedShape"
        :fieldLabel="'Shape'"
        :errors="errors.shape"
        :useImage="true"
        @input="
          $store.commit('form/updateField', {
            field: 'selectedShape',
            value: $event,
          })
        "
      />

      <BaseRadioGroup
        fieldId="profile"
        :fieldLabel="'Profile'"
        :fieldChoices="profileChoices"
        :fieldValue="selectedProfile"
        :errors="errors.profile"
        :useImage="true"
        @input="
          $store.commit('form/updateField', {
            field: 'selectedProfile',
            value: $event,
          })
        "
      />
    </div>
  </div>
</template>

<script>
import BaseRadioGroup from "./BaseRadioGroup.vue";
import formMixin from "./formMixin";
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState("form", ["selectedShape", "selectedProfile"]),
  },
  mounted() {
    // Initialize to default values if they are null
    if (this.selectedShape === null) {
      // set your default value here if any
    }
    if (this.selectedProfile === null) {
      // set your default value here if any
    }
  },
  mixins: [formMixin],
  components: {
    BaseRadioGroup,
  },
  props: {
    shapeChoices: Array,
    profileChoices: Array,
    errors: Object,
  },
  methods: {
    validateThisForm() {
      const postData = {
        shape: this.selectedShape,
        profile: this.selectedProfile,
      };
      this.validateForm("/ASP/validate_shape_and_profile/", postData);
    },
  },
};
</script>

<style scoped>
/* Your CSS styling here */
</style>
