// modals2.js

// Función para abrir el modal de edición y establecer los datos del producto en el formulario
function setEditData(id, nombre, precio) {
    document.getElementById('editId').value = id;  // Guarda el ID del producto
    document.getElementById('editNombre').value = nombre;
    document.getElementById('editPrecio').value = precio;
  }
  
  // Función para guardar los cambios de edición
  function saveEdit() {
    const id = document.getElementById('editId').value;
    const nombre = document.getElementById('editNombre').value;
    const precio = document.getElementById('editPrecio').value;
    
    // Realiza la solicitud `POST` al servidor para actualizar el producto
    fetch(`/productos/editar/${id}`, {  // Asegúrate de que la ruta esté bien configurada en Flask
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        'nombre': nombre,
        'precio': precio
      })
    })
    .then(response => {
      if (response.ok) {
        console.log("Producto editado correctamente en el servidor");
        location.reload();  // Recargar la página para ver los cambios
      } else {
        console.error("Error al editar el producto en el servidor:", response.statusText);
      }
    })
    .catch(error => console.error("Error en la solicitud de edición:", error));
  }
  