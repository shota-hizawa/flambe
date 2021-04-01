<template>
  <div class="component-wrapper">
    <el-button
      type="primary"
      icon="el-icon-plus"
      size="mini"
      @click="openDialog"
      plain
    >
      新規ユーザ
    </el-button>
    <el-dialog
      title="新規ユーザ"
      :visible.sync="isDialogShown"
      width="800px"
      :close-on-click-modal="false"
      :show-close="false"
      :close-on-press-escape="false"
    >
      <el-form class="form__body" label-position="left" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="ユーザ名">
              <el-input
                v-model="form.username"
                placeholder="ユーザ名を入力してください"
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="パスワード">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="パスワードを入力してください"
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
import CreateUserRequest from "@/api/requests/CreateUserRequest";
import {
  usernameMaxLength,
  usernameMinLength,
  userPasswordMaxLength,
  userPasswordMinLength,
} from "@/models/User";

export default defineComponent({
  setup(_, { emit }) {
    const isDialogShown = ref<boolean>(false);

    /*
     * フォーム関連
     */
    const form = reactive({
      username: "",
      password: "",
    });
    const isExecuteButtonDisabled = computed((): boolean => {
      return !form.password && !form.username;
    });
    const isExecuteButtonLoading = ref<boolean>(false);
    const resetForm = (): void => {
      form.username = "";
      form.password = "";
    };
    const openDialog = (): void => {
      resetForm();
      isDialogShown.value = true;
    };

    /**
     * API実行
     */
    const executeCreateUser = async (): Promise<void> => {
      const request = {
        username: form.username,
        password: form.password,
      };

      validateRequest(request);

      try {
        await MessageBox.confirm("新規ユーザを作成します。", "実行確認", {
          confirmButtonText: "実行",
          cancelButtonText: "戻る",
          type: "info",
        });
      } catch {
        return;
      }
      isExecuteButtonLoading.value = true;

      await apiInvoker.createUser(request);

      isExecuteButtonLoading.value = false;
      isDialogShown.value = false;
      emit("user-created");
    };

    const validateRequest = (request: CreateUserRequest): void => {
      if (
        request.username.length < usernameMinLength ||
        request.username.length > usernameMaxLength
      ) {
        Notification.error({
          title: "Error: 入力エラー",
          message: `ユーザ名は${usernameMinLength}文字以上${usernameMaxLength}文字以下で入力してください`,
        });
        throw new Error();
      }

      if (
        request.password.length < userPasswordMinLength ||
        request.password.length > userPasswordMaxLength
      ) {
        Notification.error({
          title: "Error: 入力エラー",
          message: `パスワードは${userPasswordMinLength}文字以上${userPasswordMaxLength}文字以下で入力してください`,
        });
        throw new Error();
      }
    };

    return {
      isDialogShown,
      form,
      isExecuteButtonDisabled,
      isExecuteButtonLoading,
      openDialog,
      executeCreateUser,
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
