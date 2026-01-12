const inputUrl = document.getElementById("imageUrl");
const btnAdd = document.getElementById("btnAdd");
const btnDelete = document.getElementById("btnDelete");
const gallery = document.getElementById("gallery");
const msg = document.getElementById("msg");

let selectedImg = null;

function setMessage(text) {
  msg.textContent = text;
}

function clearSelection() {
  if (selectedImg) {
    selectedImg.classList.remove("selected");
    selectedImg = null;
  }
}

function getCleanUrl() {
  const url = inputUrl.value.trim();

  if (url === "") {
    setMessage("⚠️ Por favor ingresa una URL antes de agregar.");
    return null;
  }

  try {
    new URL(url);
    return url;
  } catch {
    setMessage("❌ La URL no es válida. Ejemplo: https://...");
    return null;
  }
}

function addImage() {
  const url = getCleanUrl();
  if (!url) return;

  const img = document.createElement("img");
  img.src = url;
  img.alt = "Imagen agregada por el usuario";
  img.classList.add("new");

  img.addEventListener("click", () => {
    clearSelection();
    img.classList.add("selected");
    selectedImg = img;
    setMessage("✅ Imagen seleccionada.");
  });

  img.addEventListener("error", () => {
    setMessage("❌ No se pudo cargar la imagen.");
    img.remove();
  });

  gallery.appendChild(img);
  inputUrl.value = "";
  setMessage("🖼️ Imagen agregada correctamente.");

  setTimeout(() => img.classList.remove("new"), 200);
}

function deleteSelectedImage() {
  if (!selectedImg) {
    setMessage("⚠️ Selecciona una imagen primero.");
    return;
  }

  selectedImg.remove();
  selectedImg = null;
  setMessage("🗑️ Imagen eliminada.");
}

btnAdd.addEventListener("click", addImage);
btnDelete.addEventListener("click", deleteSelectedImage);

inputUrl.addEventListener("input", () => {
  if (inputUrl.value.trim().length > 0) {
    setMessage("");
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Enter") addImage();
  if (event.key === "Delete" || event.key === "Backspace") deleteSelectedImage();
  if (event.key === "Escape") {
    clearSelection();
    setMessage("ℹ️ Selección quitada.");
  }
});

setMessage("Pega una URL y presiona ENTER o el botón Agregar.");
