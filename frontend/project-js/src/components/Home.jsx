import { Link } from "react-router-dom";
import color from "../service/ThemeColor";
function Home() {
  const cards = [
    "Question Of The Day",
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
