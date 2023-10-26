<template>
  <div class="progress-container">
    <div class="step-labels">
      <div
        v-for="(step, index) in stepLabels"
        :key="index"
        class="step-label-wrapper"
      >
        <div
          class="step-label"
          :class="{
            'bg-primary text-white': currentStep >= index + 1,
            'bg-success text-white': currentStep > index + 1,
          }"
        >
          <i class="fas fa-check" v-if="currentStep > index + 1"></i> {{ step }}
        </div>
        <div
          v-if="index < stepLabels.length - 1"
          class="connector"
          :class="{
            'bg-primary': currentStep >= index + 1,
            'bg-success': currentStep > index + 1,
          }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    currentStep: {
      type: Number,
      required: true,
    },
    stepLabels: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.progress-container {
  width: 100%;
}

.step-labels {
  display: flex;
  justify-content: center;
}

.step-label-wrapper {
  display: flex;
  align-items: center;
}

.connector {
  width: 180px;
  height: 4px;
  background-color: #adcbf1; /* Default color */
}

.step-label {
  z-index: 2;
  padding: 10px;
  margin: 0 0px;
  border-radius: 5px;
  transition: background-color 0.4s ease, color 0.4s ease;
  background-color: #adcbf1;
}
</style>
