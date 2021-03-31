import axios, { AxiosError, AxiosInstance } from "axios";
import { Notification } from "element-ui";
import GetUserWithDoingTaskDataResponse from "@/api/responses/GetUserWithDoingTaskDataResponse";
import CreateUserRequest from "@/api/requests/CreateUserRequest";

class AxiosFactory {
  readonly baseUrl: string = process.env.VUE_APP_WEB_SERVER_ENDPOINT;
  client: AxiosInstance;

  constructor() {
    this.client = this.getClient();
  }

  /**************************************************************************************************
   * ユーザ系
   **************************************************************************************************/
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

  private getClient = (): AxiosInstance => {
    return axios.create({
      baseURL: this.baseUrl,
      headers: { "Content-Type": "application/json" },
      responseType: "json",
    });
  };
}

const apiInvoker = new AxiosFactory();

export default apiInvoker;
