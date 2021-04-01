export default interface User {
  id: number;
  username: string;
}

export const usernameMinLength = 4;
export const usernameMaxLength = 100;
export const userPasswordMinLength = 8;
export const userPasswordMaxLength = 100;
