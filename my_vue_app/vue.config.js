const { defineConfig } = require("@vue/cli-service");
const BundleTracker = require("webpack-bundle-tracker");
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const path = require("path");

// vue.config.js
module.exports = defineConfig({
  publicPath: "/static/bundles/",
  filenameHashing: true, 
  configureWebpack: {
    output: {
      filename: "[name].[hash].js", 
    },
    plugins: [
      new BundleTracker({
        path: path.resolve(__dirname, "./"),
        filename: "webpack-stats.json",
      }),
      new CleanWebpackPlugin({
        cleanStaleWebpackAssets: true, 
        protectWebpackAssets: false, 
      }),
    ],
  },
  outputDir: "../static/bundles/",
  transpileDependencies: true,
  pages: {
    verificationVue: "src/main.js",
    layerStructureFormVue: "src/layerStructure.js",
    formsetTableVue: "src/formsetTable.js",
  },
});
