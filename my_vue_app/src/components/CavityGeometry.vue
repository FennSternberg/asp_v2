<template>
  <div>
    <h1>Cavity Geometry</h1>

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
    ]),
    isC1C2ReadOnly() {
      return this.inputChoice === "C1C2";
    },
    isWLReadOnly() {
      return this.inputChoice === "WL";
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
    validateThisForm() {
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
      this.validateForm("/validate_cavity_geometry/", postData);
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
      inputChoices: [
        { value: "WL", label: "W and L" },
        { value: "C1C2", label: "C1 and C2" },
      ],
    };
  },
};
</script>

<style scoped>
/* Your CSS styling here */
</style>
