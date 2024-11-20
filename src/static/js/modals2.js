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
  
  document.addEventListener("DOMContentLoaded", () => {
    const btnIngresarProducto = document.getElementById("btnIngresarProducto");
  
    // Evento para el botón "Ingresar el producto!"
    btnIngresarProducto.addEventListener("click", () => {
      // Aquí podrías agregar validaciones si son necesarias
      const cantidad = document.getElementById("editcantidad").value;
      const costo = document.getElementById("editcosto").value;
  
      if (!cantidad || !costo) {
        alert("Por favor, complete todos los campos.");
        return;
      }
  
      // Simula el ingreso del producto (puedes enviar datos al servidor con fetch/axios si es necesario)
      console.log("Producto ingresado:", { cantidad, costo });
  
      // Mostrar el modal de confirmación
      const modalConfirmacion = new bootstrap.Modal(
        document.getElementById("modalConfirmacion")
      );
      modalConfirmacion.show();
    });
  });
  
  document.getElementById('btnGuardarProducto').addEventListener('click', function() {
    // Obtener los valores del formulario
    var cantidad = document.getElementById('editcantidad').value;
    var costo = document.getElementById('editcosto').value;
    var fecha = document.getElementById('editfecha').value;
    var producto_id = document.getElementById('editId').value;  // Producto ID

    // Validar que los campos no estén vacíos
    if (!cantidad || !costo || !fecha || !producto_id) {
        alert('Por favor complete todos los campos');
        return;
    }

    // Enviar los datos al backend usando fetch (AJAX)
    fetch('/registrar_producto_ajax', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            producto_id: producto_id,
            cantidad: cantidad,
            costo: costo,
            fecha: fecha
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Mostrar mensaje de éxito
            $('#modalConfirmacion').modal('show');
        } else {
            // Mostrar mensaje de error
            alert('Error al registrar el producto');
        }
    })
    .catch(error => {
        console.error('Error al registrar el producto:', error);
        alert('Hubo un error al registrar el producto');
    });
});
