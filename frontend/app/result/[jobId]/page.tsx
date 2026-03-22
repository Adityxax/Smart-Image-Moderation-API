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

interface FaceBox {
  x: number;
  y: number;
  w: number;
  h: number;
}

interface AnalysisResult {
  status: string;
  device: string;
  image_path: string;
  nsfw: boolean;
  nsfw_score: number;
  faces_detected: number;
  faces: FaceBox[];
  ocr_text: string;
  blur_score: number;
  quality_score: number;
  processing_time: number;
  model: Record<string, string>;
}

interface ResultCardProps {
  title: string;
  children: React.ReactNode;
}

export default function ResultPage() {
  const params = useParams();
  const jobId = params.jobId as string;

  const [data, setData] = useState<AnalysisResult | null>(null);
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

        if (res.data.status === "failed") {
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
              Status: <span className="font-semibold uppercase tracking-wider">{status}</span>
            </p>
          </div>

          {(status === "pending" || status === "running") && (
            <div className="rounded-lg overflow-hidden border border-purple-500/30 bg-black/40 relative h-64 flex items-center justify-center">
              <div className="scan-line animate-scan" />
              <div className="text-purple-300/50 flex flex-col items-center gap-2">
                <span className="text-4xl animate-pulse">📷</span>
                <p className={roboto.className}>Analyzing Image...</p>
              </div>
            </div>
          )}

          {status === "failed" && (
            <div className="bg-red-900/60 border border-red-500/40 rounded-lg p-4 text-center">
              <p className={`text-red-300 ${roboto.className}`}>
                ⚠️ Processing failed. Please try uploading the image again.
              </p>
            </div>
          )}

          {data && (
            <div className="space-y-6">
              {/* IMAGE DISPLAY */}
              <div className="rounded-lg overflow-hidden border border-white/20 bg-black shadow-2xl">
                <img
                  src={`http://localhost:8000${data.image_path}`}
                  alt="Analyzed"
                  className="w-full max-h-80 object-contain"
                />
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <ResultCard title="NSFW Check">
                  <div className="flex items-center gap-2">
                    <span className={data.nsfw ? "text-red-400" : "text-green-400"}>
                      {data.nsfw ? "⚠️ NSFW DETECTED" : "✅ SAFE CONTENT"}
                    </span>
                    <span className="text-xs text-white/50">({data.nsfw_score})</span>
                  </div>
                </ResultCard>

                <ResultCard title="Faces Detected">
                  <div className="text-2xl font-bold">{data.faces_detected}</div>
                </ResultCard>

                <ResultCard title="Blur Score">
                  <div className="text-xl">{data.blur_score}</div>
                </ResultCard>

                <ResultCard title="Quality Score">
                  <div className="w-full bg-black/40 h-2 rounded-full mt-2 overflow-hidden">
                    <div 
                      className="bg-purple-500 h-full transition-all duration-1000" 
                      style={{ width: `${data.quality_score * 100}%` }}
                    />
                  </div>
                  <div className="text-right text-xs mt-1 text-white/70">{data.quality_score} / 1.0</div>
                </ResultCard>

                <ResultCard title="Processing Time">
                  <div className="text-xl">{data.processing_time}s</div>
                </ResultCard>

                <ResultCard title="OCR Text Results">
                  <div className="max-h-32 overflow-y-auto pr-2 custom-scrollbar">
                    <p className="text-sm italic text-white/80 leading-relaxed">
                      {data.ocr_text || "No text detected in this image."}
                    </p>
                  </div>
                </ResultCard>
              </div>
              
              <div className="text-center pt-4">
                <button 
                  onClick={() => window.location.href = '/'}
                  className={`px-8 py-2 bg-purple-600 hover:bg-purple-500 rounded-full text-white transition-all ${bungee.className}`}
                >
                  Analyze Another
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function ResultCard({ title, children }: ResultCardProps) {
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
