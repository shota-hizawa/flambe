module.exports = {
  devServer: {
    port: 9000,
  },
  outputDir: `dist/${process.env.VUE_APP_ENV_NAME}`,
  pages: {
    index: {
      entry: "src/main.ts",
      title: process.env.VUE_APP_TITLE,
    },
  },
};
