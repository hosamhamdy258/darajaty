import { useQuery } from "@tanstack/react-query";
import APIClient from "../service/axios";

const apiClient = new APIClient("api/today_question");

const useQuestion = () =>
  useQuery({
    queryKey: ["question", "id"],
    queryFn: ({ signal }) => apiClient.get({ signal }),
  });

export default useQuestion;
