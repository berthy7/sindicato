/**
 * Created by bvargas on 12/11/2022.
 */


let id_table_chat = '#data_table_chat';
let id_table_cumpleaños = '#data_table_cumpleaños';
let id_table_licencias = '#data_table_licencia';

window.addEventListener("load", function () {
   reload_table()
});


$(".app-file").fileinput({
  language: "es",
  showCaption: false,
  showBrowse: true,
  showUpload: false,
  showUploadedThumbs: false,
  showPreview: true,
  previewFileType: "any",
  // allowedFileExtensions: ext_image
});


function add_columns() {
    let a_cols = []
    a_cols.push(
        { title: "ID", data: "id" },
        { title: "Fecha", data: "fecha" },
        { title: "Nombre", data: "mensaje" },
        { title: "Mensaje", data: "mensaje" },
        { title: "Respuesta", data: "respuesta" },
        { title: "Fecha Respuesta", data: "fechar" }
    );

    return a_cols;
}
function load_table(data_tb) {
    var tabla = $(id_table_chat).DataTable({
        destroy: true,
        data: data_tb,
        columns: add_columns(),
        order: [ [0, 'desc'] ],
        // columnDefs: [ { width: '33%', targets: [0, 1,2] } ],
        initComplete: function() {
        }
    });
    tabla.columns.adjust().draw();
}


function add_columns_cumpleaños() {
    let a_cols = []
    a_cols.push(
        { title: "ID", data: "id" },
        { title: "Tipo", data: "tipo" },
        { title: "Nombre", data: "id",
            render: function(data, type, row) {
                return row.nombre + " " + row.apellidos
            }
        }
    );

    return a_cols;
}
function load_table_cumpleaños(data_tb) {
    var tabla = $(id_table_cumpleaños).DataTable({
        paging: false,
        destroy: true,
        ordering: false,
        info: false,
        searching: false,
        data: data_tb,
        columns: add_columns_cumpleaños(),
        order: [ [0, 'asc'] ],
        // columnDefs: [ { width: '33%', targets: [0, 1,2] } ],
        initComplete: function() {
        }
    });
    tabla.columns.adjust().draw();
}


function add_columns_licencias() {
    let a_cols = []
    a_cols.push(
        { title: "ID", data: "id" },
        { title: "Fecha Expiracion", data: "licenciaFechaVencimiento" },
        { title: "Tipo", data: "tipo" },
        { title: "Nombre", data: "id",
            render: function(data, type, row) {
                return row.nombre + " " + row.apellidos
            }
        }
    );

    return a_cols;
}
function load_table_licencias(data_tb) {
    var tabla = $(id_table_licencias).DataTable({
        paging: false,
        destroy: true,
        ordering: false,
        info: false,
        searching: false,
        data: data_tb,
        columns: add_columns_licencias(),
        order: [ [0, 'asc'] ],
        // columnDefs: [ { width: '33%', targets: [0, 1,2] } ],
        initComplete: function() {
        }
    });
    tabla.columns.adjust().draw();
}

function reload_table() {
   $.ajax({
        method: "GET",
        url: '/chat/home',
        dataType: 'json',
        async: false,
        success: function (response) {

            console.log(response)

            load_table(response.chat)
            load_table_cumpleaños(response.cumpleaños)
            load_table_licencias(response.licencias)
        },
        error: function (jqXHR, status, err) {
        }
    });
}

$('#new-chat').click(function() {
    $('#mensaje').val('')
    $('#insert').show()
    $('#update').hide()
    $('#modal-chat').modal('show')
});

$('#insert').on('click', async function() {
    const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }

    

    const objeto ={
          mensaje: $("#mensaje").val(),
      }

        $("#insert").hide();
        $("#update").hide();
        $("#cerrar").hide();

       const response = await fetchData(
            "/chat/insert/",
            "POST",
            JSON.stringify({'obj':objeto})
       );

        if(response.success){
           showSmallMessage(response.tipo,response.mensaje,"center");
            setTimeout(function () {
               $('#modal-chat').modal('hide')
                reload_table()
            }, 2000);
        }else showSmallMessage(response.tipo,response.mensaje,"center");


})




