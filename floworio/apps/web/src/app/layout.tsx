import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "react-hot-toast";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Floworio — Data Story Platform",
  description:
    "Upload Excel data, generate AI-powered stories, render animated videos with Remotion, and publish to social media automatically.",
  keywords: ["data visualization", "bar race", "animated charts", "social media", "AI story"],
  openGraph: {
    title: "Floworio — Data Story Platform",
    description: "Turn your data into viral social media videos in minutes",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-dark-950 text-white antialiased`}>
        {children}
        <Toaster
          position="bottom-right"
          toastOptions={{
            style: {
              background: "#1a1d24",
              color: "#fff",
              border: "1px solid rgba(255,255,255,0.1)",
            },
          }}
        />
      </body>
    </html>
  );
}
