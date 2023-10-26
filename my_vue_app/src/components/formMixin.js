// formMixin.js
export default {
  methods: {
    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },
    async validateForm(url, postData) {
      const csrftoken = this.getCookie("csrftoken");

      try {
        const response = await fetch(url, {
          method: "POST",
          body: JSON.stringify(postData),
          headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrftoken,
          },
        });

        console.log(JSON.stringify(postData));
        console.log(response);
        const jsonResponse = await response.json();
        if (jsonResponse.status === "success") {
          this.$emit("validationStatus", true);
          // Check if "updated_data" is present in jsonResponse
          if ("updated_data" in jsonResponse) {
            // Update Vuex state using the generic `updateField` mutation
            for (const [key, value] of Object.entries(
              jsonResponse.updated_data
            )) {
              this.$store.commit("form/updateField", {
                field: key,
                value: value,
              });
            }
          }
        } else {
          this.$emit("validationStatus", false, jsonResponse.errors);
        }
      } catch (error) {
        console.error("Error validating the form: ", error);
        this.$emit("validationStatus", false, {});
      }
    },
  },
};
