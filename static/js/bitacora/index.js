let id_table = '#data_table';

$(document).ready( function () {
    // reload_table();
});

$('#opciones').selectpicker({
  size: 7,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Buscar Opción'
});

$('#acciones').selectpicker({
  size: 7,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Buscar Funcion'
});

$('#usuarios').selectpicker({
  size: 7,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Buscar Usuario'
});


$('#btnBuscar').on('click', async function() {

    const validationData = formValidation('div_card');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      objeto ={
            opcion: $("#opciones").val(),
            usuario: $("#usuarios").val()
      }
       const response = await fetchData(
            "/bitacora/list/",
            "POST",
            JSON.stringify({'obj':objeto})
       );

        if(response.success){
           showSmallMessage(response.tipo,response.mensaje,"center");
            setTimeout(function () {

                load_table(response.response)
            }, 2000);
        }else showSmallMessage(response.tipo,response.mensaje,"center");

})


function load_table(data_tb) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: data_tb,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: [
            { title: "Nro", data: "nro" },
            { title: "Fecha", data: "fecha" },
            { title: "Usuario", data: "nombre" },
            { title: "Registro", data: "registro" },
            { title: "Registro Id", data: "id" },
            { title: "Descripcion", data: "descripcion" },
             { title: "Usuario Eliminacion", data: "usuarioEliminacion" },
            { title: "Fecha Eliminacion", data: "fechaEliminacion" }
        ],
        dom: "Bfrtip",
        buttons: [],
        "order": [ [0, 'asc'] ],
        columnDefs: [ { width: '10%', targets: [0] }, { width: '27.5%', targets: [1, 2] }, { width: '15%', targets: [3] }, { width: '20%', targets: [4] } ],
        "initComplete": function() {}
    });
    tabla.draw()
}

function reload_table() {
    $.ajax({
        method: "GET",
        url: '/bitacora/list',
        dataType: 'json',
        async: false,
        success: function (response) {
            load_table(response)
        },
        error: function (jqXHR, status, err) {
        }
    });
}

