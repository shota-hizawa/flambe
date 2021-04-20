<template>
  <div class="component-wrapper">
    <el-button
      type="danger"
      icon="el-icon-delete"
      size="mini"
      @click="openDialog"
      plain
    >
      アサイン削除
    </el-button>
    <el-dialog
      title="アサイン削除"
      :visible.sync="isDialogShown"
      width="500px"
      :close-on-click-modal="false"
      :show-close="false"
      :close-on-press-escape="false"
    >
      {{ task.title }}から{{ user.username }}のアサインを削除します。
      <div slot="footer" class="dialog-footer">
        <el-button
          class="form__button"
          type="primary"
          @click="executeRemoveTaskAssignment"
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
import TaskWithAssignees from "@/models/TaskWithAssignees";
import User from "@/models/User";

type Props = {
  task: TaskWithAssignees;
  user: User;
};

export default defineComponent({
  props: {
    task: {
      type: Object as PropType<TaskWithAssignees>,
      required: true,
    },
    user: {
      type: Object as PropType<User>,
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
    const executeRemoveTaskAssignment = async (): Promise<void> => {
      try {
        await MessageBox.confirm("アサイン削除を実行します。", "実行確認", {
          confirmButtonText: "実行",
          cancelButtonText: "戻る",
          type: "info",
        });
      } catch {
        return;
      }
      isExecuteButtonLoading.value = true;
      await apiInvoker.removeTaskAssignmentFromUser({
        taskId: props.task.id,
        userId: props.user.id,
      });

      isExecuteButtonLoading.value = false;
      isDialogShown.value = false;
      emit("task-assignment-removed");
    };

    return {
      isDialogShown,
      isExecuteButtonLoading,
      openDialog,
      executeRemoveTaskAssignment,
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
