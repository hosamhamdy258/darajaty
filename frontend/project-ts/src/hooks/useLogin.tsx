import { UseMutationResult, useMutation } from "@tanstack/react-query";
import APIClient from "../service/axios";

const apiClient = new APIClient("api/auth/login/");

interface Variables {
  email?: string;
  password?: string;
}
interface Error {
  message: string;
  name: string;
  stack: string;
  code: string;
  status: number;
  response: {
    data: {
      [key: string]: string;
    };
  };
}

interface Data {
  expiry: string;
  token: string;
  user: User;
}
interface User {
  id: string;
  name: string;
  is_admin: boolean;
  email: string;
  phone: null;
  authenticated: boolean;
}

const useLogin = (): UseMutationResult<Data, Error, Variables, unknown> =>
  useMutation({
    mutationFn: apiClient.post,
  });

export default useLogin;
