import type { Metadata } from "next";
import { ThemeInitializer } from "@/components/workspace/theme-initializer";
import { buildIdentity } from "@/lib/build-identity";

import "./globals.css";

export const metadata: Metadata = {
  title: "Intralign",
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
      data-build={buildIdentity()}
      suppressHydrationWarning
    >
      <body>
        <ThemeInitializer />
        {children}
      </body>
    </html>
  );
}
