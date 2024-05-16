import ms from "ms";
import { useEffect } from "react";
import useStore from "../service/store";
interface props {
  time: number;
}
export function ProgressBar({ time }: props) {
  const setProgress = useStore((state) => state.setProgress);

  useEffect(() => {
    const progressBar = document.getElementById("animated-progress");
    if (!progressBar) return;

    const animation = progressBar.animate(
      [
        { width: "100%", backgroundColor: "#198754" }, // green
        { backgroundColor: "#ffc107" }, // yellow
        { width: "0%", backgroundColor: "#dc3545" }, // red
      ],
      {
        duration: ms(`${time}s`), // 30 seconds
        easing: "linear",
      }
    );

    const handleAnimationFinish = () => {
      setProgress("0%");
    };

    animation.onfinish = handleAnimationFinish;

    return () => {
      animation.removeEventListener("finish", handleAnimationFinish);
      animation.cancel();
    };
  }, []);

  return (
    <div>
      <div className="progress my-3">
        <div
          id="animated-progress"
          className="progress-bar"
          style={{
            width: "100%",
            // animation: "progressBarAnimation 3s linear",
          }}
        ></div>
      </div>
    </div>
  );
}
