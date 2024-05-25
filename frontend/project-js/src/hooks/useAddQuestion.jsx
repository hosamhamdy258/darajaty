import { useMutation } from "@tanstack/react-query";
import APIClient from "../service/axios";

const apiClient = new APIClient("api/questions/");

const useAddQuestion = () =>
  useMutation({
    mutationFn: apiClient.post,
  });

export default useAddQuestion;
