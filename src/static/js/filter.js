// filter.js

function filterTable() {
    const filterInput = document.getElementById('filterInput').value.toLowerCase();
    const table = document.getElementById('clientesTable');
    const rows = table.getElementsByTagName('tr');
  
    for (let i = 1; i < rows.length; i++) {  // Empieza desde 1 para omitir el encabezado
      const nameCell = rows[i].getElementsByTagName('td')[1]; // Columna de nombre
      if (nameCell) {
        const name = nameCell.textContent.toLowerCase();
        rows[i].style.display = name.includes(filterInput) ? '' : 'none';
      }
    }
  }
  

  function filterTable2() {
    const filterInput2 = document.getElementById('filterInput2').value.toLowerCase();
    const table = document.getElementById('productable');
    const rows = table.getElementsByTagName('tr');
  
    for (let i = 1; i < rows.length; i++) {  // Empieza en 1 para omitir el encabezado
      const nameCell = rows[i].getElementsByTagName('td')[1]; // Cambia a la columna correcta
      if (nameCell) {
        const name = nameCell.textContent.toLowerCase();
        rows[i].style.display = name.includes(filterInput2) ? '' : 'none';
      }
    }
  }
  

