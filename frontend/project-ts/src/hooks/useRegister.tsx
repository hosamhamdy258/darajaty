import {
  MutationFunction,
  UseMutationResult,
  useMutation,
} from "@tanstack/react-query";
import APIClient from "../service/axios";

const apiClient = new APIClient("api/auth/users/");

interface Variables {
  email: string;
  password: string;
  name: string;
  phone: string;
}
interface Data {
  name: string;
  email: string;
  phone: string;
}

interface Error {
  message: string;
  name: string;
  stack: string;
  code: string;
  status: number;
  response: {
    data: {
      [key: string]: [string];
    };
  };
}

const useRegister = (): UseMutationResult<Data, Error, Variables, unknown> =>
  useMutation({
    mutationFn: apiClient.post as MutationFunction<Data, Variables>,
  });

export default useRegister;
