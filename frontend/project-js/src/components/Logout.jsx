import { useEffect } from "react";
import useStore from "../service/store";
import Redirect from "./Redirect";

function Logout() {
  const { reset } = useStore();
  useEffect(() => {
    sessionStorage.removeItem("token");
    reset();
  }, []);

  return <Redirect msg="Logged Out Successfully" />;
}

export default Logout;
