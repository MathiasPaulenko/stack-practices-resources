import { apiClient } from "@/api/client";
import { User } from "@/api/users";

export const UserService = {
  async getAll(): Promise<User[]> {
    const res = await apiClient.get<User[]>("/users");
    return res.data;
  },
  async create(payload: { name: string }): Promise<User> {
    const res = await apiClient.post<User>("/users", payload);
    return res.data;
  },
};
