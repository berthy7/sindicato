let id_table = '#data_table';
let id_table_mapa = '#data_table_mapa';

let hoy = get_current_date(new Date());

let admin = null;

$(document).ready( function () {
    reload_table();
    reload_table_mapa();
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


$('#fechaFundacion').datepicker({
    format: 'dd/mm/yyyy',
    language: "es",
    daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"],
});

function load_table(_data) {

    var tabla = $(id_table).DataTable({
        destroy: true,
        data: _data["lista"],
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: [
            { title: "ID", data: "id" },
            { title: "Codigo", data: "codigo" },
            { title: "Razon Social", data: "razonSocial" },
            { title: "Fecha Fundacion", data: "fechaFundacion" },
            { title: "Nombre Presidente", data: "nombre" },
            { title: "Apellidos Presidente", data: "apellidos" },
            { title: "Celular", data: "celular" },
            { title: "Ubicación Oficina", data: "ubicacion" },
            { title: "Cant. de Internos", data: "internos" },
            { title: "Acciones", data: "id",
                render: function(data, type, row) {
                     const dataObject = JSON.stringify(row);
                    a = ''
                    // if (row.disable === '') {
                        a += `\
                            <button data-object='${dataObject}'  type="button" class="btn btn-primary edit" title="Editar" onclick="edit_item(this)">\
                                <i class="mdi mdi-file-document-edit"></i>\
                            </button>`
                    // }
                    if (_data["admin"]) {
                        a += '\
                            <button data-json="' + data + '"  type="button" class="btn btn-danger waves-effect" title="Eliminar" onclick="delete_item(this)">\
                                <i class="mdi mdi-delete"></i>\
                            </button>'

                    }
                    if (a === '') a = 'Sin permisos';
                    return a
                }
            },
            { title: "Estado", visible: false, data: "estado",
                render: function(data, type, row) {
                    return data? 'Activo': 'Inactivo'
                }
            }
        ],
        dom: "Bfrtip",
                buttons: [
            {  extend : 'excelHtml5',
               exportOptions : { columns : [0, 1, 2, 3, 4,5,6,7,8]},
                sheetName: 'Lista de Lineas',
               title: 'Lista de Lineas'  },
            {  extend : 'pdfHtml5',
                orientation: 'landscape',
               customize: function(doc) {
                    doc.styles.tableBodyEven.alignment = 'center';
                    doc.styles.tableBodyOdd.alignment = 'center';
               },
               exportOptions : {
                    columns : [0, 1, 2, 3, 4,5,6,7,8]
                },
               title: 'Lista de Lineas'
            }
        ],
        "order": [ [1, 'asc'] ],
        columnDefs: [ { width: '10%', targets: [0] },
            { width: '27.5%', targets: [1, 2] }, { width: '20%', targets: [3] }, { width: '15%', targets: [4] } ],
        "initComplete": function() {}
    });
    tabla.draw()
}

function reload_table() {
    $.ajax({
        method: "GET",
        url: '/linea/list',
        dataType: 'json',
        async: false,
        success: function (response) {
            admin = response["admin"]
             load_table(response)
        },
        error: function (jqXHR, status, err) {
        }
    });
}

function abrir_form_interno(){

    $('#form_interno').prop("hidden", false);
    $('#cantInternos').val('');

    // $("#form_interno").show();
}

function add_columns_mapa() {
    let a_cols = []
    a_cols.push(
            { title: "Linea", data: "codigo" },
            { title: "Mapa", data: "mapa",
                render: function(data, type, row) {

                    image = ![null, '', 'None', 'S/I'].includes(data)?
                            '<a data-fancybox="gallery" href="' + data + '"><img class="d-flex align-self-center rounded img-thumbnail" src="' + data + '" alt="Imagen" height="64"></a>':
                            "<i class='mdi mdi-account-box mdi-48px'></i>";

                    return '<div class="media mx-auto align-middle">' + image + '</div>'
                }
            },
    );
    return a_cols;
}
function load_table_mapa(data_tb) {
    var tabla = $(id_table_mapa).DataTable({
        destroy: true,
        paging: false,
        ordering: true,
        info: false,
        searching: true,
        data: data_tb,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: add_columns_mapa(),
        dom: "Bfrtip",
        buttons:[],
        // buttons: [
        //     {  extend : 'excelHtml5',
        //        exportOptions : { columns : [0,1]},
        //         sheetName: 'Lista General Conductor',
        //        title: 'Lista General Conductor'  },
        //     {  extend : 'pdfHtml5',
        //         orientation: 'landscape',
        //        customize: function(doc) {
        //             doc.styles.tableBodyEven.alignment = 'center';
        //             doc.styles.tableBodyOdd.alignment = 'center';
        //        },
        //        exportOptions : {
        //             columns : [0, 1, 2, 3, 4,5,6,7,8]
        //         },
        //        title: 'Lista General Conductor'
        //     }
        // ],
        "order": [ [0, 'asc'] ],
        columnDefs: [ { width: '10%', targets: [0,1] }],
        "initComplete": function() {}
    });
    tabla.draw()
}
function reload_table_mapa() {
    $.ajax({
        method: "GET",
        url: '/linea/mapa',
        dataType: 'json',
        async: false,
        success: function (response) {

            load_table_mapa(response)
        },
        error: function (jqXHR, status, err) {
        }
    });
}

$("#btnMapas").click(function () {
    // reload_table_mapa();
    $("#modal-mapas").modal("show");
});

$("#new").click(function () {
    $('#id').val(0)
        $("input[type=file]").fileinput("clear");
    $(".icon-preview").removeClass("d-none");
    $(".image-preview").addClass("d-none");
    $(".image-preview").prop("src", "");

  $('#div_internos').show()
  $('#div_btn_internos').hide()
     $('#form_interno').prop("hidden", true);
    $('#cantInternos').val('');

  $('#internos').prop("required", true);
  $('#upsert').show()
  $('#insertfile').hide()
  $("#cerrar").show();
  $(".form-control").val("");
  $("#submit_form").removeClass('was-validated');
  $("#modal").modal("show");
});

$('#btn_guardar_internos').on('click', async function() {
      const validationData = formValidation('submit_form_interno');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa la cantidad de Internos a crear');
        return;
      }
      objeto ={
          id: $("#id").val(),
          internos: $("#internos").val(),
          internosAlguiler: $("#internosAlguiler").val()
      }
       const response = await fetchData(
            "/linea/agregarInternos/",
            "POST",
            JSON.stringify({'obj':objeto})
       );
        if(response.success){
           showSmallMessage(response.tipo,response.mensaje,"center");
            setTimeout(function () {
                $('#modal').modal('hide')
                reload_table()
            }, 2000);
        }else showSmallMessage(response.tipo,response.mensaje,"center");

});

$('#upsert').on('click', async function() {
    const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      const obj ={
            id: parseInt($("#id").val()),
            codigo: $("#codigo").val(),
              razonSocial: $("#razonSocial").val(),
              fechaFundacion: $("#fechaFundacion").val(),
              ubicacion: $("#ubicacion").val(),
              nombre: $("#nombre").val(),
              apellidos: $("#apellidos").val(),
              celular: $("#celular").val(),
              internos: $("#internos").val()
      }

      let url = "/linea/insert/";

      if (obj.id != 0){
              url = "/linea/update/";
      }

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
                        $('#modal').modal('hide')
                        reload_table()
                    }, 2000);
              }else showSmallMessage(response.tipo,response.mensaje,"center");

            },
            error: function (jqXHR, status, err) {
            }
        });

})

$('#insertfile').on('click', async function() {
const obj ={
            id: parseInt($("#id").val()),
      }

      let url = "/linea/insertfile/";

        const getCookieLocal = (name) => {
          const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
          return r ? r[1] : undefined;
        }

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
                        $('#modal').modal('hide')
                        reload_table()
                    }, 2000);
              }else showSmallMessage(response.tipo,response.mensaje,"center");

            },
            error: function (jqXHR, status, err) {
            }
        });
})

function botones_admin(adm){
    if(adm){
    $('#upsert').show();
        $('#btn_agregar_internos').show();
    }else{
    $('#upsert').hide();
        $('#btn_agregar_internos').hide();
    }
}

function edit_item(e) {
    const self = JSON.parse(e.dataset.object);

    $("input[type=file]").fileinput("clear");
    $(".icon-preview").removeClass("d-none");
    $(".image-preview").addClass("d-none");
    $(".image-preview").prop("src", "");

    // clean_data()
    $('#id').val(self.id)
    $('#codigo').val(self.codigo)
    $('#razonSocial').val(self.razonSocial)
    $('#fechaFundacion').val(self.fechaFundacion)
    $('#ubicacion').val(self.ubicacion)
    $('#nombre').val(self.nombre)
    $('#apellidos').val(self.apellidos)
    $('#celular').val(self.celular)
    $('#internos').val(self.internos)
    $('#label_internos').html(self.internos)

    if (self.mapa) {
      $('#icon-mapa').addClass('d-none');
      $('#img-mapa').prop('src',self.mapa);
      $('#img-mapa').removeClass('d-none');
    }

     if (self.fotoOficina) {
      $('#icon-oficina').addClass('d-none');
      $('#img-oficina').prop('src',self.fotoOficina);
      $('#img-oficina').removeClass('d-none');
    }

    $('.item-form').parent().addClass('focused')
    $('#div_internos').hide()
    $('#div_btn_internos').show()
    $('#internos').prop("required", false);
    
    $('#form_interno').prop("hidden", true);
    $('#cantInternos').val('');

    $('#upsert').show()
    $('#insertfile').show()



    botones_admin(admin)

    $('#modal').modal('show')
}

function set_enable(e) {
    cb_delete = e
    b = $(e).prop('checked')

    if (!b) {
        cb_title = "¿Está seguro de que desea dar de baja?"
        cb_text = ""
        cb_type = "warning"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta?"
        cb_text = ""
        cb_type = "info"
    }

    Swal.fire({
        icon: cb_type,
        title: cb_title,
        text: cb_text,
        showCancelButton: true,
        allowOutsideClick: false,
        confirmButtonColor: '#009688',
        cancelButtonColor: '#ef5350',
        confirmButtonText: 'Aceptar',
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.value) {
            $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))

            if (b) $(cb_delete).parent().prop('title', 'Activo');
            else $(cb_delete).parent().prop('title', 'Inhabilitado');

            objeto ={
                id: parseInt($(cb_delete).attr('data-id')),
                estado: b
            }

            fetch("/linea/state/",{
                method: "POST",
                body:JSON.stringify({'obj':objeto}),
                headers:{
                    "X-CSRFToken" : getCookie('csrftoken')
                }
            })
            .then(function(response){
               showSmallMessage("success" , "Cambio Estado", "center");
                setTimeout(function () {
                    reload_table()
                }, 2000);
             })
        }
        else if (result.dismiss === 'cancel') $(cb_delete).prop('checked', !$(cb_delete).is(':checked'));
        else if (result.dismiss === 'esc') $(cb_delete).prop('checked', !$(cb_delete).is(':checked'));
    })
}

function delete_item(e) {
    Swal.fire({
        icon: "warning",
        title: "¿Está seguro de que desea eliminar?",
        text: "",
        showCancelButton: true,
        allowOutsideClick: false,
        confirmButtonColor: '#009688',
        cancelButtonColor: '#ef5350',
        confirmButtonText: 'Aceptar',
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.value) {

            objeto ={
                id: parseInt(JSON.parse($(e).attr('data-json')))
            }
            fetch("/linea/delete/",{
                method: "POST",
                body:JSON.stringify({'obj':objeto}),
                headers:{
                    "X-CSRFToken" : getCookie('csrftoken')
                }
            })
            .then(function(response){
               showSmallMessage("success" , "Se elimino Correctamente", "center");
                setTimeout(function () {
                    reload_table()
                }, 2000);
             })

        }
    })
}
