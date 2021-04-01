<template>
  <div class="component-wrapper">
    <el-row class="user-view__title"> ユーザ一覧 </el-row>
    <el-divider></el-divider>
    <el-row class="user-view__controller">
      <el-col :span="24">
        <user-create-modal
          class="user-view__controller-parts"
          @user-created="searchUserWithDoingTask"
        ></user-create-modal>
        <el-input
          class="user-view__controller-parts"
          size="mini"
          v-model="form.usernameFilter"
          style="width: 400px"
        >
          <template slot="prepend">ユーザ名検索</template>
        </el-input>
      </el-col>
    </el-row>
    <el-table
      v-loading="loading"
      class="user-view__table"
      :data="filteredUserWithDoingTask"
      border
      size="mini"
      :default-sort="{ prop: 'user.id', order: 'ascending' }"
    >
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-row :gutter="20">
            <el-card
              class="box-card"
              shadow="never"
              :body-style="cardBodyStyle"
            >
              <div slot="header" class="user-view__doing-tasks-card">
                <span>未完了タスク一覧</span>
              </div>
              <el-table
                :data="props.row.incompleteTasks"
                size="mini"
                :row-class-name="tableRowClassName"
                class="user-view__sub-table"
              >
                <el-table-column
                  prop="id"
                  label="ID"
                  min-width="50"
                ></el-table-column>
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
            </el-card>
          </el-row>
        </template>
      </el-table-column>
      <el-table-column
        prop="user.id"
        label="ID"
        min-width="50"
      ></el-table-column>
      <el-table-column
        prop="user.username"
        label="ユーザ名"
        min-width="200"
      ></el-table-column>
      <el-table-column label="作業中タスク数">
        <el-table-column
          prop="doingTaskData.highTaskCount"
          label="優先度高"
          min-width="100"
        ></el-table-column>
        <el-table-column
          prop="doingTaskData.mediumTaskCount"
          label="優先度中"
          min-width="100"
        ></el-table-column>
        <el-table-column
          prop="doingTaskData.lowTaskCount"
          label="優先度低"
          min-width="100"
        ></el-table-column>
      </el-table-column>
      <el-table-column label="オペレーション" min-width="150">
        <template slot-scope="scope">
          <user-delete-modal
            :user="scope.row.user"
            @user-deleted="searchUserWithDoingTask"
          ></user-delete-modal>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script lang="ts">
import GetUserWithDoingTaskDataResponse from "@/api/responses/GetUserWithDoingTaskDataResponse";
import apiInvoker from "@/api/ApiInvoker";
import {
  computed,
  defineComponent,
  onMounted,
  reactive,
  ref,
} from "@vue/composition-api";
import UserCreateModal from "@/components/modals/UserCreateModal.vue";
import UserDeleteModal from "@/components/modals/UserDeleteModal.vue";
import { taskStatusFormatter } from "@/models/TaskStatus";
import { TaskPriority, taskPriorityFormatter } from "@/models/TaskPriority";
import { dateTimeFormatter } from "@/utils/daiteTImeFormatter";
import Task from "@/models/Task";

export default defineComponent({
  components: {
    UserCreateModal,
    UserDeleteModal,
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
     * ユーザ情報
     */
    let userWithDoingTask = ref(Array<GetUserWithDoingTaskDataResponse>());
    const filteredUserWithDoingTask = computed(
      (): Array<GetUserWithDoingTaskDataResponse> => {
        if (!form.usernameFilter) return userWithDoingTask.value;
        return userWithDoingTask.value.filter((userWithDoingTask) =>
          userWithDoingTask.user.username.includes(form.usernameFilter)
        );
      }
    );
    const searchUserWithDoingTask = async () => {
      openLoading();
      userWithDoingTask.value.splice(-userWithDoingTask.value.length);
      const results = await apiInvoker.getUserWithDoingTaskData();
      results.forEach((result) => {
        userWithDoingTask.value.push(result);
      });
      closeLoading();
    };

    const tableRowClassName = ({ row }: { row: Task }): string | undefined => {
      if (row.priority === TaskPriority.HIGH) return "high-priority-row";
      if (row.priority === TaskPriority.MEDIUM) return "medium-priority-row";
      if (row.priority === TaskPriority.LOW) return "low-priority-row";
    };

    /**
     * フォーム
     */
    const form = reactive({
      usernameFilter: "",
    });

    /**
     * ライフサイクルフック
     */
    onMounted(async () => {
      await searchUserWithDoingTask();
    });

    const cardBodyStyle = { padding: "10px" };

    return {
      loading,
      filteredUserWithDoingTask,
      form,
      searchUserWithDoingTask,
      cardBodyStyle,
      taskStatusFormatter,
      taskPriorityFormatter,
      dateTimeFormatter,
      tableRowClassName,
    };
  },
});
</script>

<style lang="scss" scoped>
@import "../styles/common-style-variables";
.user-view {
  &__controller {
    margin-bottom: 15px;
  }
  &__controller-parts {
    margin-right: 15px;
  }
  &__title {
    font-size: $component-title-font-size;
  }
  &__sub-table::v-deep .high-priority-row {
    .priority-column {
      color: $high-priority-task-color;
    }
  }

  &__sub-table::v-deep .medium-priority-row {
    .priority-column {
      color: $medium-priority-task-color;
    }
  }
  &__sub-table::v-deep .low-priority-row {
    .priority-column {
      color: $low-priority-task-color;
    }
  }
}
</style>
