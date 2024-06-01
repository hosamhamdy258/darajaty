import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import color from "../service/ThemeColor";

function Redirect({ CenterMessage, buttonMessage, buttonUrl }) {
  const navigate = useNavigate();
  const handleBackToHome = () => {
    navigate("/");
  };
  const handleRedirect = () => {
    navigate("/", { state: { url: buttonUrl } });
  };
  return (
    <div className="container">
      <p className="text-center my-3 fs-4">{CenterMessage}</p>
      <div className="d-flex justify-content-center">
        <button className={`btn btn-${color} mx-1`} onClick={handleBackToHome}>
          Back to Home
        </button>
        {(buttonMessage && buttonUrl) ?
          <button className={`btn btn-${color} mx-1`} onClick={handleRedirect}>
            {buttonMessage}
          </button>
          : ""
        }
      </div>
    </div>
  );
}
Redirect.propTypes = {
  CenterMessage: PropTypes.string,
  buttonMessage: PropTypes.string,
  buttonUrl: PropTypes.string
};
export default Redirect;
