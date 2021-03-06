<template>
  <div class="component-wrapper">
    <el-button type="primary" size="mini" @click="openDialog" plain>
      ステータス変更
    </el-button>
    <el-dialog
      title="タスクステータス変更"
      :visible.sync="isDialogShown"
      width="600px"
      :close-on-click-modal="false"
      :show-close="false"
      :close-on-press-escape="false"
    >
      <p>対象タスク: {{ task.title }}</p>
      <el-select
        v-model="form.status"
        placeholder="ステータス"
        style="width: 250px"
      >
        <el-option
          v-for="item in statuses"
          :key="item[0]"
          :label="item[1]"
          :value="item[0]"
        >
        </el-option>
      </el-select>

      <div slot="footer" class="dialog-footer">
        <el-button
          class="form__button"
          type="primary"
          @click="executeUpdateTask"
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
import { defineComponent, PropType, reactive, ref } from "@vue/composition-api";
import apiInvoker from "@/api/ApiInvoker";
import { MessageBox } from "element-ui";
import TaskWithAssignees from "@/models/TaskWithAssignees";
import { taskStatusDisplayNames } from "@/models/TaskStatus";

type Props = {
  task: TaskWithAssignees;
};

export default defineComponent({
  props: {
    task: {
      type: Object as PropType<TaskWithAssignees>,
      required: true,
    },
  },
  setup(props: Props, { emit }) {
    const isDialogShown = ref<boolean>(false);
    const isExecuteButtonLoading = ref<boolean>(false);

    /*
     * フォーム関連
     */
    const form = reactive({
      status: props.task.status,
    });
    const resetForm = (): void => {
      form.status = props.task.status;
    };
    const openDialog = (): void => {
      resetForm();
      isDialogShown.value = true;
    };
    const statuses = Array.from(taskStatusDisplayNames.entries());

    /**
     * API実行
     */
    const executeUpdateTask = async (): Promise<void> => {
      try {
        await MessageBox.confirm(
          "タスクのステータスを変更します。",
          "実行確認",
          {
            confirmButtonText: "実行",
            cancelButtonText: "戻る",
            type: "info",
          }
        );
      } catch {
        return;
      }
      isExecuteButtonLoading.value = true;
      await apiInvoker.updateTaskStatus(props.task.id, {
        newStatus: form.status,
      });

      isExecuteButtonLoading.value = false;
      isDialogShown.value = false;
      emit("task-status-updated");
    };

    return {
      isDialogShown,
      isExecuteButtonLoading,
      form,
      openDialog,
      statuses,
      executeUpdateTask,
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
