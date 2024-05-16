import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import color from "../service/ThemeColor";

function Redirect({ msg }) {
  const navigate = useNavigate();
  const handleBackToHome = () => {
    navigate("/");
  };
  return (
    <div className="container">
      <p className="text-center my-3 fs-4">{msg}</p>
      <div className="d-flex justify-content-center">
        <button className={`btn btn-${color}`} onClick={handleBackToHome}>
          Back to Home
        </button>
      </div>
    </div>
  );
}
Redirect.propTypes = {
  msg: PropTypes.string,
};
export default Redirect;
