import { ElTableColumn } from "element-ui/types/table-column";

export enum TaskStatus {
  TODO = "TODO",
  DOING = "DOING",
  DONE = "DONE",
}

export const taskStatusDisplayNames = new Map([
  [TaskStatus.TODO, "作業前"],
  [TaskStatus.DOING, "作業中"],
  [TaskStatus.DONE, "完了"],
]) as ReadonlyMap<TaskStatus, string>;

export function taskStatusFormatter<T extends { [index: string]: TaskStatus }>(
  row: T,
  column: ElTableColumn
): string {
  return taskStatusDisplayNames.get(
    row[column.property] as TaskStatus
  ) as string;
}
