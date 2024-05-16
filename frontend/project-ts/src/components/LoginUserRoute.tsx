import { Navigate, Outlet } from "react-router-dom";
import useStore from "../service/store";

function LoginUserRoute() {
  const user = useStore((state) => state.user);
  if (!user.authenticated) {
    return <Navigate to={"/login"} />;
  }
  return <Outlet />;
}

export default LoginUserRoute;
