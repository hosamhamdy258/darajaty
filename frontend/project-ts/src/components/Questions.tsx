import { zodResolver } from "@hookform/resolvers/zod";
import { SubmitHandler, useForm } from "react-hook-form";
import z from "zod";
import useAnswer from "../hooks/useAnswer";
import useQuestion, { Data } from "../hooks/useQuestion";
import Loading from "./Loading";
import { ProgressBar } from "./ProgressBar";
import Redirect from "./Redirect";
import color from "../service/ThemeColor";
import useStore from "../service/store";
import React, { useEffect } from "react";

function Questions() {
  const { data, isLoading, error } = useQuestion();
  const setProgress = useStore((state) => state.setProgress);

  useEffect(() => {
    return () => {
      setProgress("100%");
    };
  }, []);

  if (error) {
    return <Redirect msg={error.response.data.detail} />;
  }

  if (isLoading) return <Loading />;
  return <QuestionsForm questionData={data} />;
}

const schema = z.object({
  answer: z.string({
    invalid_type_error: "Please choose one of the answers",
  }),
});

type FormData = z.infer<typeof schema>;

function QuestionsForm({ questionData }: { questionData: Data }) {
  const { id, question, choices_set, time } = questionData;
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const { mutate, isLoading, isSuccess, isError, data } = useAnswer();

  const onSubmit: SubmitHandler<FormData> = (data) => {
    mutate({ fk_choice: data.answer, fk_question: id });
  };
  const progress = useStore((state) => state.progress);
  if (progress == "0%") {
    return <Redirect msg="You didn't answer in time." />;
  }

  if (isSuccess) {
    return (
      <Redirect
        msg={`Your Answer is ${data["correct"] ? "correct" : "wrong"}`}
      />
    );
  }
  if (isError) {
    return <Redirect msg={"Error msg"} />;
  }

  return (
    <div className="container">
      <form className="row my-3" onSubmit={handleSubmit(onSubmit)}>
        <p className="text-center fs-4">{question}</p>
        <ProgressBar time={time} />
        <div
          className="btn-group-vertical col-12"
          role="group"
          aria-label="Basic radio toggle button group"
        >
          {choices_set.map((choice, index) => (
            <React.Fragment key={index}>
              <input
                {...register("answer")}
                type="radio"
                className="btn-check"
                id={choice.id}
                value={choice.id}
              />
              <label className={`btn btn-outline-${color}`} htmlFor={choice.id}>
                {choice.choice}
              </label>
            </React.Fragment>
          ))}
        </div>
        {errors.answer?.message && (
          <div className="alert alert-danger col-10 my-2 mx-auto" role="alert">
            {errors.answer?.message}
          </div>
        )}

        <div className="col-12">
          <div className="row justify-content-center m-3">
            <button
              className={`btn btn-${color} col-4`}
              type="submit"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <span
                    className="spinner-border spinner-border-sm"
                    role="status"
                    aria-hidden="true"
                  ></span>
                  <span className="mx-2 text-nowrap">
                    Submitting Answer ...
                  </span>
                </>
              ) : (
                "Submit Answer"
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default Questions;
