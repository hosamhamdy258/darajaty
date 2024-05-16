import { create } from "zustand";
import { immer } from "zustand/middleware/immer";
import { mountStoreDevtool } from "simple-zustand-devtools";

export interface User {
  id: string;
  name: string;
  is_admin: boolean;
  email: string;
  phone: string | null;
  authenticated: boolean;
}

interface State {
  user: User;
  progress: string;
}

interface Actions {
  update: (user: User) => void;
  reset: () => void;
  setProgress: (progress: string) => void;
}
const initData = {
  id: "",
  name: "",
  is_admin: false,
  email: "",
  phone: "",
  authenticated: false,
};
const useStore = create(
  immer<State & Actions>((set) => ({
    user: {
      ...initData,
    },

    update: (user) =>
      set((state) => {
        state.user = user;
      }),
    reset: () =>
      set((state) => {
        state.user = initData;
      }),
    progress: "100%",
    setProgress: (progress) =>
      set((state) => {
        state.progress = progress;
      }),
  }))
);

if (process.env.NODE_ENV === "development") {
  mountStoreDevtool("Store", useStore);
}

export default useStore;
