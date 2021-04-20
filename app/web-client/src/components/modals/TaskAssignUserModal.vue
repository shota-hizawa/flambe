<template>
  <div class="component-wrapper">
    <el-button type="text" size="mini" @click="openDialog" style="padding: 0">
      タスクアサイン
    </el-button>
    <el-dialog
      title="タスクアサイン"
      :visible.sync="isDialogShown"
      width="600px"
      :close-on-click-modal="false"
      :show-close="false"
      :close-on-press-escape="false"
    >
      <p>対象タスク: {{ task.title }}</p>
      <el-select
        v-model="form.assignedUserId"
        filterable
        placeholder="ユーザを選択"
        style="width: 300px"
      >
        <el-option
          v-for="item in notAssignedUsers"
          :key="item.id"
          :label="item.username"
          :value="item.id"
        >
        </el-option>
      </el-select>
      <div slot="footer" class="dialog-footer">
        <el-button
          class="form__button"
          type="primary"
          @click="assignTaskToUser"
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
import {
  defineComponent,
  onMounted,
  PropType,
  reactive,
  ref,
} from "@vue/composition-api";
import apiInvoker from "@/api/ApiInvoker";
import { MessageBox, Notification } from "element-ui";
import TaskWithAssignees from "@/models/TaskWithAssignees";
import User from "@/models/User";

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

    /**
     * フォーム関連
     */
    const form = reactive<{ assignedUserId: number | undefined }>({
      assignedUserId: undefined,
    });
    const resetForm = (): void => {
      form.assignedUserId = undefined;
    };
    const openDialog = (): void => {
      resetForm();
      isDialogShown.value = true;
    };

    /**
     *  対象ユーザ取得処理
     */
    const notAssignedUsers = ref<Array<User>>([]);
    const searchAllUsersAndEliminateAlreadyAssigned = async () => {
      const alreadyAssignedUserIds = props.task.assignees.map((assignee) => {
        return assignee.id;
      });
      notAssignedUsers.value.splice(-notAssignedUsers.value.length);
      const results = await apiInvoker.getAllUsers();
      results.forEach((result) => {
        if (!alreadyAssignedUserIds.includes(result.id))
          notAssignedUsers.value.push(result);
      });
    };

    /**
     * API実行
     */
    const assignTaskToUser = async (): Promise<void> => {
      try {
        await MessageBox.confirm(`タスクのアサインを実行します。`, "実行確認", {
          confirmButtonText: "実行",
          cancelButtonText: "戻る",
          type: "info",
        });
      } catch {
        return;
      }
      isExecuteButtonLoading.value = true;
      if (typeof form.assignedUserId === "number") {
        await apiInvoker.assignTaskToUser({
          taskId: props.task.id,
          userId: form.assignedUserId,
        });

        isExecuteButtonLoading.value = false;
        isDialogShown.value = false;
        emit("task-assigned");
      } else {
        Notification.error({
          title: "Error: 入力エラー",
          message: "不正なユーザIDです",
        });
      }
    };

    /**
     * ライフサイクルフック
     */
    onMounted(async () => {
      await searchAllUsersAndEliminateAlreadyAssigned();
    });

    return {
      isDialogShown,
      isExecuteButtonLoading,
      form,
      openDialog,
      notAssignedUsers,
      assignTaskToUser,
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
