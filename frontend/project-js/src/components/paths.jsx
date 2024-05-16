import Questions from "./Questions";
import AddQuestions from "./AddQuestions";
import ReviewQuestions from "./ReviewQuestions";
import Logout from "./Logout";
import Transactions from "./Transactions";
import Profile from "./Profile";
import Rewards from "./Rewards";
import Rules from "./Rules";
import ComingSoon from "./ComingSoon";
import Register from "./Register";
import Login from "./Login";
import UrlFixer from "../utilities/urls";

export const PrivatePaths = [
  { path: "Question of the day", element: <Questions /> },
  { path: "Add Questions", element: <AddQuestions /> },
  { path: "Review Questions", element: <ReviewQuestions /> },
  { path: "Transactions", element: <Transactions /> },
  { path: "Profile", element: <Profile /> },
  { path: "logout", element: <Logout /> },
];

export const publicPaths = [
  { path: "rewards", element: <Rewards /> },
  { path: "rules", element: <Rules /> },
  { path: "coming soon", element: <ComingSoon /> },
  { path: "Sign up", element: <Register /> },
  { path: "Login", element: <Login /> },
];

UrlFixer(publicPaths);
UrlFixer(PrivatePaths);
