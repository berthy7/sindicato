let id_table = '#data_table';
let id_table_curso = '#data_table_curso';

$(document).ready( function () {
    reload_table();
    reload_table_curso();
});

$('#fkcurso').selectpicker({
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


function load_table(data_tb) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: data_tb,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: [
            { title: "ID", data: "id" },
            { title: "Fecha", data: "fecha" },
            { title: "Nombre", data: "persona" },
            { title: "Curso", data: "curso" },
            { title: "Dictado por", data: "dictado" },
            { title: "descripcion", data: "descripcion" },
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
            }
        ],
        dom: "Bfrtip",
        buttons: [
            {  extend : 'excelHtml5',
               exportOptions : { columns : [0, 1, 2,3,4,5]},
                sheetName: 'Lista de Capacitaciones',
               title: 'Lista de Capacitaciones'  },
            {  extend : 'pdfHtml5',
                orientation: 'landscape',
               customize: function(doc) {
                    doc.styles.tableBodyEven.alignment = 'center';
                    doc.styles.tableBodyOdd.alignment = 'center';
               },
               exportOptions : {
                    columns : [0, 1, 2,3,4,5]
                },
               title: 'Lista de Capacitaciones'
            }
        ],
        "order": [ [0, 'desc'] ],
        columnDefs: [ { width: '10%', targets: [0] }, { width: '27.5%', targets: [1, 2] }, { width: '20%', targets: [3] }, { width: '15%', targets: [4] } ],
        "initComplete": function() {}
    });
    tabla.draw()
}

function reload_table() {
    $.ajax({
        method: "GET",
        url: '/capacitacion/list',
        dataType: 'json',
        async: false,
        success: function (response) {
            load_table(response)
        },
        error: function (jqXHR, status, err) {
        }
    });
}

$("#new").click(function () {
     $('#fkcurso').selectpicker("val", '');
    $('#tipoPersona').selectpicker("val", '');
    $('#fkpersona').selectpicker("val", '');
  $("#update").hide();
  $("#insert").show();
  $(".form-control").val("");
  $("#submit_form").removeClass('was-validated');
  $("#modal").modal("show");
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

$('#insert').on('click',async function() {
      const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      const objeto ={
          fecha: $("#fecha").val(),
          fkcurso: $("#fkcurso").val(),
          fkpersona: $("#fkpersona").val(),
          tipoPersona: $("#tipoPersona").val(),
          dictado: $("#dictado").val(),
          descripcion: $("#descripcion").val()
      }
       const response = await fetchData(
            "/capacitacion/insert/",
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

function edit_item(e) {
    const self = JSON.parse(e.dataset.object);
    // clean_data()
    $('#id').val(self.id)
    $('#fecha').val(self.fecha)
     $('#fkcurso').selectpicker("val", String(self.fkcurso));
    $('#tipoPersona').selectpicker("val", String(self.tipoPersona));
    $('#tipoPersona').change();

    $('#fkpersona').selectpicker("val", String(self.fkpersona));
    $('#dictado').val(self.dictado)

    $('#descripcion').val(self.descripcion)


    
    $('.item-form').parent().addClass('focused')
    $('#insert').hide()
    $('#update').show()
    $('#modal').modal('show')

}

$('#update').on('click', async function() {
    const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      objeto ={
            id: $("#id").val(),
              fecha: $("#fecha").val(),
              fkcurso: $("#fkcurso").val(),
              fkpersona: $("#fkpersona").val(),
              tipoPersona: $("#tipoPersona").val(),
              dictado: $("#dictado").val(),
              descripcion: $("#descripcion").val()
      }
       const response = await fetchData(
            "/capacitacion/update/",
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
})

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

            fetch("/capacitacion/state/",{
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
            fetch("/capacitacion/delete/",{
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

// Acciones Curso
function reload_select_curso() {
    $.ajax({
        method: "GET",
        url: '/capacitacion/cursoList',
        dataType: 'json',
        async: false,
        success: function (response) {

        $('#fkcurso').html('');

        $('#fkcurso').selectpicker('destroy');
        $('#fkcurso').selectpicker({
          size: 10,
          liveSearch: true,
          liveSearchPlaceholder: 'Buscar',
          title: 'Seleccione una opción'
        });

        var select = document.getElementById("fkcurso")
        for (var i = 0; i < response.length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = response[i]['nombre'];
            option.value = response[i]['id'];
            select.appendChild(option);
        }
        $('#fkcurso').selectpicker('refresh');

        },
        error: function (jqXHR, status, err) {
        }
    });
}

function reload_table_curso() {
    $.ajax({
        method: "GET",
        url: '/capacitacion/cursoList',
        dataType: 'json',
        async: false,
        success: function (response) {
            load_table_curso(response)
        },
        error: function (jqXHR, status, err) {
        }
    });
}
function load_table_curso(data_tb) {
    var tabla = $(id_table_curso).DataTable({
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
                        <input id="enabled' + row.id + '" type="checkbox" class="chk-col-indigo enabled" onclick="set_enable_curso(this)" data-id="' + row.id + '" ' + check + ' ' + row.disable + '>\
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
                            <button data-object='${dataObject}'  type="button" class="btn btn-primary edit" title="Editar" onclick="edit_item_curso(this)">\
                                <i class="mdi mdi-file-document-edit"></i>\
                            </button>`
                    // }
                    // if (row.delete) {
                        a += '\
                            <button data-json="' + data + '"  type="button" class="btn btn-danger waves-effect" title="Eliminar" onclick="delete_item_curso(this)">\
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
$("#new-curso").click(function () {
    $("#nombre-curso").val("");
  $("#update-curso").hide();
  $("#insert-curso").show();
  $("#submit_form-curso").removeClass('was-validated');
  $("#modal-curso").modal("show");
});
$('#insert-curso').on('click',async function() {
      const validationData = formValidation('submit_form-curso');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      const objeto ={
            nombre: $("#nombre-curso").val()
      }
       const response = await fetchData(
            "/capacitacion/cursoInsert/",
            "POST",
            JSON.stringify({'obj':objeto})
       );
        if(response.success){
           showSmallMessage(response.curso,response.mensaje,"center");
            setTimeout(function () {
                $('#modal-curso').modal('hide')
                reload_table_curso()
                reload_select_curso()
            }, 2000);
        }else showSmallMessage(response.curso,response.mensaje,"center");
});
function edit_item_curso(e) {
    const self = JSON.parse(e.dataset.object);
    // clean_data()
    $('#id-curso').val(self.id)
    $('#nombre-curso').val(self.nombre)

    $('.item-form').parent().addClass('focused')
    $('#insert-curso').hide()
    $('#update-curso').show()
    $('#modal-curso').modal('show')

}
$('#update-curso').on('click', async function() {
    const validationData = formValidation('submit_form-curso');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      objeto ={
            id: $("#id-curso").val(),
            nombre: $("#nombre-curso").val()
      }
       const response = await fetchData(
            "/capacitacion/cursoUpdate/",
            "POST",
            JSON.stringify({'obj':objeto})
       );
        if(response.success){
           showSmallMessage(response.curso,response.mensaje,"center");
            setTimeout(function () {
                $('#modal-curso').modal('hide')
                reload_table_curso()
                reload_select_curso()
                reload_table()
            }, 2000);
        }else showSmallMessage(response.curso,response.mensaje,"center");
})
function set_enable_curso(e) {
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

            fetch("/capacitacion/cursoState/",{
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
function delete_item_curso(e) {
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
            fetch("/capacitacion/cursoDelete/",{
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