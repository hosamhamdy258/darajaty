import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import z from "zod";
import useRegister from "../hooks/useRegister";
import color from "../service/ThemeColor";
import Redirect from "./Redirect";
const regex = /^01[0125][0-9]{8}$/gm;
const schema = z.object({
  email: z
    .string()
    .min(1, { message: "required" })
    .max(100, { message: "Must be 100 or fewer characters long" }),
  password: z
    .string()
    .min(1, { message: "required" })
    .max(100, { message: "Must be 100 or fewer characters long" }),
  name: z
    .string()
    .min(1, { message: "required" })
    .max(100, { message: "Must be 100 or fewer characters long" }),
  phone: z
    .string()
    .length(11, { message: "Must be 11 characters" })
    .regex(regex, { message: "Must be valid Egyptian mobile number" }),
});

function Register() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({ resolver: zodResolver(schema) });
  const { mutate, isPending, error, isSuccess } = useRegister();
  if (isSuccess) {
    return <Redirect CenterMessage="You're Registered Successfully" />;
  }

  const onSubmit = (data) =>
    mutate({
      email: data.email,
      password: data.password,
      name: data.name,
      phone: data.phone,
    });
  return (
    <div className="container">
      <form className="row my-3" onSubmit={handleSubmit(onSubmit)}>
        <div>
          <label className="form-label" htmlFor="name">
            Name
          </label>
          <input
            {...register("name")}
            className="form-control"
            type="text"
            id="name"
          />
          {errors.name?.message && (
            <p className="text-danger">{errors.name?.message}</p>
          )}
        </div>
        <div>
          <label className="form-label" htmlFor="phone">
            Phone
          </label>
          <input
            {...register("phone")}
            className="form-control"
            type="text"
            id="phone"
          />
          {errors.phone?.message && (
            <p className="text-danger">{errors.phone?.message}</p>
          )}
        </div>
        <div>
          <label className="form-label" htmlFor="email">
            Email
          </label>
          <input
            {...register("email")}
            className="form-control"
            type="email"
            id="email"
          />
          {errors.email?.message && (
            <p className="text-danger">{errors.email?.message}</p>
          )}

          {error?.response?.data.email && (
            <p className="text-danger">{error?.response?.data.email}</p>
          )}
        </div>
        <div>
          <label className="form-label" htmlFor="password">
            Password
          </label>
          <input
            {...register("password")}
            className="form-control"
            type="password"
            id="password"
          />
          {errors.password?.message && (
            <p className="text-danger">{errors.password?.message}</p>
          )}
          {error?.response?.data.password &&
            error?.response?.data.password.map((k) => (
              <p key={k} className="text-danger">
                {k}
              </p>
            ))}
        </div>
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
                  <span className="mx-2 text-nowrap">Sign up ...</span>
                </>
              ) : (
                "Sign up"
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default Register;
