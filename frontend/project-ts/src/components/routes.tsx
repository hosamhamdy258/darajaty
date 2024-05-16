import { createBrowserRouter } from "react-router-dom";
import App from "../App";
import ErrorPage from "./ErrorPage";
import Questions from "./Questions";
import Home from "./Home";
import Rewards from "./Rewards";
import AddQuestions from "./AddQuestions";
import Rules from "./Rules";
import ReviewQuestions from "./ReviewQuestions";
import ComingSoon from "./ComingSoon";
import Register from "./Register";
import LoginUserRoute from "./LoginUserRoute";
import Login from "./Login";
import Logout from "./Logout";
import Transactions from "./Transactions";
import Profile from "./Profile";
type paths = {
  path: string;
  element: JSX.Element;
}[];
function UrlFixer(paths: paths): void {
  paths.map((route) => {
    route.path = route.path.trim().toLowerCase().replace(/ /g, "-");

    return route;
  });
}

const publicPaths = [
  { path: "rewards", element: <Rewards /> },
  { path: "rules", element: <Rules /> },
  { path: "coming soon", element: <ComingSoon /> },
  { path: "Signup", element: <Register /> },
  { path: "Login", element: <Login /> },
];
const PrivatePaths = [
  { path: "Question of the day", element: <Questions /> },
  { path: "Add Questions", element: <AddQuestions /> },
  { path: "Review Questions", element: <ReviewQuestions /> },
  { path: "Transactions", element: <Transactions /> },
  { path: "Profile", element: <Profile /> },
  { path: "logout", element: <Logout /> },
];

UrlFixer(publicPaths);
UrlFixer(PrivatePaths);

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
