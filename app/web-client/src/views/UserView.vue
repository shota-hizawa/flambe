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
      class="user-view__table"
      :data="filteredUserWithDoingTask"
      border
      size="mini"
      :default-sort="{ prop: 'user.id', order: 'ascending' }"
    >
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
      <el-table-column label="タスク数">
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

export default defineComponent({
  components: {
    UserCreateModal,
    UserDeleteModal,
  },
  setup() {
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
      userWithDoingTask.value.splice(-userWithDoingTask.value.length);
      const results = await apiInvoker.getUserWithDoingTaskData();
      results.forEach((result) => {
        userWithDoingTask.value.push(result);
      });
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

    return {
      filteredUserWithDoingTask,
      form,
      searchUserWithDoingTask,
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
}
</style>
