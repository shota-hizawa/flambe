<template>
  <div class="component-wrapper">
    <el-button
      type="primary"
      icon="el-icon-search"
      size="mini"
      @click="openDialog"
      plain
    >
      未完了タスク一覧
    </el-button>
    <el-dialog
      title="未完了タスク一覧"
      :visible.sync="isDialogShown"
      width="1000px"
      :close-on-click-modal="false"
      :show-close="false"
      :close-on-press-escape="false"
    >
      <el-table
        :data="allTasks"
        size="mini"
        :row-class-name="tableRowClassName"
        class="table"
        v-loading="loading"
      >
        <el-table-column prop="id" label="ID" min-width="50"></el-table-column>
        <el-table-column
          prop="title"
          label="タイトル"
          min-width="150"
          show-overflow-tooltip
        ></el-table-column>
        <el-table-column
          prop="status"
          label="ステータス"
          min-width="85"
          :formatter="taskStatusFormatter"
        ></el-table-column>
        <el-table-column
          prop="priority"
          label="優先度"
          min-width="85"
          :formatter="taskPriorityFormatter"
          class-name="priority-column"
        >
        </el-table-column>
        <el-table-column
          prop="createdAt"
          label="作成日時"
          min-width="165"
          :formatter="dateTimeFormatter"
        ></el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button class="form__button" @click="isDialogShown = false"
          >閉じる</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from "@vue/composition-api";
import apiInvoker from "@/api/ApiInvoker";
import User from "@/models/User";
import { taskStatusFormatter } from "@/models/TaskStatus";
import { TaskPriority, taskPriorityFormatter } from "@/models/TaskPriority";
import { dateTimeFormatter } from "@/utils/daiteTImeFormatter";
import Task from "@/models/Task";

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
  setup(props: Props) {
    const isDialogShown = ref<boolean>(false);
    const openDialog = (): void => {
      searchTasks();
      isDialogShown.value = true;
    };

    /**
     * API実行
     */
    let allTasks = ref(Array<Task>());
    const searchTasks = async () => {
      openLoading();
      allTasks.value.splice(-allTasks.value.length);
      const results = await apiInvoker.getUserIncompleteTasks(props.user.id);

      results.forEach((result) => {
        allTasks.value.push(result);
      });
      closeLoading();
    };

    /**
     * テーブルローディング
     */
    const loading = ref<boolean>(true);
    const openLoading = (): void => {
      loading.value = true;
    };
    const closeLoading = (): void => {
      loading.value = false;
    };

    const tableRowClassName = ({ row }: { row: Task }): string | undefined => {
      if (row.priority === TaskPriority.HIGH) return "high-priority-row";
      if (row.priority === TaskPriority.MEDIUM) return "medium-priority-row";
      if (row.priority === TaskPriority.LOW) return "low-priority-row";
    };

    return {
      isDialogShown,
      loading,
      openDialog,
      searchTasks,
      allTasks,
      taskStatusFormatter,
      taskPriorityFormatter,
      dateTimeFormatter,
      tableRowClassName,
    };
  },
});
</script>

<style lang="scss" scoped>
@import "src/styles/common-style-variables";
.component-wrapper {
  display: inline-block;
}

.table::v-deep .high-priority-row {
  .priority-column {
    color: $high-priority-task-color;
  }
}

.table::v-deep .medium-priority-row {
  .priority-column {
    color: $medium-priority-task-color;
  }
}
.table::v-deep .low-priority-row {
  .priority-column {
    color: $low-priority-task-color;
  }
}
</style>
