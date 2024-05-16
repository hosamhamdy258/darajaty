import { useMutation } from "@tanstack/react-query";
import APIClient from "../service/axios";

const apiClient = new APIClient("api/auth/users/");

const useRegister = () =>
  useMutation({
    mutationFn: apiClient.post,
  });

export default useRegister;
