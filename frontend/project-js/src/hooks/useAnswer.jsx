import { useMutation } from "@tanstack/react-query";
import APIClient from "../service/axios";

const apiClient = new APIClient("api/today_answer/");

const useAnswer = () =>
  useMutation({
    mutationFn: apiClient.post,
  });

export default useAnswer;
