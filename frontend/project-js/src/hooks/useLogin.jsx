import { useMutation } from "@tanstack/react-query";
import APIClient from "../service/axios";

const apiClient = new APIClient("api/auth/login/");

const useLogin = () =>
  useMutation({
    mutationFn: apiClient.post,
  });

export default useLogin;
