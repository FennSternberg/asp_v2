<template>
  <div class="form-page">
    <div class="col-lg-6 mx-auto">
      <h1>Material Selection</h1>
      <BaseFormField
        fieldId="id_cavity_material"
        fieldLabel="Cavity Material"
        fieldType="vue3-select-multiple"
        :fieldValue="cavity_materials"
        :fieldChoices="cavityMaterialChoices"
        :errors="errors.cavity_materials"
        @input="
          $store.commit('form/updateField', {
            field: 'cavity_materials',
            value: $event,
          })
        "
      />

      <BaseFormField
        fieldId="id_lid_material"
        fieldLabel="Lid Material"
        fieldType="vue3-select-multiple"
        :fieldValue="lid_materials"
        :fieldChoices="lidMaterialChoices"
        :errors="errors.lid_materials"
        @input="
          $store.commit('form/updateField', {
            field: 'lid_materials',
            value: $event,
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
    ...mapState("form", ["cavity_materials", "lid_materials"]),
  },
  mixins: [formMixin],
  components: {
    BaseFormField,
  },
  props: {
    cavityMaterialChoices: Array,
    lidMaterialChoices: Array,
    errors: Object,
  },
  methods: {
    validateThisForm() {
      const postData = {
        cavity_materials: this.cavity_materials,
        lid_materials: this.lid_materials,
      };
      console.log('fenn')
      console.log(this.cavity_materials)
      this.validateForm("/ASP/validate_material_details/", postData);
    },
  },
};
</script>
