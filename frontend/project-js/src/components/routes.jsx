import { createBrowserRouter } from "react-router-dom";
import App from "../App";
import ErrorPage from "./ErrorPage";
import Home from "./Home";
import LoginUserRoute from "./LoginUserRoute";
import { PrivatePaths, publicPaths } from "./paths";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <Home /> },
      ...publicPaths,
      {
        element: <LoginUserRoute />,
        children: [...PrivatePaths],
      },
    ],
  },
]);

export default router;
