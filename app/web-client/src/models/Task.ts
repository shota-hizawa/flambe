import { Dayjs } from "dayjs";

export default interface Task {
  id: number;
  title: string;
  description: string;
  status: string;
  priority: string;
  createdAt: Dayjs;
  updatedAt: Dayjs;
}

export const taskTitleMinLength = 1;
export const taskTitleMaxLength = 255;
export const taskDescriptionMaxLength = 255;
