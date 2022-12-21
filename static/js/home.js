/**
 * Created by bvargas on 12/11/2022.
 */


let id_table_chat = '#data_table_chat';
let id_table_cumpleaños = '#data_table_cumpleaños';
let id_table_licencias = '#data_table_licencia';

window.addEventListener("load", function () {
   reload_table()
});

$('#emisorId').selectpicker({
  size: 7,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione una opción'
});

$('#receptorId').selectpicker({
  size: 7,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione una opción'
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


function add_columns(userid) {
    let a_cols = []
    a_cols.push(
        { title: "ID", data: "id" },
        { title: "Fecha", data: "fecha" },
        { title: "Nombre", data: "emisor" },
        { title: "Mensaje", data: "mensaje" },
        { title: "Respuesta", data: "respuesta" },
        { title: "Fecha Respuesta", data: "fechar" },
        { title: "Acciones", data: "id",
            render: function(data, type, row) {
                 const dataObject = JSON.stringify(row);
                a = ''

                a += `\
                    <button data-object='${dataObject}'  data-userid='${userid}' type="button" class="btn btn-primary edit" title="Editar" onclick="edit_chat(this)">\
                        <i class="mdi mdi-file-document-edit"></i>\
                    </button>`

                if (a === '') a = 'Sin permisos';
                return a
            }
        }
    );

    return a_cols;
}
function load_table(data_tb,userid) {
    var tabla = $(id_table_chat).DataTable({
        destroy: true,
        data: data_tb,
        columns: add_columns(userid),
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

            load_table(response.chat,response.userid)
            load_table_cumpleaños(response.cumpleaños)
            load_table_licencias(response.licencias)
        },
        error: function (jqXHR, status, err) {
        }
    });
}

function reload_select_usuarios(response) {

    $('#emisorId').html('');
    $('#emisorId').selectpicker('destroy');
    $('#emisorId').selectpicker({
      size: 10,
      liveSearch: true,
      liveSearchPlaceholder: 'Buscar',
      title: 'Seleccione una opción'
    });

    $('#emisorId').selectpicker('refresh');

    $('#receptorId').html('');
    $('#receptorId').selectpicker('destroy');
    $('#receptorId').selectpicker({
      size: 10,
      liveSearch: true,
      liveSearchPlaceholder: 'Buscar',
      title: 'Seleccione una opción'
    });


    var selectemisor = document.getElementById("emisorId")
    var selectreceptor = document.getElementById("receptorId")

    for (var i = 0; i < response.lista.length; i++) {
        var optionemisor = document.createElement("OPTION");
        optionemisor.innerHTML = response.lista[i]['nombre'];
        optionemisor.value = response.lista[i]['id'];
        selectemisor.appendChild(optionemisor);

        var optionreceptor = document.createElement("OPTION");
        optionreceptor.innerHTML = response.lista[i]['nombre'];
        optionreceptor.value = response.lista[i]['id'];
        selectreceptor.appendChild(optionreceptor);
    }

    $('#emisorId').selectpicker('refresh');
    $('#emisorId').selectpicker("val", String(response.userid));

    $('#receptorId').selectpicker('refresh');

}

function cargar_usuarios(){

     $.ajax({
        method: "GET",
        url: '/usuario/listar/',
        dataType: 'json',
        async: false,
        success: function (response) {

            reload_select_usuarios(response)
        },
        error: function (jqXHR, status, err) {
        }
    });

}


function privilegios_rol(){
    console.log($('#role').html())

    if($('#role').html() == "Administrador"){
            $('#div_respondido').show()
            $('#receptorId').prop("disabled", false);
    }else{
            $('#div_respondido').hide()
            $('#receptorId').prop("disabled", true);
    }
}

$('#new-chat').click(function() {
    $('#id').val(0)
    $('#mensaje').prop("disabled", false);

    $('#emisorId').selectpicker("val", '');
    $('#receptorId').selectpicker("val", '');

    cargar_usuarios()

    $("input[type=file]").fileinput("clear");
    $(".icon-preview").removeClass("d-none");
    $(".image-preview").addClass("d-none");
    $(".image-preview").prop("src", "");

    $('#mensaje').val('')
    $('#respuesta').val('')



    $('#insert').show()
    $('#update').hide()
    $('#div_respondido').hide()
     $('#div_respuesta').hide()

     privilegios_rol()

    $('#modal-chat').modal('show')
});

$('#insert').on('click', async function() {
    const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }


    let receptId = null
    let recep = null

    if($("#receptorId").val() != ""){
     receptId = $("#receptorId").val()
     recep = $("#receptorId option:selected").text()
    }


    const obj ={
         mensaje: $("#mensaje").val(),
         emisorId: $("#emisorId").val(),
         emisor: $("#emisorId option:selected").text(),
         receptorId:  receptId,
         receptor: recep
      }

        let url = "/chat/insert/";
        const getCookieLocal = (name) => {
          const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
          return r ? r[1] : undefined;
        }

        // let data = new FormData($('#submit_form')[0]);
        var data = new FormData($('#submit_form').get(0));

        data.append('obj',JSON.stringify(obj))

        $.ajax({
            method: "POST",
            url: url,
            dataType: 'json',
            processData: false,
            contentType: false,
            data: data,
            headers:{
                "X-CSRFToken" : getCookieLocal('csrftoken')
            },
            async: false,
            success: function (response) {

                if(response.success){
                   showSmallMessage(response.tipo,response.mensaje,"center");
                    setTimeout(function () {
                        $('#modal-chat').modal('hide')
                        reload_table()
                    }, 2000);
              }else showSmallMessage(response.tipo,response.mensaje,"center");

            },
            error: function (jqXHR, status, err) {
            }
        });
})


function edit_chat(e) {
    const self = JSON.parse(e.dataset.object);
    const userid = JSON.parse(e.dataset.userid);
    $("input[type=file]").fileinput("clear");
    $(".icon-preview").removeClass("d-none");
    $(".image-preview").addClass("d-none");
    $(".image-preview").prop("src", "");

    cargar_usuarios()

    $('#emisorId').selectpicker("val", String(self.emisorId));

    // clean_data()
    $('#id').val(self.id)
    $('#mensaje').val(self.mensaje)
    $('#respuesta').val(self.respuesta)

    if (self.mensajeAdjunto) {
      $('#icon').addClass('d-none');
      $('#img').prop('src',self.mensajeAdjunto);
      $('#img').removeClass('d-none');
    }

    $('.item-form').parent().addClass('focused')

    $('#div_respondido').show()
    $('#div_respuesta').show()

    $('#insert').hide()
    $('#update').show()

    privilegios_chat(self,userid)

    // botones_admin(admin)

    $('#modal-chat').modal('show')
}

$('#update').on('click', async function() {
    const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }

    const obj ={
          id: parseInt($("#id").val()),
          mensaje: $("#mensaje").val(),
          respuesta: $("#respuesta").val()
      }

        let url = "/chat/update/";

        const getCookieLocal = (name) => {
          const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
          return r ? r[1] : undefined;
        }

        // let data = new FormData($('#submit_form')[0]);
        var data = new FormData($('#submit_form').get(0));

        data.append('obj',JSON.stringify(obj))

        $.ajax({
            method: "POST",
            url: url,
            dataType: 'json',
            processData: false,
            contentType: false,
            data: data,
            headers:{
                "X-CSRFToken" : getCookieLocal('csrftoken')
            },
            async: false,
            success: function (response) {

                if(response.success){
                   showSmallMessage(response.tipo,response.mensaje,"center");
                    setTimeout(function () {
                        $('#modal-chat').modal('hide')
                        reload_table()
                    }, 2000);
              }else showSmallMessage(response.tipo,response.mensaje,"center");

            },
            error: function (jqXHR, status, err) {
            }
        });
})


function privilegios_chat(obj,userid){

    if(obj.emisorId == userid){

        $('#receptorId').selectpicker("val", String(obj.receptorId));
        $('#respuesta').prop("disabled", true);
        $('#mensaje').prop("disabled", false);
        $('#update').hide()

    }else{
        $('#receptorId').selectpicker("val", String(userid));
        $('#respuesta').prop("disabled", false);
        $('#mensaje').prop("disabled", true);
        $('#update').show()
    }

}




