<template>
  <div class="component-wrapper">
    <el-menu
      class="sidebar"
      default-active="/"
      :collapse="isSidebarCollapse"
      :collapse-transition="false"
      router
    >
      <el-menu-item @click="handleSidebarCollapse">
        <div style="float: right">
          <el-button
            v-show="!isSidebarCollapse"
            icon="el-icon-s-fold"
            type="text"
          ></el-button>
          <el-button
            v-show="isSidebarCollapse"
            icon="el-icon-s-unfold"
            type="text"
          ></el-button>
        </div>
      </el-menu-item>
      <el-menu-item index="/">
        <i class="el-icon-user"></i>
        <span>ユーザ</span>
      </el-menu-item>
      <el-menu-item index="/tasks">
        <i class="el-icon-s-management"></i>
        <span>タスク</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, SetupContext } from "@vue/composition-api";

export default defineComponent({
  setup(_, context: SetupContext) {
    /*
     * 折り畳み関連処理
     */
    const isSidebarCollapse = ref<boolean>(false);
    const handleSidebarCollapse = (): void => {
      isSidebarCollapse.value = !isSidebarCollapse.value;
      context.emit("handleSidebarCollapse", isSidebarCollapse.value);
    };

    return {
      isSidebarCollapse,
      handleSidebarCollapse,
    };
  },
});
</script>

<style lang="scss" scoped>
.component-wrapper {
  height: 100%;
}

.sidebar {
  height: 100%;
}
</style>
