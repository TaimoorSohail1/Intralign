import type { Metadata } from "next";
import { ThemeInitializer } from "@/components/workspace/theme-initializer";

import "./globals.css";


export const metadata: Metadata = {
  title: "OSLO Product Grill",
  description: "Strategic project leadership for AI-first project managers.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
    >
      <body>
        <ThemeInitializer />
        {children}
      </body>
    </html>
  );
}
