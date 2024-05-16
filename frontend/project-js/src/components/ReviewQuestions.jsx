import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import z from "zod";
import color from "../service/ThemeColor";
const schema = z.object({
  answer: z.string({
    invalid_type_error: "Please choose correct/wrong",
  }),
  answer1: z.string({
    invalid_type_error: "Please choose correct/wrong",
  }),
  answer2: z.string({
    invalid_type_error: "Please choose correct/wrong",
  }),
});

function ReviewQuestions() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(schema) });

  const onSubmit = (data) => console.log(data);
  return (
    <div className="container">
      <form className="row my-3" onSubmit={handleSubmit(onSubmit)}>
        <div className="fs-4 d-block">
          Lorem ipsum dolor, sit amet consectetur adipisicing elit. Molestias,
          iste?
        </div>
        <div className="mt-5">Is this choice is the correct answer ?</div>

        <div className="btn-group my-2 col-12">
          <div className="input-group-text text-wrap col-8">
            Lorem ipsum dolor sit
          </div>

          <input
            {...register("answer")}
            type="radio"
            className="btn-check "
            id="btnradio1"
            value="true"
          />
          <label
            className={`btn btn-outline-${color} d-flex align-items-center justify-content-center`}
            htmlFor="btnradio1"
          >
            correct
          </label>

          <input
            {...register("answer")}
            type="radio"
            className="btn-check"
            id="btnradio2"
            value="false"
          />
          <label
            className={`btn btn-outline-${color} d-flex align-items-center justify-content-center`}
            htmlFor="btnradio2"
          >
            wrong
          </label>
        </div>

        {errors.answer?.message && (
          <p className="text-danger">{errors.answer?.message}</p>
        )}

        <div className="mt-5">
          Is this choices relative to the correct answer ?
        </div>

        <div className="btn-group my-2 col-12">
          <div className="input-group-text text-wrap col-8">
            Lorem ipsum dolor sit
          </div>

          <input
            {...register("answer1")}
            type="radio"
            className="btn-check "
            id="btnradio3"
            value="true"
          />
          <label
            className={`btn btn-outline-${color} d-flex align-items-center justify-content-center`}
            htmlFor="btnradio3"
          >
            correct
          </label>

          <input
            {...register("answer1")}
            type="radio"
            className="btn-check"
            id="btnradio4"
            value="false"
          />
          <label
            className={`btn btn-outline-${color} d-flex align-items-center justify-content-center`}
            htmlFor="btnradio4"
          >
            wrong
          </label>
        </div>
        {errors.answer1?.message && (
          <p className="text-danger">{errors.answer1?.message}</p>
        )}
        <div className="btn-group my-2 col-12">
          <div className="input-group-text text-wrap col-8">
            Lorem ipsum dolor sit1
          </div>

          <input
            {...register("answer2")}
            type="radio"
            className="btn-check "
            id="btnradio5"
            value="true"
          />
          <label
            className={`btn btn-outline-${color} d-flex align-items-center justify-content-center`}
            htmlFor="btnradio5"
          >
            correct
          </label>

          <input
            {...register("answer2")}
            type="radio"
            className="btn-check"
            id="btnradio6"
            value="false"
          />
          <label
            className={`btn btn-outline-${color} d-flex align-items-center justify-content-center`}
            htmlFor="btnradio6"
          >
            wrong
          </label>
        </div>
        {errors.answer2?.message && (
          <p className="text-danger">{errors.answer2?.message}</p>
        )}

        <div className="col-12">
          <div className="row justify-content-center m-3">
            <button className={`btn btn-${color} col-4`} type="submit">
              Submit Answer
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default ReviewQuestions;
