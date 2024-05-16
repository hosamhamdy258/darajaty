import color from "../service/ThemeColor";

function Loading() {
  return (
    <div className={`container text-${color} text-center my-3`}>
      <div
        className="spinner-border"
        style={{ width: "4rem", height: "4rem" }}
        role="status"
      >
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
  );
}

export default Loading;
