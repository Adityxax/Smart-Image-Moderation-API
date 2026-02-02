import "./globals.css";

export const metadata = {
  title: "Smart Image Moderation",
  description: "CPU-only ML · Async Processing · Dockerized",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-black text-white">

        {/* HEADER */}
        <header className="relative z-20 w-full border-b border-white/10 backdrop-blur-md bg-black/40">
          <div className="max-w-7xl mx-auto px-8 py-4 flex justify-between items-center">

            {/* LEFT */}
            <div className="flex items-center gap-3">
              <span className="text-2xl">🧠</span>
              <h1
                className="text-2xl font-bold tracking-widest text-white"
                style={{ fontFamily: "Bungee, sans-serif" }}
              >
                SMART IMAGE MODERATION API
              </h1>
            </div>

            {/* RIGHT */}
            <p
              className="text-sm text-zinc-300"
              style={{ fontFamily: "Roboto Condensed, sans-serif" }}
            >
              Backend: FastAPI · Celery · Redis · OpenCV · EasyOCR
            </p>

          </div>
        </header>

        {/* PAGE CONTENT */}
        {children}

      </body>
    </html>
  );
}
