<template>
  <div class="component-wrapper">
    <el-button type="primary" size="mini" @click="openDialog" plain>
      優先度変更
    </el-button>
    <el-dialog
      title="タスク優先度変更"
      :visible.sync="isDialogShown"
      width="600px"
      :close-on-click-modal="false"
      :show-close="false"
      :close-on-press-escape="false"
    >
      <p>対象タスク: {{ task.title }}</p>
      <el-select
        v-model="form.priority"
        placeholder="優先度"
        style="width: 250px"
      >
        <el-option
          v-for="item in priorities"
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
import { taskPriorityDisplayNames } from "@/models/TaskPriority";

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
      priority: props.task.priority,
    });
    const resetForm = (): void => {
      form.priority = props.task.priority;
    };
    const openDialog = (): void => {
      resetForm();
      isDialogShown.value = true;
    };
    const priorities = Array.from(taskPriorityDisplayNames.entries());

    /**
     * API実行
     */
    const executeUpdateTask = async (): Promise<void> => {
      try {
        await MessageBox.confirm("タスクの優先度を変更します。", "実行確認", {
          confirmButtonText: "実行",
          cancelButtonText: "戻る",
          type: "info",
        });
      } catch {
        return;
      }
      isExecuteButtonLoading.value = true;
      await apiInvoker.updateTaskPriority(props.task.id, {
        newPriority: form.priority,
      });

      isExecuteButtonLoading.value = false;
      isDialogShown.value = false;
      emit("task-priority-updated");
    };

    return {
      isDialogShown,
      isExecuteButtonLoading,
      form,
      openDialog,
      priorities,
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
