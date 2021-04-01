<template>
  <div id="app">
    <el-container class="container">
      <el-aside class="container__aside" :width="sidebarWidth">
        <sidebar @handleSidebarCollapse="onHandleCollapse"></sidebar>
      </el-aside>
      <el-container>
        <el-main class="main">
          <router-view v-if="isMounted" />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from "@vue/composition-api";
import Sidebar from "@/components/Sidebar.vue";

export default defineComponent({
  components: {
    Sidebar,
  },
  setup() {
    /*
     * サイドバーの設定
     */
    const sidebarWidth = ref<string>("300px");
    const onHandleCollapse = (isSidebarCollapse: boolean): void => {
      sidebarWidth.value = isSidebarCollapse ? "64px" : "300px";
    };

    /*
     * ライフサイクルフック
     * App.vueのマウントが完了されるまで、ルーターコンポーネントのレンダリングを実行しないように制御している
     */
    const isMounted = ref<boolean>(false);
    onMounted(async () => {
      isMounted.value = true;
    });

    return {
      isMounted,
      sidebarWidth,
      onHandleCollapse,
    };
  },
});
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Noto+Sans+JP&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Lato&display=swap");

#app {
  font-family: "Lato", "Noto Sans JP", "ヒラギノ角ゴ ProN",
    "Hiragino Kaku Gothic ProN", "メイリオ", Meiryo, sans-serif;
}
</style>

<style lang="scss" scoped>
.container {
  height: 100vh;
}

.main {
  min-width: 900px;
}
</style>
