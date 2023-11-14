<template>
  <div>
    <h1>Thermoforming Verification</h1>
    <ProgressBar :currentStep="currentStep" :stepLabels="stepLabels" />
    <div class="transition-container mt-3">
      <transition
        :enter-active-class="
          isNavigatingBackward
            ? 'reverse-fade-enter-active'
            : 'fade-enter-active'
        "
        :leave-active-class="
          isNavigatingBackward
            ? 'reverse-fade-leave-active'
            : 'fade-leave-active'
        "
        :enter-from-class="
          isNavigatingBackward ? 'reverse-fade-enter-from' : 'fade-enter-from'
        "
        :enter-to-class="
          isNavigatingBackward ? 'reverse-fade-enter-to' : 'fade-enter-to'
        "
        :leave-from-class="
          isNavigatingBackward ? 'reverse-fade-leave-from' : 'fade-leave-from'
        "
        :leave-to-class="
          isNavigatingBackward ? 'reverse-fade-leave-to' : 'fade-leave-to'
        "
        mode="out-in"
      >
        <div :key="currentStep">
          <div class="row">
            <div class="col-lg-10 mx-auto">
              <PlugParameters
                ref="plugParametersRef"
                @validationStatus="handleValidationStatus"
                v-if="currentStep === 1"
                :plugChoices="availablePlugs"
                :errors="errors"
              ></PlugParameters>
              <AnalysisDetails
                ref="analysisDetailsRef"
                @validationStatus="handleValidationStatus"
                v-if="currentStep === 2"
                :internalContactChoices="internalContactChoices"
                :currentUserId="currentUserId"
                :errors="errors"
              ></AnalysisDetails>
              <MaterialChoices
                ref="materialChoicesRef"
                @validationStatus="handleValidationStatus"
                v-if="currentStep === 3"
                :cavityMaterialChoices="cavityMaterialChoices"
                :lidMaterialChoices="lidMaterialChoices"
                :errors="errors"
              ></MaterialChoices>
              <ShapeAndProfile
                ref="shapeAndProfileRef"
                @validationStatus="handleValidationStatus"
                v-if="currentStep === 4"
                :shape-choices="shapeChoices"
                :profile-choices="profileChoices"
                :errors="errors"
              ></ShapeAndProfile>
              <CavityGeometry
                ref="cavityGeometryRef"
                @validationStatus="handleValidationStatus"
                v-if="currentStep === 5"
                :errors="errors"
              ></CavityGeometry>
              <ThermoformingConfirmation
                ref="dummyPageRef"
                v-if="currentStep === 6"
                :cavityMaterialChoices="cavityMaterialChoices"
                :lidMaterialChoices="lidMaterialChoices"
              ></ThermoformingConfirmation>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-6 mx-auto">
              <div class="mt-4 text-center">
                <button
                  @click="goToPreviousStep"
                  :hidden="currentStep === 1"
                  class="btn btn-secondary me-3"
                >
                  Previous
                </button>
                <button
                  @click="goToNextStep"
                  :hidden="currentStep === totalSteps"
                  class="btn btn-primary ms-3"
                >
                  Next
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import AnalysisDetails from "./components/AnalysisDetails.vue";
import ShapeAndProfile from "./components/ShapeAndProfile.vue";
import ThermoformingConfirmation from "./components/ThermoformingConfirmation.vue";
import ProgressBar from "./components/ProgressBar.vue";
import CavityGeometry from "./components/CavityGeometry.vue";
import MaterialChoices from "./components/MaterialChoices.vue";
import PlugParameters from "./components/PlugParameters.vue";

export default {
  components: {
    ProgressBar,
    AnalysisDetails,
    ShapeAndProfile,
    CavityGeometry,
    ThermoformingConfirmation,
    MaterialChoices,
    PlugParameters,
  },
  data() {
    return {
      internalContactChoices: window.internalContactChoicesFromDjango || [],
      currentUserId: window.currentUserIdFromDjango || null,
      cavityMaterialChoices: window.availableMaterialsFromDjango || [],
      lidMaterialChoices: window.availableLidsFromDjango || [],
      shapeChoices: window.shapeChoicesFromDjango || [],
      profileChoices: window.profileChoicesFromDjango || [],
      availablePlugs: window.availablePlugsFromDjango || [],
      currentStep: 1,
      totalSteps: 5,
      errors: {},
      isNavigatingBackward: false,
      stepLabels: [
        "Plug",
        "Analysis Details",
        "Material Choices",
        "Shape & Profile",
        "Cavity Geometry",
        "Confirmation",
      ],
    };
  },
  methods: {
    async goToNextStep() {
      const refNames = {
        1: "plugParametersRef",
        2: "analysisDetailsRef",
        3: "materialChoicesRef",
        4: "shapeAndProfileRef",
        5: "cavityGeometryRef",
        6: "thermoformingConfirmationRef",
      };
      this.isNavigatingBackward = false;
      const currentRef = this.$refs[refNames[this.currentStep]];
      if (currentRef && typeof currentRef.validateForm === "function") {
        currentRef.validateThisForm();
      }
    },
    handleValidationStatus(status, errors = {}, nextPage = true) {
      console.log(errors);
      if (status) {
        this.errors = {};
        if (nextPage) {
          if (this.currentStep < this.totalSteps) {
            this.currentStep += 1;
          }
        }
      } else {
        this.errors = errors;
      }
    },
    goToPreviousStep() {
      this.isNavigatingBackward = true;
      if (this.currentStep > 1) {
        this.currentStep -= 1;
      }
    },
  },
};
</script>
<style>
h1 {
  text-align: center;
}
</style>
<style scoped>
.transition-container {
  overflow-x: hidden;
}
.fade-enter-active,
.fade-leave-active,
.reverse-fade-enter-active,
.reverse-fade-leave-active {
  transition: transform 0.3s ease;
}
.fade-enter-from,
.reverse-fade-leave-to {
  transform: translateX(100%);
}
.fade-leave-to,
.reverse-fade-enter-from {
  transform: translateX(-100%);
}
.fade-enter-to,
.fade-leave-from,
.reverse-fade-enter-to,
.reverse-fade-leave-from {
  transform: translateX(0);
}
.form-page {
  padding: 20px;
  margin: 0 auto;
  border: 1px solid #e1e1e1;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}
</style>
