"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "../lib/api";
import { Bungee, Roboto_Condensed } from "next/font/google";

const bungee = Bungee({
  weight: "400",
  subsets: ["latin"],
});

const roboto = Roboto_Condensed({
  weight: ["300", "400", "700"],
  subsets: ["latin"],
});

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const router = useRouter();

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const selected = e.target.files?.[0];
    if (!selected) return;

    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setError(null);
  }

  async function handleUpload() {
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await api.post("/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      router.push(`/result/${res.data.job_id}`);
    } catch {
      setError("Upload failed. Check backend logs.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* BACKGROUND IMAGE */}
      <div
        className="absolute inset-0 bg-cover bg-center scale-110"
        style={{
          backgroundImage: "url('/ui-bg.png')",
        }}
      />

      {/* DARK OVERLAY */}
      <div className="absolute inset-0 bg-gradient-to-br from-black/70 via-black/50 to-black/80 backdrop-blur-[2px]" />

      {/* CONTENT */}
      <div className="relative z-10 flex items-center justify-center min-h-[85vh] px-6">
        <div
          className="
            w-full max-w-lg
            bg-purple-900/80
            rounded-2xl
            shadow-2xl
            p-8
            space-y-6
            border border-purple-500/40
            transition-all duration-300
            hover:shadow-[0_0_40px_rgba(168,85,247,0.6)]
            hover:border-purple-400
          "
        >
          <h2
            className={`text-3xl font-bold text-center text-white ${bungee.className}`}
          >
            Smart Image Moderation
          </h2>

          <p
            className={`text-sm text-white/80 text-center ${roboto.className}`}
          >
            Upload an image to analyze NSFW risk, faces, OCR text, and quality
            metrics in real time
          </p>

          <div className="space-y-4">
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className={`block w-full text-sm text-white
                file:mr-4 file:py-2 file:px-4
                file:rounded-lg file:border-0
                file:bg-purple-600 file:text-white
                hover:file:bg-purple-500
                transition
                ${roboto.className}`}
            />

            {preview && (
              <div className="rounded-lg overflow-hidden border border-white/20 bg-black">
                <img
                  src={preview}
                  alt="Preview"
                  className="w-full max-h-64 object-contain"
                />
              </div>
            )}

            <button
              onClick={handleUpload}
              disabled={!file || loading}
              className={`
                w-full py-3 rounded-lg font-semibold
                text-white
                transition-all duration-300
                ${
                  loading
                    ? "bg-purple-800 cursor-not-allowed"
                    : `
                      bg-purple-600
                      hover:bg-purple-500
                      hover:shadow-[0_0_25px_rgba(168,85,247,0.8)]
                      hover:scale-[1.02]
                      active:scale-[0.98]
                    `
                }
                ${bungee.className}
              `}
            >
              {loading ? "Processing..." : "Upload & Analyze"}
            </button>

            {error && (
              <div
                className={`text-red-300 text-sm text-center ${roboto.className}`}
              >
                {error}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* FOOTER */}
      <footer className="relative z-10 text-center pb-6">
        <p className={`text-sm text-white/70 ${roboto.className}`}>
          This project is CPU-only ML · Async Processing · Dockerized
        </p>
      </footer>
    </div>
  );
}
