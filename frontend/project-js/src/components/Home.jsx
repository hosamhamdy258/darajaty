import { Link, useLocation, useNavigate } from "react-router-dom";
import color from "../service/ThemeColor";
import { useEffect } from "react";


function Home() {
  const navigate = useNavigate();
  const location = useLocation();
  const url = location.state?.url;

  useEffect(() => {
    if (url) {
      navigate(url);
    }
  })

  const cards = [
    "Today Question",
    // "Rewards",
    "Add Questions",
    "Rules",
    // "Review Questions",
    "Coming Soon",
  ];

  return (
    <>
      <div className="container text-center">
        <div className="row row-cols-1">
          {cards.map((value) => (
            <div className="col" key={value}>
              <Link
                className={`card btn btn-outline-${color} border-${color} p-3 mx-1 my-3 fw-semibold`}
                to={value.toLowerCase().replace(/ /g, "-")}
              >
                {value}
              </Link>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default Home;
