let id_table = '#data_table';
let id_table_tipo = '#data_table_tipo';

$(document).ready( function () {
    reload_table();
    reload_table_tipo();
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

$('#fklinea').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione'
});

$('#estados').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione'
});

$('#incidente').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione'
});


$('#fktipo').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione'
});

$('#tipoPersona').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione'
});

$('#fkpersona').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione'
});

$('#fecha').datepicker({
    format: 'dd/mm/yyyy',
    language: "es",
    daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"],
});

$("#recargar").click(function () {
    reload_select_tipo()
});

function reload_table() {
    $.ajax({
        method: "GET",
        url: '/incidente/list',
        dataType: 'json',
        async: false,
        success: function (response) {
            load_table(response)
        },
        error: function (jqXHR, status, err) {
        }
    });
}
function load_table(data_tb) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: data_tb,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: [
            { title: "Nro.", data: "id" },
            { title: "Fecha", data: "fecha" },
            { title: "Linea", data: "linea"},
            { title: "Responsable", data: "responsable" },
            { title: "Incidente", data: "tipo" },
            { title: "Descripcion", data: "descripcion" },
            { title: "Estado", data: "estados"},
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
                    // if (row.delete) {
                        a += '\
                            <button data-json="' + data + '"  type="button" class="btn btn-danger waves-effect" title="Eliminar" onclick="delete_item(this)">\
                                <i class="mdi mdi-delete"></i>\
                            </button>'
                    // }
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
               exportOptions : { columns : [0, 1, 2,3,4,5,6]},
                sheetName: 'Lista de Incidentes',
               title: 'Lista de Incidentes'  },
            {  extend : 'pdfHtml5',
                orientation: 'landscape',
               customize: function(doc) {
                    doc.styles.tableBodyEven.alignment = 'center';
                    doc.styles.tableBodyOdd.alignment = 'center';
               },
               exportOptions : {
                    columns : [0, 1, 2,3,4,5,6]
                },
               title: 'Lista de Incidentes'
            }
        ],
        "order": [ [0, 'desc'] ],
        columnDefs: [ { width: '10%', targets: [0] }, { width: '27.5%', targets: [1, 2] }, { width: '20%', targets: [3] }, { width: '15%', targets: [4] } ],
        "initComplete": function() {}
    });
    tabla.draw()
}
$("#new").click(function () {
    $('#id').val(0);
    $('#fktipo').selectpicker("val", '');
    $('#tipoPersona').selectpicker("val", '');
    $('#fkpersona').selectpicker("val", '');
    $('#fklinea').selectpicker("val", '');

    $("#upsert").show();
    $(".form-control").val("");
    $("#submit_form").removeClass('was-validated');
    $("#modal").modal("show");
    $('#estados').selectpicker("val",'Abierto');

});
$('#tipoPersona').change(function () {

     $.ajax({
        method: "GET",
        url: '/persona/listarPersonaXTipo/'+$(this).val(),
        dataType: 'json',
        async: false,
        success: function (response) {

            $('#fkpersona').html('');
            $('#fkpersona').selectpicker('destroy');
            $('#fkpersona').selectpicker({
              size: 10,
              liveSearch: true,
              liveSearchPlaceholder: 'Buscar',
              title: 'Seleccione una opción'
            });

            var select = document.getElementById("fkpersona")
            var option = document.createElement("OPTION");
            // option.innerHTML = "Seleccione una opcióna";
            // option.value = 0;
            // select.appendChild(option);
            for (i of response) {
                option = document.createElement("OPTION");
                option.innerHTML = i.nombre;
                option.value = i.id;
                // option.setAttribute('data-state', '')
                select.appendChild(option);
            }
            $('#fkpersona').selectpicker('refresh');
        },
        error: function (jqXHR, status, err) {
        }
    });
    switch($(this).val()) {
      case "Otro":
          $('#responsable').val('');
          $('#div_responsable').prop("hidden", false);
          $('#div_fkpersona').prop("hidden", true);
        break;
      default:
          $('#div_responsable').prop("hidden", true);
          $('#div_fkpersona').prop("hidden", false);
    }

});



$('#upsert').on('click',async function() {
      const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }

      const objeto ={
            id: parseInt($("#id").val()),
            fecha: $("#fecha").val(),
            fktipo: $("#fktipo").val(),
            fkpersona: $("#fkpersona").val(),
            tipoPersona: $("#tipoPersona").val(),
            fklinea: $("#fklinea").val(),

            responsable: $("#responsable").val() != '' ? $("#responsable").val() : $("#fkpersona option:selected").text(),
            descripcion: $("#descripcion").val(),
            estados: $("#estados").val(),
            costo: $("#costo").val() != '' ? $("#costo").val() : 0
      }

    let url = "/incidente/insert/";

      if (objeto.id != 0){
              url = "/incidente/update/";
      }

      const getCookieLocal = (name) => {
      const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
      return r ? r[1] : undefined;
    }


    let data = new FormData($('#submit_form').get(0));
        data.append('obj',JSON.stringify(objeto))


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
                $('#upsert').show();
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
});
function edit_item(e) {
    const self = JSON.parse(e.dataset.object);

    $('#id').val(self.id)
    $('#fecha').val(self.fecha)
    $('#fktipo').selectpicker("val", String(self.fktipo));
    $('#fklinea').selectpicker("val", String(self.fklinea));
    $('#tipoPersona').selectpicker("val", String(self.tipoPersona));
    $('#tipoPersona').change();
    $('#fkpersona').selectpicker("val", String(self.fkpersona));
    $('#estados').selectpicker("val", String(self.estados));

    $('#descripcion').val(self.descripcion)
    $('#responsable').val(self.responsable)
    $('#costo').val(self.costo)

    if (self.respaldo) {
      $('#icon-respaldo').addClass('d-none');
      $('#img-respaldo').prop('src', self.respaldo);
      $('#img-respaldo').removeClass('d-none');
    }

    
    $('.item-form').parent().addClass('focused')
    $('#upsert').show()
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

            fetch("/incidente/state/",{
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
            fetch("/incidente/delete/",{
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

// Acciones Tipo
function reload_select_tipo() {
    $.ajax({
        method: "GET",
        url: '/incidente/tipoList',
        dataType: 'json',
        async: false,
        success: function (response) {

        $('#fktipo').html('');

        $('#fktipo').selectpicker('destroy');
        $('#fktipo').selectpicker({
          size: 10,
          liveSearch: true,
          liveSearchPlaceholder: 'Buscar',
          title: 'Seleccione una opción'
        });

        var select = document.getElementById("fktipo")
        for (var i = 0; i < response.length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = response[i]['nombre'];
            option.value = response[i]['id'];
            select.appendChild(option);
        }
        $('#fktipo').selectpicker('refresh');

        },
        error: function (jqXHR, status, err) {
        }
    });
}
function reload_table_tipo() {
    $.ajax({
        method: "GET",
        url: '/incidente/tipoList',
        dataType: 'json',
        async: false,
        success: function (response) {
            load_table_tipo(response)
        },
        error: function (jqXHR, status, err) {
        }
    });
}
function load_table_tipo(data_tb) {
    var tabla = $(id_table_tipo).DataTable({
        destroy: true,
        data: data_tb,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: [
            { title: "ID", data: "id" },
            { title: "Incidente", data: "nombre" },
            { title: "Estado", data: "estado",
                render: function(data, type, row) {
                    let check = data ? 'checked' : ''
                    return '\
                    <div title="' + row.estado + '">\
                        <input id="enabled' + row.id + '" type="checkbox" class="chk-col-indigo enabled" onclick="set_enable_tipo(this)" data-id="' + row.id + '" ' + check + ' ' + row.disable + '>\
                        <label for="enabled' + row.id + '"></label>\
                    </div>'
                }
            },
            { title: "Acciones", data: "id",
                render: function(data, type, row) {
                     const dataObject = JSON.stringify(row);
                    a = ''
                    // if (row.disable === '') {
                        a += `\
                            <button data-object='${dataObject}'  type="button" class="btn btn-primary edit" title="Editar" onclick="edit_item_tipo(this)">\
                                <i class="mdi mdi-file-document-edit"></i>\
                            </button>`
                    // }
                    // if (row.delete) {
                        a += '\
                            <button data-json="' + data + '"  type="button" class="btn btn-danger waves-effect" title="Eliminar" onclick="delete_item_tipo(this)">\
                                <i class="mdi mdi-delete"></i>\
                            </button>'
                    // }
                    if (a === '') a = 'Sin permisos';
                    return a
                }
            }
        ],
        dom: "Bfrtip",
        buttons: [],
        "order": [ [0, 'desc'] ],
        columnDefs: [ { width: '10%', targets: [0] }, { width: '27.5%', targets: [1, 2] }, { width: '20%', targets: [3] } ],
        "initComplete": function() {}
    });
    tabla.draw()
}
$("#new-tipo").click(function () {
    $("#nombre-tipo").val("");
  $("#update-tipo").hide();
  $("#insert-tipo").show();
  $("#submit_form-tipo").removeClass('was-validated');
  $("#modal-tipo").modal("show");
});
$('#insert-tipo').on('click',async function() {
      const validationData = formValidation('submit_form-tipo');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      const objeto ={
            nombre: $("#nombre-tipo").val()
      }
       const response = await fetchData(
            "/incidente/tipoInsert/",
            "POST",
            JSON.stringify({'obj':objeto})
       );
        if(response.success){
           showSmallMessage(response.tipo,response.mensaje,"center");
            setTimeout(function () {
                $('#modal-tipo').modal('hide')
                reload_table_tipo()
                reload_select_tipo()
            }, 2000);
        }else showSmallMessage(response.tipo,response.mensaje,"center");
});
function edit_item_tipo(e) {
    const self = JSON.parse(e.dataset.object);
    // clean_data()
    $('#id-tipo').val(self.id)
    $('#nombre-tipo').val(self.nombre)

    $('.item-form').parent().addClass('focused')
    $('#insert-tipo').hide()
    $('#update-tipo').show()
    $('#modal-tipo').modal('show')

}
$('#update-tipo').on('click', async function() {
    const validationData = formValidation('submit_form-tipo');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      objeto ={
            id: $("#id-tipo").val(),
            nombre: $("#nombre-tipo").val()
      }
       const response = await fetchData(
            "/incidente/tipoUpdate/",
            "POST",
            JSON.stringify({'obj':objeto})
       );
        if(response.success){
           showSmallMessage(response.tipo,response.mensaje,"center");
            setTimeout(function () {
                $('#modal-tipo').modal('hide')
                reload_table_tipo()
                reload_select_tipo()
            }, 2000);
        }else showSmallMessage(response.tipo,response.mensaje,"center");
})
function set_enable_tipo(e) {
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

            fetch("/incidente/tipoState/",{
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
function delete_item_tipo(e) {
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
            fetch("/incidente/tipoDelete/",{
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