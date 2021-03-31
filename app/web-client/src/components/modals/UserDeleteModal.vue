<template>
  <div class="component-wrapper">
    <el-button
      type="primary"
      icon="el-icon-delete"
      size="mini"
      @click="openDialog"
      plain
    >
      ユーザ削除
    </el-button>
    <el-dialog
      title="ユーザ削除"
      :visible.sync="isDialogShown"
      width="500px"
      :close-on-click-modal="false"
      :show-close="false"
      :close-on-press-escape="false"
    >
      ユーザ: {{ user.username }} を削除します。
      <div slot="footer" class="dialog-footer">
        <el-button
          class="form__button"
          type="primary"
          @click="executeCreateUser"
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
import User from "@/models/user";

type Props = {
  user: User;
};

export default defineComponent({
  props: {
    user: {
      type: Object as PropType<User>,
      required: true,
    },
  },
  setup(props: Props, { emit }) {
    const isDialogShown = ref<boolean>(false);
    const isExecuteButtonLoading = ref<boolean>(false);
    const openDialog = (): void => {
      console.info("aaa");
      console.info(props.user);
      isDialogShown.value = true;
    };

    /**
     * API実行
     */
    const executeCreateUser = async (): Promise<void> => {
      try {
        await MessageBox.confirm("ユーザ削除を実行します。", "実行確認", {
          confirmButtonText: "実行",
          cancelButtonText: "戻る",
          type: "info",
        });
      } catch {
        return;
      }
      isExecuteButtonLoading.value = true;
      await apiInvoker.deleteUser(props.user.id);

      isExecuteButtonLoading.value = false;
      isDialogShown.value = false;
      emit("user-deleted");
    };

    return {
      isDialogShown,
      isExecuteButtonLoading,
      openDialog,
      executeCreateUser,
    };
  },
});
</script>

<style lang="scss" scoped>
@import "src/styles/common-style-variables";
.content-wrapper {
  display: inline-block;
}

.form {
  &__button {
    width: $normal-button-size;
  }
}
</style>
