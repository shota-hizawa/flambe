import User from "@/models/User";
import Task from "@/models/Task";

export default interface TaskWithAssignees extends Task {
  assignees: Array<User>;
}
