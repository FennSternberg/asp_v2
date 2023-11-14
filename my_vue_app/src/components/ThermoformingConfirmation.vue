<template>
  <div class="form-page">
    <h1>Confirmation</h1>
    <div class="row">
      <div class="col-lg-6">
        <div class="summary-group">
          <h2>Analysis Details</h2>
          <div class="summary-item">
            <strong>Internal Contact:</strong> {{ internal_contact }}
          </div>
          <div class="summary-item">
            <strong>Job Name:</strong> {{ jobname }}
          </div>
          <div class="summary-item">
            <strong>Customer:</strong> {{ customer }}
          </div>
        </div>
      </div>
      <div class="col-lg-6">
        <div class="summary-group">
          <h2>Material Choices</h2>
          <div class="summary-item">
            <strong>Cavity Materials:</strong>
            <ul>
              <li v-for="material in cavity_materials" :key="material">
                {{ getCavityMaterialLabel(material) }}
              </li>
            </ul>
          </div>
          <div class="summary-item">
            <strong>Lid Materials:</strong>
            <ul>
              <li v-for="material in lid_materials" :key="material">
                {{ getLidMaterialLabel(material) }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="summary-group">
        <h2>Cavity Geometry</h2>
        <div class="row">
          <div class="col-lg-6">
            <div class="summary-item">
              <strong>Shape:</strong> {{ selectedShape }}
            </div>
            <div class="summary-item">
              <strong>Shape:</strong> {{ selectedProfile }}
            </div>
            <div class="summary-item"><strong>W:</strong> {{ w }}</div>
            <div class="summary-item"><strong>C1:</strong> {{ c1 }}</div>
            <div v-if="selectedShape !== 'round'">
              <div class="summary-item"><strong>L:</strong> {{ l }}</div>
              <div class="summary-item"><strong>C2:</strong> {{ c2 }}</div>
            </div>
            <div class="summary-item"><strong>Depth:</strong> {{ depth }}</div>
            <div class="summary-item">
              <strong>Wall Angle:</strong> {{ wall_angle }}
            </div>
            <div class="summary-item"><strong>r:</strong> {{ r }}</div>
            <div class="summary-item"><strong>Rb:</strong> {{ rb }}</div>
            <div class="summary-item"><strong>Rf:</strong> {{ rf }}</div>
          </div>
          <div class="col-lg-6">
            <img
              class="cavity-image"
              :src="`/static/images/cavity/thermoveridims-${selectedProfile}-round.svg`"
              alt="Diagram of cavity dimensions"
            />
            <img
              v-if="selectedShape == 'oblong'"
              class="cavity-image"
              :src="`/static/images/cavity/thermoveridims-${selectedProfile}-oblong.svg`"
              alt="Diagram of cavity dimensions"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import formMixin from "./formMixin";
import { mapState } from "vuex";

export default {
  props: {
    cavityMaterialChoices: Array,
    lidMaterialChoices: Array,
  },
  computed: {
    ...mapState("form", [
      "internal_contact",
      "jobname",
      "customer",
      "cavity_materials",
      "lid_materials",
      "selectedShape",
      "selectedProfile",
      "w",
      "c1",
      "l",
      "c2",
      "depth",
      "wall_angle",
      "r",
      "rb",
      "rf",
    ]),
  },
  methods:{
  getCavityMaterialLabel(materialId) {
      const materialChoice = this.cavityMaterialChoices.find(choice => choice.value === materialId);
      return materialChoice ? materialChoice.label : `Material ID: ${materialId}`;
    },
    getLidMaterialLabel(materialId) {
      const materialChoice = this.lidMaterialChoices.find(choice => choice.value === materialId);
      return materialChoice ? materialChoice.label : `Material ID: ${materialId}`;
    },
  },
  mixins: [formMixin],
};
</script>

<style scoped>
h1 {
  border-bottom: 2px solid #e1e1e1;
  padding-bottom: 10px;
  margin-bottom: 20px;
  color: #333;
}

.summary-group {
  border: 1px solid #e1e1e1;
  border-radius: 5px;
  padding: 15px;
  margin-bottom: 20px;
  background-color: #f8f8f8;
}

.summary-group h2 {
  color: #555;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
  margin-bottom: 15px;
}

.summary-item {
  margin-bottom: 15px;
  color: #666;
}

.summary-item strong {
  color: #333;
}
.cavity-image {
  max-width: 75%; /* sets the image width to half of its container */
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>
