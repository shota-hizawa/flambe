<template>
  <div class="component-wrapper">
    <el-row class="task-view__title"> タスク一覧 </el-row>
    <el-divider></el-divider>
    <el-row class="task-view__controller">
      <el-col :span="24">
        <task-create-modal
          class="task-view__controller-parts"
          @task-created="searchAllTasks"
        ></task-create-modal>
      </el-col>
    </el-row>
    <el-table
      class="task-view__table"
      :data="allTasks"
      border
      size="mini"
      :default-sort="{ prop: 'task.id', order: 'ascending' }"
      :row-class-name="tableRowClassName"
    >
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card
                class="box-card"
                shadow="never"
                :body-style="cardBodyStyle"
              >
                <div slot="header">
                  <span>説明</span>
                </div>
                <p>{{ props.row.description }}</p>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card
                class="box-card"
                shadow="never"
                :body-style="cardBodyStyle"
              >
                <div slot="header">
                  <span>担当者</span>
                </div>
                <el-table
                  :data="props.row.assignees"
                  size="mini"
                  :show-header="false"
                >
                  <el-table-column prop="username"></el-table-column>
                </el-table>
              </el-card>
            </el-col>
          </el-row>
        </template>
      </el-table-column>
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
      <el-table-column label="オペレーション" min-width="400">
        <template slot-scope="scope">
          <el-row class="task-view__operation-column">
            <task-status-update-modal
              :task="scope.row"
              @task-status-updated="searchAllTasks"
            ></task-status-update-modal>
            <task-priority-update-modal
              :task="scope.row"
              @task-priority-updated="searchAllTasks"
            ></task-priority-update-modal>
            <task-delete-modal
              :task="scope.row"
              @task-deleted="searchAllTasks"
            ></task-delete-modal>
          </el-row>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script lang="ts">
import apiInvoker from "@/api/ApiInvoker";
import { defineComponent, onMounted, ref } from "@vue/composition-api";
import { taskStatusFormatter } from "@/models/TaskStatus";
import { taskPriorityFormatter } from "@/models/TaskPriority";
import Task from "@/models/Task";
import { TaskPriority } from "@/models/TaskPriority";
import { dateTimeFormatter } from "@/utils/daiteTImeFormatter";
import TaskCreateModal from "@/components/modals/TaskCreateModal.vue";
import TaskDeleteModal from "@/components/modals/TaskDeleteModal.vue";
import TaskStatusUpdateModal from "@/components/modals/TaskStatusUpdateModal.vue";
import TaskPriorityUpdateModal from "@/components/modals/TaskPriorityUpdateModal.vue";

export default defineComponent({
  components: {
    TaskCreateModal,
    TaskDeleteModal,
    TaskStatusUpdateModal,
    TaskPriorityUpdateModal,
  },
  setup() {
    let allTasks = ref(Array<Task>());

    // const filteredUserWithDoingTask = computed(
    //   (): Array<GetUserWithDoingTaskDataResponse> => {
    //     if (!form.usernameFilter) return userWithDoingTask.value;
    //     return userWithDoingTask.value.filter((userWithDoingTask) =>
    //       userWithDoingTask.user.username.includes(form.usernameFilter)
    //     );
    //   }
    // );

    const searchAllTasks = async () => {
      allTasks.value.splice(-allTasks.value.length);
      const results = await apiInvoker.getAllTasks();
      results.forEach((result) => {
        allTasks.value.push(result);
      });
    };

    // eslint-disable-next-line
    const tableRowClassName = ({row} : {row: Task}): string | undefined => {
      if (row.priority === TaskPriority.HIGH) return "high-priority-row";
      if (row.priority === TaskPriority.MEDIUM) return "medium-priority-row";
      if (row.priority === TaskPriority.LOW) return "low-priority-row";
    };

    const cardBodyStyle = { padding: "10px" };

    /**
     * フォーム
     */
    // const form = reactive({
    //   usernameFilter: "",
    // });

    /**
     * ライフサイクルフック
     */
    onMounted(async () => {
      await searchAllTasks();
    });

    return {
      allTasks,
      taskStatusFormatter,
      taskPriorityFormatter,
      dateTimeFormatter,
      searchAllTasks,
      tableRowClassName,
      cardBodyStyle,
      TaskPriority,
    };
  },
});
</script>

<style lang="scss" scoped>
@import "../styles/common-style-variables";
//@import "~element-ui/packages/theme-chalk/src/index";

.task-view {
  &__controller {
    margin-bottom: 15px;
  }
  &__controller-parts {
    margin-right: 15px;
  }
  &__title {
    font-size: $component-title-font-size;
  }

  &__operation-column::v-deep .el-button {
    margin-left: 10px;
  }
  &__table::v-deep .high-priority-row {
    .priority-column {
      color: $high-priority-task-color;
    }
  }

  &__table::v-deep .medium-priority-row {
    .priority-column {
      color: $medium-priority-task-color;
    }
  }
  &__table::v-deep .low-priority-row {
    .priority-column {
      color: $low-priority-task-color;
    }
  }
}
</style>
