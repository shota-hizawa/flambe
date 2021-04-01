import User from "@/models/User";
import DoingTaskData from "@/models/DoingTaskData";
import Task from "@/models/Task";

export default interface GetUserWithDoingTaskDataResponse {
  user: User;
  doingTaskData: DoingTaskData;
  incompleteTasks: Array<Task>;
}
