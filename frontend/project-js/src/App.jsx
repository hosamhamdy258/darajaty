import { Outlet } from "react-router-dom";
import NavBar from "./components/NavBar";

function App() {
  return (
    <>
      <NavBar></NavBar>
      <Outlet></Outlet>
    </>
  );
}

export default App;
