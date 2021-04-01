<template>
  <div class="component-wrapper">
    <el-button
      type="primary"
      icon="el-icon-plus"
      size="mini"
      @click="openDialog"
      plain
    >
      新規タスク
    </el-button>
    <el-dialog
      title="新規タスク"
      :visible.sync="isDialogShown"
      width="800px"
      :close-on-click-modal="false"
      :show-close="false"
      :close-on-press-escape="false"
    >
      <el-form class="form__body" label-position="left" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="タイトル">
              <el-input
                v-model="form.title"
                placeholder="タイトルを入力してください"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="優先度">
              <el-select v-model="form.priority" placeholder="優先度を選択">
                <el-option
                  v-for="i in priorities"
                  :key="i[0]"
                  :label="i[1]"
                  :value="i[0]"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="説明">
              <el-input
                v-model="form.description"
                type="textarea"
                placeholder="タスクの説明を入力してください"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button
          class="form__button"
          type="primary"
          @click="executeCreateUser"
          :disabled="isExecuteButtonDisabled"
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
import { computed, defineComponent, reactive, ref } from "@vue/composition-api";
import apiInvoker from "@/api/ApiInvoker";
import { MessageBox, Notification } from "element-ui";
import { TaskPriority, taskPriorityDisplayNames } from "@/models/TaskPriority";
import {
  taskDescriptionMaxLength,
  taskTitleMaxLength,
  taskTitleMinLength,
} from "@/models/Task";
import CreateTaskRequest from "@/api/requests/CreateTaskRequest";

export default defineComponent({
  setup(_, { emit }) {
    const isDialogShown = ref<boolean>(false);

    /*
     * フォーム関連
     */
    const form = reactive({
      title: "",
      description: "",
      priority: TaskPriority.MEDIUM,
    });
    const isExecuteButtonDisabled = computed((): boolean => {
      return !form.description && !form.title;
    });
    const isExecuteButtonLoading = ref<boolean>(false);
    const resetForm = (): void => {
      form.title = "";
      form.description = "";
      form.priority = TaskPriority.MEDIUM;
    };
    const priorities = Array.from(taskPriorityDisplayNames.entries());
    const openDialog = (): void => {
      resetForm();
      isDialogShown.value = true;
    };

    /**
     * API実行
     */
    const executeCreateTask = async (): Promise<void> => {
      const request = {
        title: form.title,
        description: form.description,
        priority: form.priority,
      };

      validateRequest(request);

      try {
        await MessageBox.confirm("新規タスクを作成します。", "実行確認", {
          confirmButtonText: "実行",
          cancelButtonText: "戻る",
          type: "info",
        });
      } catch {
        return;
      }
      isExecuteButtonLoading.value = true;

      await apiInvoker.createTask(request);

      isExecuteButtonLoading.value = false;
      isDialogShown.value = false;
      emit("task-created");
    };

    const validateRequest = (request: CreateTaskRequest): void => {
      if (
        request.title.length < taskTitleMinLength ||
        request.title.length > taskTitleMaxLength
      ) {
        Notification.error({
          title: "Error: 入力エラー",
          message: `タスク名は${taskTitleMinLength}文字以上${taskTitleMaxLength}文字以内で入力してください`,
        });
        throw new Error();
      }

      if (request.description.length > taskDescriptionMaxLength) {
        Notification.error({
          title: "Error: 入力エラー",
          message: `タスクの説明は${taskDescriptionMaxLength}文字以内で入力してください`,
        });
        throw new Error();
      }
    };

    return {
      isDialogShown,
      form,
      priorities,
      isExecuteButtonDisabled,
      isExecuteButtonLoading,
      openDialog,
      executeCreateUser: executeCreateTask,
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
