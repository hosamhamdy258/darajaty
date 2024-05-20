import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    // port: 3000,
  },
  build: {
    // eslint-disable-next-line no-undef
    outDir: path.resolve(__dirname, 'templates/dist'), // Ensure output directory matches Docker volume
    rollupOptions: {
      output: {
        entryFileNames: "assets/index.js",
        assetFileNames: "assets/style.css",
        chunkFileNames: "assets/chunk.js",
      },
    },
  },
});
