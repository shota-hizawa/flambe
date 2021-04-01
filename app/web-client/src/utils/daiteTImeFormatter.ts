import { Dayjs } from "dayjs";
import { ElTableColumn } from "element-ui/types/table-column";

export function dateTimeFormatter<T extends { [index: string]: Dayjs }>(
  row: T,
  column: ElTableColumn
): string {
  return row[column.property].format("YYYY年MM月DD日 HH:mm:ss");
}
