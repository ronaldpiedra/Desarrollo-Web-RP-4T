CREATE DATABASE IF NOT EXISTS desarrollo_web_sem15;
USE desarrollo_web_sem15;

CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20)
);

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    id_categoria INT NOT NULL,
    id_proveedor INT NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
);

INSERT INTO categorias (nombre) VALUES
('Tecnología'),
('Oficina'),
('Accesorios');

INSERT INTO proveedores (nombre, telefono) VALUES
('Proveedor Uno', '0991111111'),
('Proveedor Dos', '0982222222'),
('Proveedor Tres', '0973333333');

INSERT INTO productos (nombre, precio, stock, id_categoria, id_proveedor) VALUES
('Mouse', 15.50, 20, 1, 1),
('Teclado', 25.00, 15, 1, 2),
('Cuaderno', 3.25, 50, 2, 3);