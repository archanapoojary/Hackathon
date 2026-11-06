import type { Metadata, Viewport } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "Hindsight Engine | Enterprise Deal & Revenue Intelligence",
    template: "%s | Hindsight Engine",
  },
  description:
    "Multi-persona Enterprise Deal & Revenue Intelligence Platform powered by Hindsight Memory & Groq. Sales, Customer Success, and Product intelligence unified.",
  keywords: [
    "deal intelligence",
    "revenue intelligence",
    "customer success",
    "product feedback",
    "hindsight memory",
    "groq",
    "enterprise sales",
  ],
  authors: [{ name: "Hindsight Engine Team" }],
  creator: "Hindsight Engine",
  publisher: "Hindsight Engine",
  robots: "index, follow",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://hindsight-engine.example.com",
    siteName: "Hindsight Engine",
    title: "Hindsight Engine | Enterprise Deal & Revenue Intelligence",
    description:
      "Multi-persona Enterprise Deal & Revenue Intelligence Platform powered by Hindsight Memory & Groq.",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Hindsight Engine Dashboard",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Hindsight Engine | Enterprise Deal & Revenue Intelligence",
    description:
      "Multi-persona Enterprise Deal & Revenue Intelligence Platform powered by Hindsight Memory & Groq.",
    images: ["/og-image.png"],
  },
  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon-16x16.png",
    apple: "/apple-touch-icon.png",
  },
  manifest: "/site.webmanifest",
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#090A0F" },
    { media: "(prefers-color-scheme: dark)", color: "#090A0F" },
  ],
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`} suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body className="min-h-screen bg-background text-text-PRIMARY antialiased">
        <div className="flex min-h-screen">
          {children}
        </div>
      </body>
    </html>
  );
}