import { useEffect } from "react";
import useStore from "../service/store";
import Redirect from "./Redirect";

function Logout() {
  // TODO fix Logout Message
  const { reset } = useStore();
  useEffect(() => {
    sessionStorage.removeItem("token");
    reset();
  }, []);

  return <Redirect CenterMessage="Logged Out Successfully" />;
}

export default Logout;
