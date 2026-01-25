
let productos = [
    {
        nombre: "Laptop",
        precio: 850,
        descripcion: "Laptop para trabajo y estudio"
    },
    {
        nombre: "Mouse",
        precio: 15,
        descripcion: "Mouse inalámbrico"
    },
    {
        nombre: "Teclado",
        precio: 25,
        descripcion: "Teclado mecánico básico"
    }
];


let lista = document.getElementById("listaProductos");


function mostrarProductos() {
    
    lista.innerHTML = "";

   
    productos.forEach(function(producto) {
        let item = document.createElement("li");
        item.textContent = producto.nombre + 
            " - $" + producto.precio + 
            " | " + producto.descripcion;

        lista.appendChild(item);
    });
}


mostrarProductos();


let boton = document.getElementById("btnAgregar");

boton.addEventListener("click", function () {
    let nuevoProducto = {
        nombre: "Producto nuevo",
        precio: 10,
        descripcion: "Producto agregado dinámicamente"
    };

    productos.push(nuevoProducto);
    mostrarProductos();
});
