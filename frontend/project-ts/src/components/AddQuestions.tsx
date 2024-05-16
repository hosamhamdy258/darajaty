import { zodResolver } from "@hookform/resolvers/zod";
import { SubmitHandler, useForm } from "react-hook-form";
import z from "zod";
import color from "../service/ThemeColor";
const schema = z.object({
  question: z
    .string()
    .min(1, { message: "required" })
    .max(300, { message: "Must be 300 or fewer characters long" }),
  correct_choice: z
    .string()
    .min(1, { message: "required" })
    .max(100, { message: "Must be 100 or fewer characters long" }),
  extra_choice1: z
    .string()
    .min(1, { message: "required" })
    .max(100, { message: "Must be 100 or fewer characters long" }),
  extra_choice2: z
    .string()
    .min(1, { message: "required" })
    .max(100, { message: "Must be 100 or fewer characters long" }),
});

type FormData = z.infer<typeof schema>;
function AddQuestions() {
  const choices: Array<keyof FormData> = [
    "correct_choice",
    "extra_choice1",
    "extra_choice2",
  ];
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({ resolver: zodResolver(schema) });
  const onSubmit: SubmitHandler<FormData> = (data) => console.log(data);

  return (
    <div className="container">
      <p>fill this form to add question </p>
      <form className="row" onSubmit={handleSubmit(onSubmit)}>
        <div className="form-floating mb-5">
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
            <p className="text-danger">{errors.question?.message}</p>
          )}
        </div>
        {choices.map((value) => (
          <div className="form-floating my-1" key={value}>
            <input
              className="form-control"
              id={value}
              type="text"
              placeholder=""
              autoComplete="off"
              {...register(value)}
            />
            <label className="mx-2" htmlFor={value}>
              {value}
            </label>
            {errors[value]?.message && (
              <p className="text-danger">{errors[value]?.message}</p>
            )}
          </div>
        ))}
        <div className="col-12">
          <div className="row justify-content-center m-3">
            <button className={`btn btn-${color} col-4`} type="submit">
              Submit Question
            </button>
          </div>
        </div>{" "}
      </form>
    </div>
  );
}

export default AddQuestions;
