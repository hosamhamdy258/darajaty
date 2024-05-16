import { zodResolver } from "@hookform/resolvers/zod";
import { SubmitHandler, useForm } from "react-hook-form";
import z from "zod";
import useLogin from "../hooks/useLogin";
import useStore from "../service/store";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import color from "../service/ThemeColor";

const schema = z.object({
  email: z
    .string()
    .min(1, { message: "required" })
    .max(300, { message: "Must be 300 or fewer characters long" }),
  password: z
    .string()
    .min(1, { message: "required" })
    .max(100, { message: "Must be 100 or fewer characters long" }),
});

type FormData = z.infer<typeof schema>;

function Login() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({ resolver: zodResolver(schema) });
  const { mutate, isLoading, data, isSuccess, error } = useLogin();
  const { user, update } = useStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (isSuccess) {
      data.user["authenticated"] = true;
      sessionStorage.setItem("token", "token " + data.token);
      update(data.user);
      navigate("/");
    }
  }, [isSuccess]);
  useEffect(() => {
    if (user.authenticated) {
      navigate("/");
    }
  }, []);

  const onSubmit: SubmitHandler<FormData> = (data) =>
    mutate({ email: data.email, password: data.password });

  return (
    <div className="container">
      <form className="row my-3" onSubmit={handleSubmit(onSubmit)}>
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
        </div>
        {error?.response?.data.non_field_errors && (
          <p className="text-danger text-center my-2">
            {error?.response?.data.non_field_errors}
          </p>
        )}
        {error?.code == "ERR_NETWORK" && (
          <p className="text-danger text-center my-2">
            Check device connection is working or server is running
          </p>
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
                  <span className="mx-2 text-nowrap">Login ...</span>
                </>
              ) : (
                "Login"
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default Login;
