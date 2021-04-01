<template>
  <div class="component-wrapper">
    <el-row class="task-view__title"> タスク一覧 </el-row>
    <el-divider></el-divider>
    <el-row class="task-view__controller">
      <el-col :span="24">
        <task-create-modal
          class="task-view__controller-parts"
          @task-created="searchTasks"
        ></task-create-modal>
        <el-select
          class="task-view__controller-parts"
          v-model="form.selectedStatuses"
          multiple
          placeholder="ステータスでフィルタ"
          size="mini"
          style="width: 250px"
        >
          <el-option
            v-for="i in statuses"
            :key="i[0]"
            :label="i[1]"
            :value="i[0]"
          />
        </el-select>
        <el-select
          class="task-view__controller-parts"
          v-model="form.selectedPriorities"
          multiple
          placeholder="優先度でフィルタ"
          size="mini"
          style="width: 250px"
        >
          <el-option
            v-for="i in priorities"
            :key="i[0]"
            :label="i[1]"
            :value="i[0]"
          />
        </el-select>
        <el-button
          class="task-view__controller-parts-button"
          type="primary"
          icon="el-icon-search"
          size="mini"
          @click="clickSearchButton"
          plain
        >
          検索
        </el-button>
      </el-col>
    </el-row>
    <el-row class="task-view__paginator">
      <el-pagination
        @current-change="searchTasks"
        :current-page.sync="currentPage"
        layout="prev, pager, next"
        :total="totalPages"
        :page-size="pageSize"
      >
      </el-pagination>
    </el-row>
    <el-table
      v-loading="loading"
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
                <div slot="header" class="task-view__assignees-card">
                  <span>担当者</span>
                  <task-assign-user-modal
                    :task="props.row"
                    @task-assigned="searchTasks"
                  ></task-assign-user-modal>
                </div>
                <el-table
                  :data="props.row.assignees"
                  size="mini"
                  :show-header="false"
                >
                  <el-table-column
                    prop="username"
                    min-width="200"
                  ></el-table-column>
                  <el-table-column min-width="150">
                    <template slot-scope="scope">
                      <el-row class="task-view__operation-assign-column">
                        <task-remove-assignment-user-modal
                          :task="props.row"
                          :user="scope.row"
                          @task-assignment-removed="searchTasks"
                        ></task-remove-assignment-user-modal>
                      </el-row>
                    </template>
                  </el-table-column>
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
              @task-status-updated="searchTasks"
            ></task-status-update-modal>
            <task-priority-update-modal
              :task="scope.row"
              @task-priority-updated="searchTasks"
            ></task-priority-update-modal>
            <task-delete-modal
              :task="scope.row"
              @task-deleted="searchTasks"
            ></task-delete-modal>
          </el-row>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script lang="ts">
import apiInvoker from "@/api/ApiInvoker";
import {
  defineComponent,
  onMounted,
  reactive,
  ref,
} from "@vue/composition-api";
import {
  TaskStatus,
  taskStatusDisplayNames,
  taskStatusFormatter,
} from "@/models/TaskStatus";
import {
  taskPriorityDisplayNames,
  taskPriorityFormatter,
} from "@/models/TaskPriority";
import Task from "@/models/Task";
import { TaskPriority } from "@/models/TaskPriority";
import { dateTimeFormatter } from "@/utils/daiteTImeFormatter";
import TaskCreateModal from "@/components/modals/TaskCreateModal.vue";
import TaskDeleteModal from "@/components/modals/TaskDeleteModal.vue";
import TaskStatusUpdateModal from "@/components/modals/TaskStatusUpdateModal.vue";
import TaskPriorityUpdateModal from "@/components/modals/TaskPriorityUpdateModal.vue";
import TaskAssignUserModal from "@/components/modals/TaskAssignUserModal.vue";
import TaskRemoveAssignmentUserModal from "@/components/modals/TaskRemoveAssignmentUserModal.vue";

export default defineComponent({
  components: {
    TaskCreateModal,
    TaskDeleteModal,
    TaskStatusUpdateModal,
    TaskPriorityUpdateModal,
    TaskAssignUserModal,
    TaskRemoveAssignmentUserModal,
  },
  setup() {
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

    /**
     * フォーム
     */
    const form = reactive<{
      selectedStatuses: Array<TaskStatus>;
      selectedPriorities: Array<TaskPriority>;
    }>({
      selectedStatuses: [],
      selectedPriorities: [],
    });
    const statuses = Array.from(taskStatusDisplayNames.entries());
    const priorities = Array.from(taskPriorityDisplayNames.entries());

    /**
     * タスク情報
     */
    const totalTasksCount = ref<number>(0);
    const currentPage = ref<number>(1);
    const pageSize = 20;
    let allTasks = ref(Array<Task>());
    const clickSearchButton = async () => {
      currentPage.value = 1;
      await searchTasks();
    };
    const searchTasks = async () => {
      openLoading();
      allTasks.value.splice(-allTasks.value.length);
      const results = await apiInvoker.searchTasks(
        {
          statuses: form.selectedStatuses,
          priorities: form.selectedPriorities,
        },
        currentPage.value - 1,
        pageSize
      );
      totalTasksCount.value = results.total;

      results.items.forEach((result) => {
        allTasks.value.push(result);
      });
      closeLoading();
    };

    const tableRowClassName = ({ row }: { row: Task }): string | undefined => {
      if (row.priority === TaskPriority.HIGH) return "high-priority-row";
      if (row.priority === TaskPriority.MEDIUM) return "medium-priority-row";
      if (row.priority === TaskPriority.LOW) return "low-priority-row";
    };

    const cardBodyStyle = { padding: "10px" };

    /**
     * ライフサイクルフック
     */
    onMounted(async () => {
      await searchTasks();
    });

    return {
      loading,
      allTasks,
      form,
      statuses,
      priorities,
      totalPages: totalTasksCount,
      currentPage,
      pageSize,
      taskStatusFormatter,
      taskPriorityFormatter,
      dateTimeFormatter,
      clickSearchButton,
      searchTasks,
      tableRowClassName,
      cardBodyStyle,
      TaskPriority,
    };
  },
});
</script>

<style lang="scss" scoped>
@import "../styles/common-style-variables";

.task-view {
  &__controller {
    margin-bottom: 15px;
  }
  &__controller-parts {
    margin-right: 15px;
  }
  &__controller-parts-button {
    width: $normal-button-size;
  }
  &__title {
    font-size: $component-title-font-size;
  }

  &__assignees-card {
    display: flex;
    justify-content: space-between;
    height: 13px;
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
