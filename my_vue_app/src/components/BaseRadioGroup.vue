<template>
  <div :class="{ 'border border-danger': errors, 'p-2': errors }">
    <label :for="fieldId"
      ><b>{{ fieldLabel }}</b></label
    >
    <div :id="fieldId">
      <!-- Conditionally render if useImage is true -->
      <div v-if="useImage">
        <label
          v-for="(choice, index) in fieldChoices"
          :key="index"
          class="image-radio-label"
        >
          <input
            type="radio"
            :name="fieldId"
            :value="choice.value"
            :checked="fieldValue === choice.value"
            @change="$emit('input', $event.target.value)"
            class="image-radio"
          />

          <img :src="choice.path" :alt="choice.label" class="image-radio-img" />

          <div class="text-center">{{ choice.label }}</div>
        </label>
      </div>

      <!-- Fallback to default behavior if useImage is false -->
      <div v-else>
        <label v-for="(choice, index) in fieldChoices" :key="index">
          <input
            type="radio"
            :name="fieldId"
            :value="choice.value"
            :checked="fieldValue === choice.value"
            @change="$emit('input', $event.target.value)"
          />
          {{ choice.value }}
        </label>
      </div>
    </div>
    <p v-if="errors" class="text-danger">
      {{ errors[0] }}
    </p>
  </div>
</template>

<script>
export default {
  props: {
    fieldId: String,
    fieldLabel: String,
    fieldChoices: Array,
    useImage: Boolean,
    fieldValue: [String, Number],
    errors: Array,
  },
};
</script>

<style scoped>
.image-radio {
  display: none; /* Hide the default radio */
}

.image-radio-label {
  display: inline-block;
  cursor: pointer;
  margin-right: 20px; /* Add horizontal space between each image option */
}

.image-radio-img {
  width: 200px; /* Fixed width */
  /* height is automatically calculated to maintain aspect ratio */
  border: 1px solid gray;
  transition: all 0.3s;
}

/* When radio is selected, the image grows larger and changes border color */
.image-radio:checked + .image-radio-img {
  width: 300px; /* Fixed width when selected */
  /* height is automatically calculated to maintain aspect ratio */
  border: 3px solid blue;
}
</style>
