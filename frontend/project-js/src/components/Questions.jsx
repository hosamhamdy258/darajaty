import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import z from "zod";
import useAnswer from "../hooks/useAnswer";
import useQuestion from "../hooks/useQuestion";
import Loading from "./Loading";
import { ProgressBar } from "./ProgressBar";
import Redirect from "./Redirect";
import color from "../service/ThemeColor";
import useStore from "../service/store";
import React, { useEffect } from "react";
import PropTypes from "prop-types";

function Questions() {
  const { data, isPending, error } = useQuestion();
  const setProgress = useStore((state) => state.setProgress);

  useEffect(() => {
    return () => {
      setProgress("100%");
    };
  }, []);

  if (error) {
    return <Redirect CenterMessage={error.response.data.detail} />;
  }

  if (isPending) return <Loading />;
  return <QuestionsForm questionData={data} />;
}

const schema = z.object({
  answer: z.string({
    invalid_type_error: "Please choose one of the answers",
  }),
});

function QuestionsForm({ questionData }) {
  const { id, question, choices_set, time } = questionData;

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(schema) });

  const { mutate, isPending, isSuccess, isError, data } = useAnswer();

  const onSubmit = (data) => {
    mutate({ fk_choice: data.answer, fk_question: id });
  };
  const progress = useStore((state) => state.progress);
  const setPoints = useStore((state) => state.setPoints);
  const buttonUrl = "/today-question";
  const buttonMessage = "Another Question";

  if (progress == "0%") {
    return (
      <Redirect
        CenterMessage="You didn't answer in time."
        buttonMessage={buttonMessage}
        buttonUrl={buttonUrl}
      />
    );
  }

  if (isSuccess) {
    setPoints(data["wallet"]);
    const CenterMessage = `Your Answer is ${
      data["correct"] ? "correct" : "wrong"
    }`;
    return (
      <Redirect
        CenterMessage={CenterMessage}
        buttonMessage={buttonMessage}
        buttonUrl={buttonUrl}
      />
    );
  }
  if (isError) {
    return (
      <Redirect
        CenterMessage={"Error CenterMessage"}
        buttonMessage={buttonMessage}
        buttonUrl={buttonUrl}
      />
    );
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
              disabled={isPending}
            >
              {isPending ? (
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

QuestionsForm.propTypes = {
  questionData: PropTypes.object,
};

export default Questions;
