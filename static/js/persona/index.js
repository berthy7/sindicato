let id_table = '#data_table';
let id_table_referencia = '#data_table_referencia';

let referencias = []

$(document).ready( function () {
    reload_table();
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

$('#referencia-Categoria').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione'
});

$('#tipo').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione una opción'
});

$('#genero').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione'
});

$('#referencia-Genero').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione'
});

$('#licenciaCategoria').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione'
});

$('#lugarNacimiento').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione'
});


function add_columns_referencia() {
    let a_cols = []
    a_cols.push(
         { title: "Categoria", data: "categoria" },
        { title: "CI", data: "ci" },
        { title: "Nombre", data: "nombre" },
        { title: "Apellidos", data: "apellidos" },
        { title: "Telefono", data: "telefono" }
    );
    a_cols.push(
        { title: "Acciones", data: "ci",
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
    );

    return a_cols;
}

function load_table_referencia(data_tb) {
    var tabla = $(id_table_referencia).DataTable({
        destroy: true,
        paging: false,
        ordering: true,
        info: false,
        searching: true,
        data: data_tb,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: add_columns_referencia(),
        dom: "Bfrtip",
        buttons: [],
        "order": [ [0, 'desc'] ],
        columnDefs: [ { width: '10%', targets: [0,1,2,3] }],
        "initComplete": function() {}
    });
    tabla.draw()
}

function load_table(data_tb) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: data_tb,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: [
            { title: "ID", data: "id" },
            { title: "Tipo", data: "tipo" },
            { title: "Ci", data: "ci" },
            { title: "Nombre", data: "nombre" },
            { title: "Apellidos", data: "apellidos" },
            { title: "Domicilio", data: "domicilio" },
            { title: "Estado", data: "estado",
                render: function(data, type, row) {
                    let check = data ? 'checked' : ''
                    return '\
                    <div title="' + row.estado + '">\
                        <input id="enabled' + row.id + '" type="checkbox" class="chk-col-indigo enabled" onclick="set_enable(this)" data-id="' + row.id + '" ' + check + ' ' + row.disable + '>\
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
        buttons: [],
        "order": [ [0, 'desc'] ],
        columnDefs: [ { width: '10%', targets: [0,1,2,3] }],
        "initComplete": function() {}
    });
    tabla.draw()
}

function reload_table() {
    $.ajax({
        method: "GET",
        url: '/persona/list',
        dataType: 'json',
        async: false,
        success: function (response) {
            load_table(response)
        },
        error: function (jqXHR, status, err) {
        }
    });
}


function limpiar(){
    $('#tipo').selectpicker("val", '');
    $('#lugarNacimiento').selectpicker("val", '');
    $('#genero').selectpicker("val", '');
    $('#licenciaCategoria').selectpicker("val", '');

}

$("#new").click(function () {
    limpiar();

    referencias = []
    load_table_referencia(referencias)

  $("#update").hide();
  $("#insert").show();
  $(".form-control").val("");
  $("#submit_form").removeClass('was-validated');
  $("#modal").modal("show");
});

$("#newReferencia").click(function () {


    $(".referencia").val("");



  $("#submit_form").attr("hidden", true);
  $("#submit_form-referencia").attr("hidden", false);
  limpiar();
  $("#referencia-atras").attr("hidden", false);
  $("#update").hide();
  $("#insert").hide();
  $("#cerrar").hide();
  $("#modalLabel").attr("hidden", true);
  $("#modalLabelRefencia").attr("hidden", false);

});

$("#referencia-atras").click(function () {
  $("#submit_form").attr("hidden", false);
  $("#submit_form-referencia").attr("hidden", true);
  //limpiar();
  $("#referencia-atras").attr("hidden", true);
  $("#update").hide();
  $("#insert").show();
  $("#cerrar").show();
  $("#modalLabel").attr("hidden", false);
  $("#modalLabelRefencia").attr("hidden", true);
});

$("#referencia-insert").on("click", function () {
  const validationData = formValidation('submit_form-referencia');
  if (validationData.error) {
    showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
    return;
  }

  referencias.push({
        // id: $("#referencia-id").val(),
        categoria: $("#referencia-Categoria").val(),
        genero: $("#referencia-Genero").val(),
        nombre: $("#referencia-Nombre").val(),
        apellidos: $("#referencia-Apellido").val(),
        ci: $("#referencia-Carnet").val(),
        telefono: $("#referencia-Telefono").val()
  });

    console.log(referencias)

    load_table_referencia(referencias);

    $("#submit_form").attr("hidden", false);
    $("#submit_form-referencia").attr("hidden", true);

    $("#referencia-atras").attr("hidden", true);
      $("#insert").show();
      $("#cerrar").show();

});

$("#insert").on("click", function () {
        let tipo = "";
    if($("#tipo").val() == "")
        tipo = "Socio"
    else
         tipo = $("#tipo").val()

  const objectData = {
    ci: $("#ci").val(),
    nombre: $("#nombre").val(),
    apellidos: $("#apellidos").val(),
    genero: $("#genero").val(),
    licenciaNro: $("#licenciaNro").val(),
    licenciaCategoria: $("#licenciaCategoria").val(),
    licenciaFechaVencimiento: $("#licenciaFechaVencimiento").val(),
    telefono: $("#telefono").val(),
    domicilio: $("#domicilio").val(),
    tipo: tipo
    // fkciudad: $("#fkciudad").val() ? $("#fkciudad").val() : null,
  };

    const obj ={
        obj:objectData,
        referencias:referencias
    }

  const validationData = formValidation('submit_form');

  if (validationData.error) {
    showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
    return;
  }

   const response = fetchData(
        "/persona/insert/",
        "POST",
        JSON.stringify({'response':obj})
   );
   showSmallMessage("success" , "Insertado Correctamente", "center");
    setTimeout(function () {
        $('#modal').modal('hide')
        reload_table()
    }, 2000);

});


// $('#insert').on('click', function() {
//       const validationData = formValidation('submit_form');
//       if (validationData.error) {
//         showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
//         return;
//       }
//       objeto ={
//             nombre: $("#nombre").val()
//       }
//        const response = fetchData(
//             "/persona/insert/",
//             "POST",
//             JSON.stringify({'obj':objeto})
//        );
//        showSmallMessage("success" , "Insertado Correctamente", "center");
//         setTimeout(function () {
//             $('#modal').modal('hide')
//             reload_table()
//         }, 2000);
// });

// $("#insert").on("click", function() {
//   const objectData = {
//     ci: $("#ci").val(),
//     nombre: $("#nombre").val(),
//     apellidos: $("#apellidos").val(),
//     genero: $("#genero").val(),
//     licenciaNro: $("#licenciaNro").val(),
//     licenciaCategoria: $("#licenciaCategoria").val(),
//     licenciaFechaVencimiento: $("#licenciaFechaVencimiento").val(),
//     lugarNacimiento: $("#lugarNacimiento").val(),
//     domicilio: $("#domicilio").val(),
//     tipo: $("#tipo").val(),
//     // fkciudad: $("#fkciudad").val() ? $("#fkciudad").val() : null,
//
//   };
//
//   const validationData = formValidation('submit_form');
//
//   if (validationData.error) {
//     showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
//     return;
//   }
//
//   upsertItem({
//     id: Number($("#id").val()),
//     actionId: this.id,
//     objectData,
//     routes: ["/persona/insert/"],
//     method: "POST",
//     formId: "submit_form",
//     callback: () => reloadTable(),
//   });
// });

 function edit_item(e) {
    const self = JSON.parse(e.dataset.object);

     $.ajax({
        method: "GET",
        url: '/persona/'+self.id,
        dataType: 'json',
        async: false,
        success: function (response) {
            let self = response.obj
            $('#id').val(self.id)
            $('#ci').val(self.ci)
            $('#nombre').val(self.nombre)
            $('#apellidos').val(self.apellidos)
            $('#telefono').val(self.telefono)
            $('#genero').selectpicker("val", String(self.genero));
            $('#licenciaNro').val(self.licenciaNro)
            $('#licenciaCategoria').selectpicker("val", String(self.licenciaCategoria));
            $('#licenciaFechaVencimiento').val(self.licenciaFechaVencimiento)
            $('#telefono').selectpicker("val", String(self.telefono));
            $('#domicilio').val(self.domicilio)
            $('#tipo').selectpicker("val", String(self.tipo));

            load_table_referencia(response.referencias)

            $('.item-form').parent().addClass('focused')
            $('#insert').hide()
            $('#update').show()
            $('#modal').modal('show')

        },
        error: function (jqXHR, status, err) {
        }
    });

    // clean_data()
}

$('#update').click(function() {
    const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      objeto ={
            id: parseInt($("#id").val()),
            ci: $("#ci").val(),
            nombre: $("#nombre").val(),
            apellidos: $("#apellidos").val(),
            genero: $("#genero").val(),
            licenciaNro: $("#licenciaNro").val(),
            licenciaCategoria: $("#licenciaCategoria").val(),
            licenciaFechaVencimiento: $("#licenciaFechaVencimiento").val(),
            telefono: $("#telefono").val(),
            domicilio: $("#domicilio").val(),
            tipo: $("#tipo").val(),
      }
       const response = fetchData(
            "/persona/update/",
            "POST",
            JSON.stringify({'obj':objeto})
       );
       showSmallMessage("success" , "Modificado Correctamente", "center");
        setTimeout(function () {
            $('#modal').modal('hide')
            reload_table()
        }, 2000);
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

            fetch("/persona/state/",{
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
            fetch("/persona/delete/",{
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
