<template>
  <div>
    <label :for="fieldId" v-if="fieldLabel" class="form-label"
      >{{ fieldLabel }}
    </label>

    <!-- Text Type -->
    <input
      v-if="fieldType === 'text'"
      :type="fieldType"
      :id="fieldId"
      class="form-control"
      :class="{ 'is-invalid': errors }"
      :value="fieldValue"
      :readonly="readonly"
    />

    <!-- Number Type -->
    <input
      v-if="fieldType === 'number'"
      :type="fieldType"
      :id="fieldId"
      class="form-control"
      :class="{ 'is-invalid': errors }"
      :step="any"
      :value="fieldValue"
      :readonly="readonly"
    />

    <!-- Select Type -->
    <select
      v-if="fieldType === 'select'"
      :id="fieldId"
      class="form-select"
      :class="{ 'is-invalid': errors }"
      :value="fieldValue"
      :disabled="readonly"
    >
      <option
        v-for="(choice, index) in fieldChoices"
        :key="index"
        :value="choice.value"
      >
        {{ choice.label }}
      </option>
    </select>

    <!-- Vue3-Select -->

    <Vue3Select
      v-if="fieldType === 'vue3-select'"
      :id="fieldId"
      :options="fieldChoices"
      :class="{ 'is-invalid': errors }"
      :disabled="readonly"
      :reduce="(option) => option.value"
      :modelValue="fieldValue"
      @update:modelValue="handleSelectInput"
      :list-max-height="20"
    />

    <!-- Error Messages -->
    <div class="invalid-feedback" v-if="errors">
      {{ errors[0] }}
    </div>
  </div>
</template>

<script>
import Vue3Select from "vue3-select";
import "vue3-select/dist/vue3-select.css";

export default {
  components: {
    Vue3Select,
  },
  props: {
    fieldId: String,
    fieldLabel: String,
    fieldType: String,
    fieldValue: [String, Number],
    fieldChoices: Array,
    errors: Array,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    handleSelectInput(selectedValue) {
      this.$emit("input", selectedValue);
    },
  },
};
</script>
