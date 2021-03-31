import User from "@/models/user";
import DoingTaskData from "@/models/DoingTaskData";

export default interface GetUserWithDoingTaskDataResponse {
  user: User;
  doingTaskData: DoingTaskData;
}
