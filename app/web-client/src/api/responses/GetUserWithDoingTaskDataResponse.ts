import User from "@/models/User";
import DoingTaskData from "@/models/DoingTaskData";

export default interface GetUserWithDoingTaskDataResponse {
  user: User;
  doingTaskData: DoingTaskData;
}
