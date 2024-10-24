"use client";

import FormProduct from "./components/FormProduct";
import ListProduct from "./components/ListProduct";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold">Frontend Despacho</h1>
      <h2 className="text-primary">Generado con Next.js</h2>

      {/* Formulario */}
      <div className="flex flex-col items-center justify-center">
        <FormProduct />
      </div>

      {/* Productos */}
      <div className="flex flex-col items-center justify-center">
        <h3 className="text-2xl font-bold">Productos</h3>
        <ListProduct />
      </div>
    </main>
  );
}
