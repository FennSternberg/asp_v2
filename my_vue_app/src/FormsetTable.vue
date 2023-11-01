<template>
  <div class="mb-3">
    <div v-if="uploadExcelFlag" class="row align-items-center mb-3">
      <div class="col-8">
        <input
          type="file"
          ref="excelFile"
          class="form-control"
          accept=".xlsx"
        />
      </div>
      <div class="col-4 text-end">
        <button type="button" class="btn btn-secondary" @click="parseExcelFile">
          Upload Excel
        </button>
      </div>
    </div>

    <!-- The formset and table -->
    <input
      type="hidden"
      :id="`id_${formsetName}-TOTAL_FORMS`"
      v-model="totalForms"
    />
    <table class="table">
      <thead>
        <tr>
          <th></th>
          <th v-for="(field, index) in fields" :key="`field-${index}`">
            {{ field.label }} <span v-if="field.unit">({{ field.unit }})</span>
          </th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(point, index) in points"
          v-show="!point.is_deleted"
          :key="`point-${index}`"
        >
          <td>
            <input
              type="hidden"
              :name="`${formsetName}-${index}-id`"
              v-model="point.id"
            />
            <input
              type="hidden"
              :name="`${formsetName}-${index}-DELETE`"
              v-model="point.is_deleted"
            />
          </td>
          <td
            v-for="(field, fieldIndex) in fields"
            :key="`point-${index}-field-${fieldIndex}`"
          >
            <input
              :required="isFieldRequired(field, point)"
              :type="field.type"
              :name="`${formsetName}-${index}-${field.field}`"
              class="form-control"
              :step="field.step"
              v-model="point[field.field]"
            />
          </td>

          <td>
            <button
              type="button"
              class="btn btn-danger"
              @click="removePoint(index)"
              v-if="points.length > 1"
            >
              Remove
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <button type="button" class="btn btn-secondary" @click="addPoint">
      Add More
    </button>
    <hr />
  </div>
</template>

<script>
export default {
  data() {
    return {
      uploadExcelFlag: true,
      totalForms: 0, // Initialize as 0, we'll update it
      // You can populate these fields from the backend or props
      fields: window.formset_fields,
      formsetName: window.formsetName,
      points: window.points,
    };
  },
  methods: {
    parseExcelFile() {
      const fileInput = this.$refs.excelFile;
      const file = fileInput.files[0];
      if (!file) {
        alert("Please select a file");
        return;
      }

      const reader = new FileReader();
      reader.onload = (event) => {
        // Import XLSX inside the method
        const XLSX = require("xlsx");

        const data = event.target.result;
        const workbook = XLSX.read(data, { type: "binary" });
        const firstSheet = workbook.SheetNames[0];
        const sheetData = XLSX.utils.sheet_to_json(workbook.Sheets[firstSheet]);

        this.points = sheetData.map((row) => {
          const point = { is_deleted: false };
          this.fields.forEach((field) => {
            const fieldName = field.field;
            point[fieldName] = row[fieldName];
          });
          return point;
        });
        this.updateTotalForms();
      };
      reader.readAsBinaryString(file);
    },
    isFieldRequired(field, point) {
      return field.required === "true" && !point.is_deleted;
    },
    updateTotalForms() {
      this.totalForms = this.points.length;
    },
    addPoint() {
      const newPoint = { is_deleted: false };
      this.fields.forEach((field) => {
        newPoint[field.field] = "";
      });
      this.points.push(newPoint);
      this.updateTotalForms();
    },
    removePoint(index) {
      this.points[index].is_deleted = true;
      this.updateTotalForms();
    },
  },
  mounted() {
    this.updateTotalForms();
  },
};
</script>

<style scoped>
/* Your styles here */
</style>
