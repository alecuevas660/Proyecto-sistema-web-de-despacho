import { useState } from "react";

function FormProduct() {
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [price, setPrice] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/products/`, {
            method: "POST",
            body: JSON.stringify({ name, description, price }),
            headers: {
                "Content-Type": "application/json",
            },
        });
        const data = await response.json();
        console.log(data);
    }

    return (
        <div className="flex flex-col items-center justify-center">
            <h3 className="text-2xl font-bold">Formulario Productos</h3>
            <form onSubmit={handleSubmit} className="flex flex-col items-center justify-center">
                <h1 className="text-xl font-bold text-green-800">Añadir Producto</h1>
                <input type="text" placeholder="Nombre"
                    required
                    className="input input-bordered input-primary w-full max-w-xs rounded-md p-2 m-2"
                    onChange={(e) => setName(e.target.value)}
                />
                <textarea
                    placeholder="Descripción"
                    className="textarea textarea-bordered textarea-primary w-full max-w-xs rounded-md p-2 m-2"
                    onChange={(e) => setDescription(e.target.value)}
                />
                <input
                    type="number"
                    step="0.01"
                    placeholder="Precio"
                    required
                    className="input input-bordered input-primary w-full max-w-xs rounded-md p-2 m-2"
                    onChange={(e) => setPrice(e.target.value)}
                />
                <button type="submit" className="btn btn-primary rounded-md bg-gray-800 text-white m-2 w-full hover:bg-green-600 transition-colors duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 shadow-lg">
                    <span className="mr-2">💾</span>
                    Guardar
                </button>
            </form>
        </div>
    );
}

export default FormProduct;
