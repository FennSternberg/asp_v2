<template>
  <div>
    <div
      class="mb-3"
      v-for="(selectedMaterial, index) in selectedMaterials"
      :key="index"
    >
      <div class="d-flex align-items-center">
        <div class="col-2 text-end">
          <label class="me-2">Layer {{ index + 1 }}:</label>
        </div>
        <div class="col-7">
          <BaseFormField
            fieldId="material"
            fieldLabel=""
            fieldType="vue3-select"
            :fieldChoices="formattedMaterials"
            :fieldValue="selectedMaterials[index]"
            @input="updateSelectedMaterial(index, $event)"
          />
        </div>
        <div class="col-3">
          <button
            type="button"
            class="btn btn-danger"
            @click="removeMaterial(index)"
          >
            Remove
          </button>
        </div>
      </div>
    </div>
    <div class="mb-3">
      <button type="button" class="btn btn-success" @click="addMaterial">
        Add Material
      </button>
      <input
        type="hidden"
        name="ordered_material_ids"
        :value="selectedMaterials.join(',')"
      />
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import BaseFormField from "./components/BaseFormField.vue"; // Make sure the path is correct

export default {
  setup() {
    const allMaterials = ref(JSON.parse(window.all_materials_json || "[]"));
    const selectedMaterials = ref(
      JSON.parse(window.selected_materials_json || "[]")
    );

    function updateSelectedMaterial(index, newMaterialId) {
      selectedMaterials.value[index] = newMaterialId;
    }

    function addMaterial() {
      if (allMaterials.value.length > 0) {
        selectedMaterials.value.push(allMaterials.value[0].id);
      }
    }

    function removeMaterial(index) {
      selectedMaterials.value.splice(index, 1);
    }

    const formattedMaterials = allMaterials.value.map((material) => ({
      label: material.name,
      value: material.id,
    }));

    return {
      allMaterials,
      selectedMaterials,
      addMaterial,
      removeMaterial,
      updateSelectedMaterial,
      formattedMaterials,
    };
  },
  components: {
    BaseFormField,
  },
};
</script>
