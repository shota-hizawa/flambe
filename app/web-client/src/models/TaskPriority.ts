import { ElTableColumn } from "element-ui/types/table-column";

export enum TaskPriority {
  HIGH = "HIGH",
  MEDIUM = "MEDIUM",
  LOW = "LOW",
}

export const taskPriorityDisplayNames = new Map([
  [TaskPriority.HIGH, "高"],
  [TaskPriority.MEDIUM, "中"],
  [TaskPriority.LOW, "低"],
]) as ReadonlyMap<TaskPriority, string>;

export function taskPriorityFormatter<
  T extends { [index: string]: TaskPriority }
>(row: T, column: ElTableColumn): string {
  return taskPriorityDisplayNames.get(
    row[column.property] as TaskPriority
  ) as string;
}
