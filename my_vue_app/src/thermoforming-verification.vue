<template>
  <div>
    <ProgressBar :currentStep="currentStep" :stepLabels="stepLabels" />

    <!-- Conditional rendering of steps -->
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
            <div class="col-lg-6 mx-auto">
              <AnalysisDetails
                ref="analysisDetailsRef"
                @validationStatus="handleValidationStatus"
                v-if="currentStep === 1"
                :internalContactChoices="internalContactChoices"
                :currentUserId="currentUserId"
                :errors="errors"
              ></AnalysisDetails>
              <ShapeAndProfile
                ref="shapeAndProfileRef"
                @validationStatus="handleValidationStatus"
                v-if="currentStep === 2"
                :shape-choices="shapeChoices"
                :profile-choices="profileChoices"
                :errors="errors"
              ></ShapeAndProfile>
              <CavityGeometry
                ref="cavityGeometryRef"
                @validationStatus="handleValidationStatus"
                v-if="currentStep === 3"
                :errors="errors"
              ></CavityGeometry>
              <DummyPage
                ref="dummyPageRef"
                v-if="currentStep === 4"
              ></DummyPage>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-6 mx-auto">
              <div class="mt-5 text-center">
                <!-- Navigation -->
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
import DummyPage from "./components/DummyPage.vue";
import ProgressBar from "./components/ProgressBar.vue";
import CavityGeometry from "./components/CavityGeometry.vue";

export default {
  components: { 
    ProgressBar,
    AnalysisDetails,
    ShapeAndProfile,
    CavityGeometry,
    DummyPage,
  },
  data() {
    return {
      internalContactChoices: window.internalContactChoicesFromDjango || [],
      currentUserId: window.currentUserIdFromDjango || null,
      shapeChoices: [
        {
          label: "Round",
          value: "round",
          path: "/static/images/cavity/round.png",
        },
        {
          label: "Oblong",
          value: "oblong",
          path: "/static/images/cavity/oblong.png",
        },
      ],
      profileChoices: [
        {
          label: "Profile 2",
          value: "profile2",
          path: "/static/images/cavity/profile2.png",
        },
        {
          label: "Profile 3",
          value: "profile3",
          path: "/static/images/cavity/profile3.png",
        },
      ],
      currentStep: 1,
      totalSteps: 4,
      errors: {},
      isNavigatingBackward: false,
      stepLabels: [
        "Analysis Details",
        "Shape & Profile",
        "Cavity Geometry",
        "Confirmation",
      ],
    };
  },
  methods: {
    async goToNextStep() {
      const refNames = {
        1: "analysisDetailsRef",
        2: "shapeAndProfileRef",
        3: "cavityGeometryRef",
        4: "dummyPageRef",
      };
      this.isNavigatingBackward = false;
      const currentRef = this.$refs[refNames[this.currentStep]];
      if (currentRef && typeof currentRef.validateForm === "function") {
        currentRef.validateThisForm();
      }
    },
    handleValidationStatus(status, errors = {}) {
      console.log(errors);
      if (status) {
        this.errors = {};
        if (this.currentStep < this.totalSteps) {
          this.currentStep += 1;
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
</style>
