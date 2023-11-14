<template>
  <div>
    <label :for="fieldId" v-if="fieldLabel" class="form-label"
      >{{ fieldLabel }}
    </label>

    <!-- Checkbox Type -->
    <input
      v-if="fieldType === 'checkbox'"
      type="checkbox"
      :id="fieldId"
      class="form-check-input"
      :class="{ 'is-invalid': errors }"
      :checked="fieldValue"
      :disabled="readonly"
    />

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

    <!-- Vue3-Select Multiple -->
    <Vue3Select
      v-if="fieldType === 'vue3-select-multiple'"
      :id="fieldId"
      :options="fieldChoices"
      :class="{ 'is-invalid': errors }"
      :disabled="readonly"
      :reduce="(option) => option.value"
      :modelValue="fieldValue"
      @update:modelValue="handleSelectInput"
      :list-max-height="20"
      multiple
    />

    <!-- Slider -->
    <div v-if="fieldType === 'slider'">
      <vue-slider
        v-model="slider_value"
        :min="min_slider"
        :max="max_slider"
        :dotSize="20"
        :height="6"
        :processStyle="{
          backgroundColor: '#5bc0de',
        }"
        :tooltip="'always'"
        :enableCross="false"
        :class="{ 'is-invalid': errors }"
        @input="handleSliderChange"
      ></vue-slider>
    </div>

    <div class="invalid-feedback" v-if="errors">
      {{ errors[0] }}
    </div>
  </div>
</template>

<script>
import Vue3Select from "vue3-select";
import "vue3-select/dist/vue3-select.css";
import VueSlider from "@vueform/slider";
import "@vueform/slider/themes/default.css";

export default {
  data() {
    return {
      slider_value: [null, null],
    };
  },
  components: {
    Vue3Select,
    VueSlider,
  },
  props: {
    fieldId: String,
    fieldLabel: String,
    fieldType: String,
    fieldValue: [String, Number, Array],
    fieldChoices: Array,
    errors: Array,
    readonly: {
      type: Boolean,
      default: false,
    },
    min_slider: Number,
    max_slider: Number,
    min_value_slider: Number,
    max_value_slider: Number,
  },
  methods: {
    handleSelectInput(selectedValue) {
      this.$emit("input", selectedValue);
    },
    // This will be called after user has finished dragging the slider handle
    handleSliderChange(value) {
      this.$emit("input", value);
    },
  },
  mounted() {
    // Set the slider_value to the min and max values provided by props
    this.slider_value = [this.min_value_slider, this.max_value_slider];
  },
};
</script>
