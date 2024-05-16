import { UseQueryResult, useQuery } from "@tanstack/react-query";
import APIClient from "../service/axios";
import ms from "ms";

const apiClient = new APIClient("api/today_question");
interface Error {
  message: string;
  name: string;
  stack: string;
  code: string;
  status: number;
  response: Response;
}

interface Response {
  data: ErrorData;
  status: number;
  statusText: string;
  headers: Headers;
}

interface ErrorData {
  [key: string]: string;
}

export interface Data {
  id: string;
  question: string;
  choices_set: QuestionChoice[];
  time: number;
}
export interface QuestionChoice {
  id: string;
  choice: string;
}

const useQuestion = (): UseQueryResult<Data, Error> =>
  useQuery({
    queryKey: ["question", "id"],
    queryFn: ({ signal }) => apiClient.get({ signal }),
    // staleTime: ms("5s"),
    cacheTime: ms("0s"),
  });

export default useQuestion;
