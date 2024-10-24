import "./globals.css";

export const metadata = {
  title: "Frontend Despacho",
  description: "Generado con Next.js",
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>
        {children}
      </body>
    </html>
  );
}
