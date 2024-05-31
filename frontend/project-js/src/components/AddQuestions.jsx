import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import z from "zod";
import color from "../service/ThemeColor";
import useAddQuestion from '../hooks/useAddQuestion';
import Redirect from './Redirect';
const schema = z.object({
  question: z
    .string()
    .min(1, { message: "required" })
    .max(300, { message: "Must be 300 or fewer characters long" }),
  correct_choice: z
    .string()
    .min(1, { message: "required" })
    .max(100, { message: "Must be 100 or fewer characters long" }),
  extra_choice_1: z
    .string()
    .min(1, { message: "required" })
    .max(100, { message: "Must be 100 or fewer characters long" }),
  extra_choice_2: z
    .string()
    .min(1, { message: "required" })
    .max(100, { message: "Must be 100 or fewer characters long" }),
});

function AddQuestions() {
  const choices = ["correct_choice", "extra_choice_1", "extra_choice_2"];
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(schema) });
  const { mutate, isPending, isSuccess, error } = useAddQuestion();

  const onSubmit = (data) => {
    mutate({
      "question": data.question,
      "choices_set": [
        { "choice": data.correct_choice, "correct": true },
        { "choice": data.extra_choice_1, },
        { "choice": data.extra_choice_2, }
      ]
    });
  };

  if (isSuccess) {
    return (
      <Redirect
        msg={`Question Added Successfully`}
      />
    );
  }

  return (
    <div className="container">
      <p className="my-3">fill this form to add question </p>
      <form className="row" onSubmit={handleSubmit(onSubmit)}>
        <div className="form-floating mb-1">
          <textarea
            className="form-control"
            id="questionInput"
            placeholder=""
            autoComplete="off"
            {...register("question")}
          />

          <label className="mx-2" htmlFor="questionInput">
            Type Question
          </label>
          {errors.question?.message && (
            <div>
              <span className="text-danger">{errors.question?.message}</span>
            </div>
          )}
        </div>

        {error?.response?.data &&
          Object.values(error?.response?.data || {}).flat().map((value, index) => (
            <div className="alert alert-danger col-10 my-2 mx-auto" role="alert" key={index}>
              {value}
            </div>
          ))
        }

        {choices.map((value) => (
          <div className="form-floating mb-1" key={value}>
            <input
              className="form-control"
              id={value}
              type="text"
              placeholder=""
              autoComplete="off"
              {...register(value)}
            />
            <label className="mx-2" htmlFor={value}>
              {value.replace(/_/g, " ")}
            </label>
            {errors[value]?.message && (
              <div>
                <span className="text-danger">{errors[value]?.message}</span>
              </div>
            )}
          </div>
        ))}
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
                    Submitting Question ...
                  </span>
                </>
              ) : (
                "Submit Question"
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default AddQuestions;
