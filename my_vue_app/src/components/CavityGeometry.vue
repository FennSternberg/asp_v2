<template>
  <div class="form-page">
    <h1>Cavity Geometry</h1>
    <div class="row">
      <div class="col-lg-6">
        <BaseFormField
          fieldId="id_depth"
          fieldLabel="Depth"
          fieldType="number"
          :fieldValue="depth"
          :errors="errors.depth"
          @input="
            $store.commit('form/updateField', {
              field: 'depth',
              value: $event.target.value,
            })
          "
        />

        <BaseFormField
          fieldId="id_wall_angle"
          fieldLabel="Wall Angle"
          fieldType="number"
          :fieldValue="wall_angle"
          :errors="errors.wall_angle"
          @input="
            $store.commit('form/updateField', {
              field: 'wall_angle',
              value: $event.target.value,
            })
          "
        />

        <BaseFormField
          fieldId="id_r"
          fieldLabel="r"
          fieldType="number"
          :fieldValue="r"
          :errors="errors.r"
          @input="
            $store.commit('form/updateField', {
              field: 'r',
              value: $event.target.value,
            })
          "
        />

        <BaseFormField
          v-show="selectedProfile !== 'profile2'"
          fieldId="id_rb"
          fieldLabel="Rb"
          fieldType="number"
          :fieldValue="rb"
          :errors="errors.rb"
          @input="
            $store.commit('form/updateField', {
              field: 'rb',
              value: $event.target.value,
            })
          "
        />

        <BaseFormField
          fieldId="id_rf"
          fieldLabel="Rf"
          fieldType="number"
          :fieldValue="rf"
          :errors="errors.rf"
          @input="
            $store.commit('form/updateField', {
              field: 'rf',
              value: $event.target.value,
            })
          "
        />
        <BaseFormField
          fieldId="inputChoice"
          fieldLabel="Choose input pair:"
          fieldType="select"
          :fieldValue="inputChoice"
          :fieldChoices="inputChoices"
          :errors="errors.inputChoice"
          @input="
            $store.commit('form/updateField', {
              field: 'inputChoice',
              value: $event.target.value,
            })
          "
        />

        <BaseFormField
          fieldId="id_w"
          fieldLabel="W"
          fieldType="number"
          :fieldValue="w"
          :errors="errors.w"
          :readonly="isC1C2ReadOnly"
          @input="
            $store.commit('form/updateField', {
              field: 'w',
              value: $event.target.value,
            })
          "
        />

        <BaseFormField
          fieldId="id_c1"
          fieldLabel="C1"
          fieldType="number"
          :fieldValue="c1"
          :errors="errors.c1"
          :readonly="isWLReadOnly"
          @input="
            $store.commit('form/updateField', {
              field: 'c1',
              value: $event.target.value,
            })
          "
        />

        <BaseFormField
          v-show="selectedShape !== 'round'"
          fieldId="id_l"
          fieldLabel="L"
          fieldType="number"
          :fieldValue="l"
          :errors="errors.l"
          :readonly="isC1C2ReadOnly"
          @input="
            $store.commit('form/updateField', {
              field: 'l',
              value: $event.target.value,
            })
          "
        />

        <BaseFormField
          v-show="selectedShape !== 'round'"
          fieldId="id_c2"
          fieldLabel="C2"
          fieldType="number"
          :fieldValue="c2"
          :errors="errors.c2"
          :readonly="isWLReadOnly"
          @input="
            $store.commit('form/updateField', {
              field: 'c2',
              value: $event.target.value,
            })
          "
        />
      </div>
      <div class="col-lg-6 justify-content-center">
        <div class="row">
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
        <div class="row">
          <div class="col-auto mx-auto mt-3">
            <button class="btn btn-info" @click="validateThisFormNoProgress">
              Sketch My Cavity
            </button>
          </div>
        </div>

        <div class="row">
          <svg
            class="mt-3 mb-3"
            :viewBox="roundviewBoxValues"
            :height="svgHeight"
            :width="svgWidth"
            xmlns="http://www.w3.org/2000/svg"
            ref="svgElement"
          >
            <polyline
              :points="roundPoints"
              fill="none"
              stroke="black"
              stroke-width="0.1"
            />
          </svg>
          <svg
            class="mt-3 mb-3"
            :viewBox="oblongviewBoxValues"
            :height="svgHeight"
            :width="svgWidth"
            xmlns="http://www.w3.org/2000/svg"
            ref="svgElement"
          >
            <polyline
              :points="oblongPoints"
              fill="none"
              stroke="black"
              stroke-width="0.1"
            />
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import BaseFormField from "./BaseFormField.vue";
import formMixin from "./formMixin";

export default {
  mixins: [formMixin],
  computed: {
    ...mapState("form", [
      "inputChoice",
      "w",
      "c1",
      "l",
      "c2",
      "depth",
      "wall_angle",
      "r",
      "rb",
      "rf",
      "selectedShape",
      "selectedProfile",
      "round_coordinates",
      "oblong_coordinates",
    ]),
    isC1C2ReadOnly() {
      return this.inputChoice === "C1C2";
    },
    isWLReadOnly() {
      return this.inputChoice === "WL";
    },
    roundPoints() {
      return this.getPoints(this.round_coordinates);
    },
    oblongPoints() {
      return this.getPoints(this.oblong_coordinates);
    },
    roundboundingBox() {
      return this.getboundingBox(this.round_coordinates);
    },
    oblongboundingBox() {
      return this.getboundingBox(this.oblong_coordinates);
    },
    roundviewBoxValues() {
      return this.getViewBoxValues(this.roundboundingBox);
    },
    oblongviewBoxValues() {
      return this.getViewBoxValues(this.oblongboundingBox);
    },
  },
  watch: {
    w() {
      if (this.isWLReadOnly) {
        this.updateLongFromShort();
      }
    },
    c1() {
      if (this.isC1C2ReadOnly) {
        this.updateShortFromLong();
      }
    },
    l() {
      if (this.isWLReadOnly) {
        this.updateLongFromShort();
      }
    },
    c2() {
      if (this.isC1C2ReadOnly) {
        this.updateShortFromLong();
      }
    },
    r() {
      if (this.isWLReadOnly) {
        this.updateLongFromShort();
      } else if (this.isC1C2ReadOnly) {
        this.updateShortFromLong();
      }
    },
    wall_angle() {
      if (this.isWLReadOnly) {
        this.updateLongFromShort();
      } else if (this.isC1C2ReadOnly) {
        this.updateShortFromLong();
      }
    },
  },
  components: {
    BaseFormField,
  },
  props: {
    errors: Object,
  },
  methods: {
    getPoints(coordinates) {
      if (coordinates) {
        return coordinates
          .map((point) => [point[0], -point[1] + this.svgHeight])
          .map((point) => point.join(","))
          .join(" ");
      } else {
        return [];
      }
    },
    getboundingBox(coordinates) {
      if (coordinates && coordinates.length > 0) {
        let minX = coordinates[0][0];
        let minY = -coordinates[0][1] + this.svgHeight;
        let maxX = coordinates[0][0];
        let maxY = -coordinates[0][1] + this.svgHeight;

        coordinates.forEach((point) => {
          minX = Math.min(minX, point[0]);
          minY = Math.min(minY, -point[1] + this.svgHeight);
          maxX = Math.max(maxX, point[0]);
          maxY = Math.max(maxY, -point[1] + this.svgHeight);
        });

        return {
          minX: minX,
          minY: minY,
          width: maxX - minX,
          height: maxY - minY,
        };
      } else {
        return null;
      }
    },
    getViewBoxValues(boundingBox) {
      if (boundingBox) {
        return `${boundingBox.minX} ${boundingBox.minY} ${boundingBox.width} ${boundingBox.height}`;
      } else {
        return "0 0 300 300";
      }
    },
    getPostData() {
      const postData = {
        w: this.w,
        c1: this.c1,
        l: this.l,
        c2: this.c2,
        depth: this.depth,
        wall_angle: this.wall_angle,
        r: this.r,
        rb: this.rb,
        rf: this.rf,
        profile: this.selectedProfile,
        shape: this.selectedShape,
      };
      console.log("Validate");
      console.log(postData);
      return postData;
    },

    async validateThisFormNoProgress() {
      const postData = this.getPostData();
      const response = await this.validateForm(
        "/ASP/validate_cavity_geometry/",
        postData,
        false
      );
      if (
        response.sketch_points &&
        response.sketch_points[0] &&
        response.sketch_points[0].length >= 2
      ) {
        this.$store.commit("form/updateField", {
          field: "round_coordinates",
          value: response.sketch_points[0],
        });
      }
      if (
        response.sketch_points &&
        response.sketch_points[1] &&
        response.sketch_points[1].length >= 2
      ) {
        this.$store.commit("form/updateField", {
          field: "oblong_coordinates",
          value: response.sketch_points[1],
        });
      }
    },
    async validateThisForm() {
      const postData = this.getPostData();
      const response = await this.validateForm(
        "/ASP/validate_cavity_geometry/",
        postData
      );
      if (
        response.sketch_points &&
        response.sketch_points[0] &&
        response.sketch_points[0].length >= 2
      ) {
        this.$store.commit("form/updateField", {
          field: "round_coordinates",
          value: response.sketch_points[0],
        });
      }

      if (
        response.sketch_points &&
        response.sketch_points[1] &&
        response.sketch_points[1].length >= 2
      ) {
        this.$store.commit("form/updateField", {
          field: "oblong_coordinates",
          value: response.sketch_points[1],
        });
      }
    },
    updateLongFromShort() {
      const calculatedC1 = this.calcLongFromShort(
        Number(this.w),
        Number(this.r),
        Number(this.wall_angle)
      );
      this.$store.commit("form/updateField", {
        field: "c1",
        value: calculatedC1,
      });
      const calculatedC2 = this.calcLongFromShort(
        Number(this.l),
        Number(this.r),
        Number(this.wall_angle)
      );
      this.$store.commit("form/updateField", {
        field: "c2",
        value: calculatedC2,
      });
    },
    updateShortFromLong() {
      const calculatedW = this.calcShortFromLong(
        Number(this.c1),
        Number(this.r),
        Number(this.wall_angle)
      );
      this.$store.commit("form/updateField", {
        field: "w",
        value: calculatedW,
      });
      const calculatedL = this.calcShortFromLong(
        Number(this.c2),
        Number(this.r),
        Number(this.wall_angle)
      );
      this.$store.commit("form/updateField", {
        field: "l",
        value: calculatedL,
      });
    },
    calcLongFromShort(W, r, wall_angle) {
      const radian_wall_angle =
        Math.PI / 4 - (0.5 * wall_angle * Math.PI) / 180;
      const C1 = W + 2 * r * Math.tan(radian_wall_angle);
      return Number(C1).toFixed(1);
    },
    calcShortFromLong(C1, r, wall_angle) {
      const radian_wall_angle =
        Math.PI / 4 - (0.5 * wall_angle * Math.PI) / 180;
      const W = C1 - 2 * r * Math.tan(radian_wall_angle);
      return Number(W).toFixed(1);
    },
  },

  data() {
    return {
      svgHeight: 150,
      svgWidth: 150,
      inputChoices: [
        { value: "WL", label: "W and L" },
        { value: "C1C2", label: "C1 and C2" },
      ],
    };
  },
};
</script>

<style scoped>
/* Styling for the images in the first row */
.cavity-image {
  max-width: 75%; /* sets the image width to half of its container */
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>
