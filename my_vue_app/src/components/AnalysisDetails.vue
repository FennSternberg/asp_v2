<template>
  <div class="form-page">
    <div class="col-lg-6 mx-auto">
      <h1>Analysis Details</h1>
      <BaseFormField
        fieldId="id_internal_contact"
        fieldLabel="Internal Contact"
        fieldType="vue3-select"
        :fieldValue="internal_contact"
        :fieldChoices="internalContactChoices"
        :errors="errors.internal_contact"
        @input="
          $store.commit('form/updateField', {
            field: 'internal_contact',
            value: $event,
          })
        "
      />

      <BaseFormField
        fieldId="id_jobname"
        fieldLabel="Job Name"
        fieldType="text"
        :fieldValue="jobname"
        :errors="errors.jobname"
        @input="
          $store.commit('form/updateField', {
            field: 'jobname',
            value: $event.target.value,
          })
        "
      />

      <BaseFormField
        fieldId="id_customer"
        fieldLabel="Customer"
        fieldType="text"
        :fieldValue="customer"
        :errors="errors.customer"
        @input="
          $store.commit('form/updateField', {
            field: 'customer',
            value: $event.target.value,
          })
        "
      />
    </div>
  </div>
</template>

<script>
import formMixin from "./formMixin";
import BaseFormField from "./BaseFormField.vue";
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState("form", ["jobname", "customer", "internal_contact"]),
  },
  mounted() {
    // Initialize internal_contact to currentUserId if it is not set
    if (this.internal_contact === null || this.internal_contact === "") {
      this.$store.commit("form/updateField", {
        field: "internal_contact",
        value: this.currentUserId,
      });
    }
  },
  mixins: [formMixin],
  components: {
    BaseFormField,
  },
  props: {
    internalContactChoices: Array,
    currentUserId: [String, Number, null],
    errors: Object,
  },
  methods: {
    validateThisForm() {
      const postData = {
        jobname: this.jobname,
        customer: this.customer,
        internal_contact: this.internal_contact,
      };
      this.validateForm("/ASP/validate_analysis_details/", postData);
    },
  },
};
</script>

<style scoped></style>
