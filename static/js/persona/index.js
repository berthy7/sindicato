let id_table = '#data_table';
let id_table_referencia = '#data_table_referencia';
let id_table_lineasAgregadas = '#data_table_lineas';

let referencias = []
let lineasAgregadas = []

$(document).ready( function () {
    reload_table();
});


$('#fklinea').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione una opción'
});
$('#fkinterno').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione una opción'
});


$('#ciFechaVencimiento').datepicker({
    format: 'dd/mm/yyyy',
    language: "es",
    daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"],
});


$('#licenciaFechaVencimiento').datepicker({
    format: 'dd/mm/yyyy',
    language: "es",
    daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"],
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

$('#socioConductor').selectpicker({
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
                            <button data-json="' + data + '"  type="button" class="btn btn-danger waves-effect" title="Eliminar">\
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

function add_columns_lineasAgregadas() {
    let a_cols = []
    a_cols.push(
         { title: "fklinea", data: "fklinea", visible: false },
        { title: "Linea", data: "linea" },
        { title: "fkinterno", data: "fkinterno", visible: false },
        { title: "Interno", data: "interno" }
    );
    a_cols.push(
        { title: "Acciones", data: "fklinea",
                render: function(data, type, row) {
                     const dataObject = JSON.stringify(row);
                    a = ''
                    // if (row.delete) {
                        a += '\
                            <button data-json="' + data + '"  type="button" class="btn btn-danger waves-effect" title="Eliminar">\
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

function load_table_lineasAgregadas(data_tb) {
    var tabla = $(id_table_lineasAgregadas).DataTable({
        destroy: true,
        paging: false,
        ordering: true,
        info: false,
        searching: false,
        data: data_tb,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: add_columns_lineasAgregadas(),
        dom: "Bfrtip",
        buttons: [],
        "order": [ [0, 'desc'] ],
        columnDefs: [ { width: '10%', targets: [0,1,2] }],
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
    $('#socioConductor').selectpicker("val", '');
    $('#lugarNacimiento').selectpicker("val", '');
    $('#genero').selectpicker("val", '');
    $('#licenciaCategoria').selectpicker("val", '');
}

function agregar_linea(){

      lineasAgregadas.push({
        fklinea: $("#fklinea").val(),
        linea:  $("#fklinea option:selected").html(),
        fkinterno: $("#fkinterno").val(),
        interno:  $("#fkinterno option:selected").html()
  });

    load_table_lineasAgregadas(lineasAgregadas);

    $('#fklinea').selectpicker("val", '');
    $('#fkinterno').selectpicker("val", '');

    // $("#form_interno").show();
}


$('#fklinea').change(function () {

     $.ajax({
        method: "GET",
        url: '/linea/listarInternosXLinea/'+$(this).val(),
        dataType: 'json',
        async: false,
        success: function (response) {

            $('#fkinterno').html('');
            $('#fkinterno').selectpicker('destroy');
            $('#fkinterno').selectpicker({
              size: 10,
              liveSearch: true,
              liveSearchPlaceholder: 'Buscar',
              title: 'Seleccione una opción'
            });

            var select = document.getElementById("fkinterno")
            var option = document.createElement("OPTION");
            // option.innerHTML = "Seleccione una opcióna";
            // option.value = 0;
            // select.appendChild(option);

            for (i of response) {
                console.log("iter")
                option = document.createElement("OPTION");
                option.innerHTML = i.numero;
                option.value = i.id;
                // option.setAttribute('data-state', '')
                select.appendChild(option);
            }
            $('#fkinterno').selectpicker('refresh');


        },
        error: function (jqXHR, status, err) {
        }
    });

});


$("#new").click(function () {
    limpiar();

    referencias = []
    load_table_referencia(referencias)
$('#div_tabla_lineas').show()
  $("#update").hide();
  $("#insert").show();
  $(".form-control").val("");
  $("#submit_form").removeClass('was-validated');
  $("#modal").modal("show");
});

$("#newReferencia").click(function () {

  $(".referencia").val("");
   $('#referencia-Categoria').selectpicker("val", "");
  $("#submit_form").attr("hidden", true);
  $("#submit_form-referencia").attr("hidden", false);

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
    
    load_table_referencia(referencias);

    $("#submit_form").attr("hidden", false);
    $("#submit_form-referencia").attr("hidden", true);

    $("#referencia-atras").attr("hidden", true);
      $("#insert").show();
      $("#cerrar").show();

});

$('#socioConductor').change(function () {
    if($(this).val() == "")
    {
        $('#licenciaNro').prop("required", false);
        $('#licenciaCategoria').prop("required", false);
    }
    else
    {
        $('#licenciaNro').prop("required", true);
        $('#licenciaCategoria').prop("required", true);
    }

});


$("#insert").on("click",async function () {
    const validationData = formValidation('submit_form');
  if (validationData.error) {
    showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
    return;
  }

  const objectData = {
    ci: $("#ci").val(),
    nombre: $("#nombre").val(),
    apellidos: $("#apellidos").val(),
    genero: $("#genero").val(),
    licenciaNro: $("#licenciaNro").val(),
    licenciaCategoria: $("#licenciaCategoria").val(),
    ciFechaVencimiento: $("#ciFechaVencimiento").val(),
    licenciaFechaVencimiento: $("#licenciaFechaVencimiento").val(),
    telefono: $("#telefono").val(),
    domicilio: $("#domicilio").val(),
      lugarNacimiento: $("#lugarNacimiento").val(),
      socioConductor: $("#socioConductor").val(),
    tipo: "Socio"
    // fkciudad: $("#fkciudad").val() ? $("#fkciudad").val() : null,
  };

    const obj ={
        obj:objectData,
        referencias:referencias,
        lineas:lineasAgregadas
    }

   const response =await fetchData(
        "/persona/insert/",
        "POST",
        JSON.stringify({'response':obj})
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
            $('#ciFechaVencimiento').val(self.ciFechaVencimiento)
            $('#licenciaFechaVencimiento').val(self.licenciaFechaVencimiento);
            $('#lugarNacimiento').selectpicker("val", String(self.lugarNacimiento));
            $('#domicilio').val(self.domicilio)
            $('#socioConductor').selectpicker("val", String(self.socioConductor));

            load_table_referencia(response.referencias)

            load_table_lineasAgregadas(response.asignaciones)
            // $('#div_tabla_lineas').hide()
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

$('#update').on('click', async function() {
    const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      const objeto ={
            id: parseInt($("#id").val()),
            ci: $("#ci").val(),
            nombre: $("#nombre").val(),
            apellidos: $("#apellidos").val(),
            genero: $("#genero").val(),
            licenciaNro: $("#licenciaNro").val(),
            licenciaCategoria: $("#licenciaCategoria").val(),
            ciFechaVencimiento: $("#ciFechaVencimiento").val(),
            licenciaFechaVencimiento: $("#licenciaFechaVencimiento").val(),
            telefono: $("#telefono").val(),
            domicilio: $("#domicilio").val(),
            lugarNacimiento: $("#lugarNacimiento").val(),
            socioConductor: $("#socioConductor").val(),
            tipo: "Socio"

      }
       const response = await fetchData(
            "/persona/update/",
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
