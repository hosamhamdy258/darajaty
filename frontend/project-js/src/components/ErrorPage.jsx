import Redirect from "./Redirect";
export default function ErrorPage() {
  // const error = useRouteError();
  // console.error(error);

  return (
    <div id="error-page" className="container">
      <div className="row text-center my-3 fs-3">
        <div className="col">
          <h1>Oops!</h1>
          <p>Sorry, an unexpected error has occurred.</p>
          <Redirect />
        </div>
      </div>
    </div>
  );
}
