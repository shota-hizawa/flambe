export default interface PaginatedResponse<T> {
  items: Array<T>;
  total: number;
  page: number;
  size: number;
}
