import { Dayjs } from "dayjs";
import User from "@/models/User";

export interface Task {
  id: number;
  title: string;
  description: string;
  status: string;
  priority: string;
  createdAt: Dayjs;
  updatedAt: Dayjs;
  assignees: Array<User>;
}
