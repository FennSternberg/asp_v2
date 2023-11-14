<template>
  <div class="form-page">
    <div class="col-lg-6 mx-auto">
      <h1>Plug</h1>
      <BaseFormField
        fieldId="id_include_plug"
        fieldLabel="Include Plug?"
        fieldType="checkbox"
        :fieldValue="include_plug"
        :errors="errors.include_plug"
        @input="
          $store.commit('form/updateField', {
            field: 'include_plug',
            value: $event.target.checked,
          })
        "
      />
      <div v-if="include_plug">
        <BaseFormField
          fieldId="id_plug_material"
          fieldLabel="Plug Material"
          fieldType="vue3-select"
          :fieldValue="plug_materials"
          :fieldChoices="plugChoices"
          :errors="errors.plug_material"
          @input="
            $store.commit('form/updateField', {
              field: 'plug_material',
              value: $event,
            })
          "
        />
        <BaseFormField
          fieldId="id_plug_width"
          fieldLabel="W"
          fieldType="number"
          :fieldValue="plug_width"
          :errors="errors.plug_width"
          :readonly="false"
          @input="
            $store.commit('form/updateField', {
              field: 'plug_width',
              value: $event.target.value,
            })
          "
        />
        <BaseFormField
          fieldId="id_plug_length"
          fieldLabel="L"
          fieldType="number"
          :fieldValue="plug_length"
          :errors="errors.plug_length"
          :readonly="false"
          @input="
            $store.commit('form/updateField', {
              field: 'plug_length',
              value: $event.target.value,
            })
          "
        />
        <BaseFormField
          fieldId="id_slider"
          fieldLabel="Plug Travel"
          fieldType="slider"
          :min_slider="0"
          :max_silder="100"
          :min_value_slider="plug_travel_min"
          :max_value_slider="plug_travel_max"
          :errors="errors.plug_travel"
          class="mt-3 mb-3"
          @input="update_travel_slider"
        />
        <BaseFormField
          fieldId="id_n_travel"
          fieldLabel="N Travel"
          fieldType="number"
          :fieldValue="plug_n_travel"
          :errors="errors.plug_n_travel"
          :readonly="false"
          @input="
            $store.commit('form/updateField', {
              field: 'plug_n_travel',
              value: $event.target.value,
            })
          "
        />
        <BaseFormField
          fieldId="id_plug_rb"
          fieldLabel="Rb"
          fieldType="number"
          :fieldValue="plug_rb"
          :errors="errors.plug_rb"
          :readonly="false"
          @input="
            $store.commit('form/updateField', {
              field: 'plug_rb',
              value: $event.target.value,
            })
          "
        />
        <BaseFormField
          fieldId="id_plug_rf"
          fieldLabel="Rf"
          fieldType="number"
          :fieldValue="plug_rf"
          :errors="errors.plug_rf"
          :readonly="false"
          @input="
            $store.commit('form/updateField', {
              field: 'plug_rf',
              value: $event.target.value,
            })
          "
        />
      </div>
    </div>
  </div>
</template>

<script>
import formMixin from "./formMixin";
import BaseFormField from "./BaseFormField.vue";
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState("form", [
      "include_plug",
      "plug_material",
      "plug_width",
      "plug_length",
      "plug_travel_min",
      "plug_travel_max",
      "plug_n_travel",
      "plug_rb",
      "plug_rf",
    ]),
  },
  mixins: [formMixin],
  components: {
    BaseFormField,
  },
  props: {
    plugChoices: Array,
    errors: Object,
  },
  methods: {
    validateThisForm() {
      const postData = {
        include_plug: this.include_plug,
        plug_material: this.plug_material,
        plug_width: this.plug_width,
        plug_length: this.plug_length,
        plug_travel_min: this.plug_travel_min,
        plug_travel_max: this.plug_travel_max,
        plug_n_travel: this.plug_n_travel,
        plug_rb: this.plug_rb,
        plug_rf: this.plug_rf,
      };
      this.validateForm("/ASP/validate_plug/", postData);
    },

    update_travel_slider(range_values) {
      this.$store.commit("form/updateField", {
        field: "plug_travel_min",
        value: range_values[0],
      });
      this.$store.commit("form/updateField", {
        field: "plug_travel_max",
        value: range_values[1],
      });
    },
  },
};
</script>
