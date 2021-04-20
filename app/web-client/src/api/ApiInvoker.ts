import axios, { AxiosError, AxiosInstance } from "axios";
import { Notification } from "element-ui";
import GetUserWithDoingTaskDataResponse from "@/api/responses/GetUserWithDoingTaskDataResponse";
import CreateUserRequest from "@/api/requests/CreateUserRequest";
import TaskWithAssignees from "@/models/TaskWithAssignees";
import dayjs from "dayjs";
import CreateTaskRequest from "@/api/requests/CreateTaskRequest";
import UpdateTaskStatusRequest from "@/api/requests/UpdateTaskStatusRequest";
import UpdateTaskPriorityRequest from "@/api/requests/UpdateTaskPriorityRequest";
import User from "@/models/User";
import AssignTaskToUserRequest from "@/api/requests/AssignTaskToUserRequest";
import RemoveTaskAssignmentFromUserRequest from "@/api/requests/RemoveTaskAssignmentFromUserRequest";
import GetTasksFilteredByStatusesAndPrioritiesRequest from "@/api/requests/GetTasksFilteredByStatusesAndPrioritiesRequest";
import PaginatedResponse from "@/api/responses/PaginatedResponse";

const iso8601Datetime = /\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d/;

class AxiosFactory {
  readonly baseUrl: string = process.env.VUE_APP_WEB_SERVER_ENDPOINT;
  client: AxiosInstance;

  constructor() {
    this.client = this.getClient();
  }

  /**************************************************************************************************
   * ユーザ系
   **************************************************************************************************/
  public getAllUsers = async (): Promise<Array<User>> => {
    try {
      const response = await this.client.get<Array<User>>("/users");
      return response.data;
    } catch (e) {
      this.handleError(e);
      throw new Error("ユーザ情報の取得に失敗しました。");
    }
  };

  public getUserWithDoingTaskData = async (): Promise<
    Array<GetUserWithDoingTaskDataResponse>
  > => {
    try {
      const response = await this.client.get<
        Array<GetUserWithDoingTaskDataResponse>
      >("/users/doing-task-data");
      return response.data;
    } catch (e) {
      this.handleError(e);
      throw new Error("ユーザ情報の取得に失敗しました。");
    }
  };
  public createUser = async (request: CreateUserRequest): Promise<void> => {
    try {
      await this.client.post("/users", request);
      this.handleSuccess("新規ユーザを追加しました。");
    } catch (e) {
      this.handleError(e);
    }
  };

  public deleteUser = async (userId: number): Promise<void> => {
    try {
      await this.client.delete(`/users/${userId}`);
      this.handleSuccess("ユーザを削除しました。");
    } catch (e) {
      this.handleError(e);
    }
  };

  /**************************************************************************************************
   * タスク系
   **************************************************************************************************/
  public searchTasks = async (
    request: GetTasksFilteredByStatusesAndPrioritiesRequest,
    page: number,
    size: number
  ): Promise<PaginatedResponse<TaskWithAssignees>> => {
    try {
      // 1ページの取得数は20で固定にする
      const response = await this.client.post<
        PaginatedResponse<TaskWithAssignees>
      >(`/tasks/search?page=${page}&size=${size}`, request);
      return response.data;
    } catch (e) {
      this.handleError(e);
      throw new Error("タスク情報の取得に失敗しました。");
    }
  };

  public createTask = async (request: CreateTaskRequest): Promise<void> => {
    try {
      await this.client.post("/tasks", request);
      this.handleSuccess("新規タスクを追加しました。");
    } catch (e) {
      this.handleError(e);
    }
  };

  public updateTaskStatus = async (
    taskId: number,
    request: UpdateTaskStatusRequest
  ): Promise<void> => {
    try {
      await this.client.put(`/tasks/${taskId}/status`, request);
      this.handleSuccess("タスクのステータスを変更しました。");
    } catch (e) {
      this.handleError(e);
    }
  };

  public updateTaskPriority = async (
    taskId: number,
    request: UpdateTaskPriorityRequest
  ): Promise<void> => {
    try {
      await this.client.put(`/tasks/${taskId}/priority`, request);
      this.handleSuccess("タスクの優先度を変更しました。");
    } catch (e) {
      this.handleError(e);
    }
  };

  public assignTaskToUser = async (
    request: AssignTaskToUserRequest
  ): Promise<void> => {
    try {
      await this.client.post("/tasks/assign", request);
      this.handleSuccess("タスクをアサインしました。");
    } catch (e) {
      this.handleError(e);
    }
  };

  public removeTaskAssignmentFromUser = async (
    request: RemoveTaskAssignmentFromUserRequest
  ): Promise<void> => {
    try {
      await this.client.post("/tasks/remove-assign", request);
      this.handleSuccess("タスクのアサインを削除しました。");
    } catch (e) {
      this.handleError(e);
    }
  };

  public deleteTask = async (taskId: number): Promise<void> => {
    try {
      await this.client.delete(`/tasks/${taskId}`);
      this.handleSuccess("タスクを削除しました。");
    } catch (e) {
      this.handleError(e);
    }
  };

  /**************************************************************************************************
   * 共通処理
   **************************************************************************************************/
  private handleSuccess = (message: string): void => {
    Notification.success({
      title: "Success",
      message,
    });
  };

  // エラーメッセージのみ、FastAPIでキャメルケースで取り扱うベストプラクティスが不明なため暫定的にスネークケースを許容
  private handleError = (e: AxiosError): void => {
    const response = e.response?.data;
    const code = response.error_code ? response.error_code : "unknown";
    const message = response.error_msg
      ? response.error_msg
      : "unknown error occurred";
    Notification.error({
      title: `Error: ${code}`,
      message: message,
    });
  };

  // eslint-disable-next-line
  private dayjsParseChallenge = (key: string, val: any) => {
    if (typeof val === "string") {
      return iso8601Datetime.test(val) ? dayjs(val) : val;
    } else {
      return val;
    }
  };

  private getClient = (): AxiosInstance => {
    return axios.create({
      baseURL: this.baseUrl,
      headers: { "Content-Type": "application/json" },
      responseType: "json",
      // 可能な場合はレスポンスのフィールドをdayjsに変換する
      // cf. https://github.com/axios/axios/blob/16b5718954d88fbefe17f0b91101d742b63209c7/lib/defaults.js#L57
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      transformResponse: (data: any) => {
        try {
          return JSON.parse(JSON.stringify(data), this.dayjsParseChallenge);
        } catch (e) {
          console.error(e);
        }
        return data;
      },
    });
  };
}

const apiInvoker = new AxiosFactory();

export default apiInvoker;
