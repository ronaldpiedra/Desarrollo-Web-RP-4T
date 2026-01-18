// Formulario
const formulario = document.getElementById("formulario");

// Inputs
const nombre = document.getElementById("nombre");
const correo = document.getElementById("correo");
const password = document.getElementById("password");
const confirmar = document.getElementById("confirmar");
const edad = document.getElementById("edad");

// Mensajes de error
const errorNombre = document.getElementById("error-nombre");
const errorCorreo = document.getElementById("error-correo");
const errorPassword = document.getElementById("error-password");
const errorConfirmar = document.getElementById("error-confirmar");
const errorEdad = document.getElementById("error-edad");

// Botón enviar (es el primer submit del formulario)
const botonEnviar = formulario.querySelector("button[type='submit']");

/* ======================================================
   FUNCIONES DE VALIDACIÓN (UNA POR CAMPO)
   ====================================================== */

// ----- VALIDAR NOMBRE -----
function validarNombre() {
    if (nombre.value.length < 3) {
        errorNombre.textContent = "El nombre debe tener al menos 3 caracteres";
        nombre.classList.add("invalido");
        nombre.classList.remove("valido");
        return false;
    } else {
        errorNombre.textContent = "";
        nombre.classList.add("valido");
        nombre.classList.remove("invalido");
        return true;
    }
}

// ----- VALIDAR CORREO -----
function validarCorreo() {
    // Expresión regular básica para correos
    const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!regexCorreo.test(correo.value)) {
        errorCorreo.textContent = "Ingrese un correo válido";
        correo.classList.add("invalido");
        correo.classList.remove("valido");
        return false;
    } else {
        errorCorreo.textContent = "";
        correo.classList.add("valido");
        correo.classList.remove("invalido");
        return true;
    }
}

// ----- VALIDAR CONTRASEÑA -----
function validarPassword() {
    // Mínimo 8 caracteres, al menos un número y un carácter especial
    const regexPassword = /^(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;

    if (!regexPassword.test(password.value)) {
        errorPassword.textContent = "Mínimo 8 caracteres, un número y un símbolo";
        password.classList.add("invalido");
        password.classList.remove("valido");
        return false;
    } else {
        errorPassword.textContent = "";
        password.classList.add("valido");
        password.classList.remove("invalido");
        return true;
    }
}

// ----- VALIDAR CONFIRMACIÓN -----
function validarConfirmacion() {
    if (confirmar.value !== password.value || confirmar.value === "") {
        errorConfirmar.textContent = "Las contraseñas no coinciden";
        confirmar.classList.add("invalido");
        confirmar.classList.remove("valido");
        return false;
    } else {
        errorConfirmar.textContent = "";
        confirmar.classList.add("valido");
        confirmar.classList.remove("invalido");
        return true;
    }
}

// ----- VALIDAR EDAD -----
function validarEdad() {
    if (edad.value < 18) {
        errorEdad.textContent = "Debe ser mayor o igual a 18 años";
        edad.classList.add("invalido");
        edad.classList.remove("valido");
        return false;
    } else {
        errorEdad.textContent = "";
        edad.classList.add("valido");
        edad.classList.remove("invalido");
        return true;
    }
}

/* ======================================================
   FUNCIÓN GENERAL: ACTIVAR / DESACTIVAR BOTÓN
   ====================================================== */

function validarFormulario() {
    if (
        validarNombre() &&
        validarCorreo() &&
        validarPassword() &&
        validarConfirmacion() &&
        validarEdad()
    ) {
        botonEnviar.disabled = false;
    } else {
        botonEnviar.disabled = true;
    }
}

/* ======================================================
   EVENTOS EN TIEMPO REAL (INPUT)
   ====================================================== */

nombre.addEventListener("input", validarFormulario);
correo.addEventListener("input", validarFormulario);
password.addEventListener("input", validarFormulario);
confirmar.addEventListener("input", validarFormulario);
edad.addEventListener("input", validarFormulario);

/* ======================================================
   EVENTO SUBMIT
   ====================================================== */

formulario.addEventListener("submit", function (e) {
    e.preventDefault(); // Evita que la página se recargue
    alert("Formulario enviado correctamente ✅");
});

/* ======================================================
   EVENTO RESET (LIMPIAR TODO)
   ====================================================== */

formulario.addEventListener("reset", function () {
    botonEnviar.disabled = true;

    // Quita clases de todos los inputs
    const inputs = formulario.querySelectorAll("input");
    inputs.forEach(input => {
        input.classList.remove("valido", "invalido");
    });

    // Limpia mensajes de error
    const errores = formulario.querySelectorAll("small");
    errores.forEach(error => {
        error.textContent = "";
    });
});