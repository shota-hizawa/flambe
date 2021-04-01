<template>
  <div class="component-wrapper">
    <el-button
      type="danger"
      icon="el-icon-delete"
      size="mini"
      @click="openDialog"
      plain
    >
      タスク削除
    </el-button>
    <el-dialog
      title="タスク削除"
      :visible.sync="isDialogShown"
      width="500px"
      :close-on-click-modal="false"
      :show-close="false"
      :close-on-press-escape="false"
    >
      タスク: {{ task.title }} を削除します。
      <div slot="footer" class="dialog-footer">
        <el-button
          class="form__button"
          type="primary"
          @click="executeDeleteTask"
          :loading="isExecuteButtonLoading"
          >実行</el-button
        >
        <el-button class="form__button" @click="isDialogShown = false"
          >キャンセル</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from "@vue/composition-api";
import apiInvoker from "@/api/ApiInvoker";
import { MessageBox } from "element-ui";
import Task from "@/models/Task";

type Props = {
  task: Task;
};

export default defineComponent({
  props: {
    task: {
      type: Object as PropType<Task>,
      required: true,
    },
  },
  setup(props: Props, { emit }) {
    const isDialogShown = ref<boolean>(false);
    const isExecuteButtonLoading = ref<boolean>(false);
    const openDialog = (): void => {
      isDialogShown.value = true;
    };

    /**
     * API実行
     */
    const executeDeleteTask = async (): Promise<void> => {
      try {
        await MessageBox.confirm("タスク削除を実行します。", "実行確認", {
          confirmButtonText: "実行",
          cancelButtonText: "戻る",
          type: "info",
        });
      } catch {
        return;
      }
      isExecuteButtonLoading.value = true;
      await apiInvoker.deleteTask(props.task.id);

      isExecuteButtonLoading.value = false;
      isDialogShown.value = false;
      emit("task-deleted");
    };

    return {
      isDialogShown,
      isExecuteButtonLoading,
      openDialog,
      executeDeleteTask,
    };
  },
});
</script>

<style lang="scss" scoped>
@import "src/styles/common-style-variables";
.component-wrapper {
  display: inline-block;
}

.form {
  &__button {
    width: $normal-button-size;
  }
}
</style>
