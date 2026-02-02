"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "../../../lib/api";
import { Bungee, Roboto_Condensed } from "next/font/google";

const bungee = Bungee({
  weight: "400",
  subsets: ["latin"],
});

const roboto = Roboto_Condensed({
  weight: ["300", "400", "700"],
  subsets: ["latin"],
});

export default function ResultPage() {
  const params = useParams();
  const jobId = params.jobId as string;

  const [data, setData] = useState<any>(null);
  const [status, setStatus] = useState("pending");

  useEffect(() => {
    if (!jobId) return;

    const interval = setInterval(async () => {
      try {
        const res = await api.get(`/result/${jobId}`);
        setStatus(res.data.status);

        if (res.data.status === "success") {
          setData(res.data.result);
          clearInterval(interval);
        }
      } catch (err) {
        console.error("Polling failed", err);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobId]);

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
      <div className="relative z-10 flex items-center justify-center min-h-screen px-6">
        <div className="w-full max-w-2xl bg-purple-900/80 rounded-2xl shadow-2xl p-8 space-y-6 border border-purple-500/40">

          <h1
            className={`text-4xl text-center text-white ${bungee.className}`}
          >
            Analysis Results
          </h1>

          <p
            className={`text-sm text-center break-all ${roboto.className}`}
          >
            <span className="text-white/70">Job ID:</span>{" "}
            <span className="text-white font-semibold drop-shadow-[0_0_6px_rgba(255,255,255,0.6)]">
              {jobId}
            </span>
          </p>

          <div className="bg-purple-800/60 rounded-lg p-4 text-center">
            <p className={`text-white ${roboto.className}`}>
              Status: <span className="font-semibold">{status}</span>
            </p>
          </div>

          {data && (
            <div className="grid md:grid-cols-2 gap-4">
              <ResultCard title="NSFW">
                {data.nsfw ? "⚠️ NSFW" : "✅ Safe"}
              </ResultCard>

              <ResultCard title="Faces Detected">
                {data.faces_detected}
              </ResultCard>

              <ResultCard title="Blur Score">
                {data.blur_score}
              </ResultCard>

              <ResultCard title="Quality Score">
                {data.quality_score}
              </ResultCard>

              <ResultCard title="Processing Time">
                {data.processing_time}s
              </ResultCard>

              <ResultCard title="OCR Text">
                <pre className="whitespace-pre-wrap text-sm">
                  {data.ocr_text || "No text detected"}
                </pre>
              </ResultCard>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function ResultCard({ title, children }: any) {
  return (
    <div className="bg-purple-800/70 border border-purple-400/30 rounded-lg p-4 shadow-lg hover:shadow-purple-500/40 transition">
      <h2 className="text-white font-semibold mb-2">
        {title}
      </h2>
      <div className="text-white">
        {children}
      </div>
    </div>
  );
}
