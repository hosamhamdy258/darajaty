import { NavLink } from "react-router-dom";
import useStore from "../service/store";
import color from "../service/ThemeColor";

function NavBar() {
  const user = useStore((state) => state.user);

  return (
    <div className="container ">
      <nav className={`navbar navbar-expand-lg border rounded border-${color}`}>
        <div className="container ">
          <NavLink className="navbar-brand" to={"/"}>
            Darajaty
          </NavLink>
          {user.authenticated && (
            <div className="row text-center text-truncate w-50">
              <div className="col">{user.name} </div>
              <div className="col text-success">Points : {user.wallet}</div>
            </div>
          )}
          <button
            className={`navbar-toggler btn btn-${color} border-${color}`}
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
              <li className={`nav-item btn btn-outline-${color} border-0`}>
                <NavLink className="nav-link" to={"/"}>
                  Home
                </NavLink>
              </li>
              {!user.authenticated && (
                <>
                  <li className={`nav-item btn btn-outline-${color} border-0`}>
                    <NavLink className="nav-link" to={"/sign-up"}>
                      Register
                    </NavLink>
                  </li>
                  <li className={`nav-item btn btn-outline-${color} border-0`}>
                    <NavLink className="nav-link" to={"/login"}>
                      Login
                    </NavLink>
                  </li>
                </>
              )}
              {user.authenticated && (
                <>
                  <li className={`nav-item btn btn-outline-${color} border-0`}>
                    <NavLink className="nav-link" to={"/profile"}>
                      Profile
                    </NavLink>
                  </li>
                  <li className={`nav-item btn btn-outline-${color} border-0`}>
                    <NavLink className="nav-link" to={"/logout"}>
                      Logout
                    </NavLink>
                  </li>
                </>
              )}
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default NavBar;
