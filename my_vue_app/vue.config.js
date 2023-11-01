const { defineConfig } = require("@vue/cli-service");
const BundleTracker = require("webpack-bundle-tracker");
const path = require("path");

// vue.config.js
module.exports = defineConfig({
  publicPath: "/static/bundles/", // <-- Add this line
  configureWebpack: {
    plugins: [
      new BundleTracker({
        path: path.resolve(__dirname, "./"),
        filename: "webpack-stats.json",
      }),
    ],
  },
  outputDir: "../static/bundles/",
  transpileDependencies: true,
  pages: {
    verificationVue: "src/main.js",
    layerStructureFormVue: "src/layerStructure.js",
    formsetTableVue : "src/formsetTable.js"
  },
});
