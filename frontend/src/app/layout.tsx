import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "KisanShield – Climate-Resilient Agri Advisory + Autonomous Relief Engine",
  description: "Unified agro-climate advisory, predictive risk analytics, and autonomous disaster relief logistics for Indian agriculture.",
  viewport: "width=device-width, initial-scale=1, maximum-scale=1",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased selection:bg-emerald-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
