let id_table = '#data_table';
let id_table_referencia = '#data_table_referencia';
let id_table_lineasAgregadas = '#data_table_lineas';

let referencias = []
let lineasAgregadas = []

$(document).ready( function () {
    reload_table();
});


$('#fklinea').selectpicker({
  size: 7,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione una opción'
});
$('#fkinterno').selectpicker({
  size: 7,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione una opción'
});


$('#fechaNacimiento').datepicker({
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
                        <button data-object='${dataObject}'  type="button" class="btn btn-primary edit" title="Editar" onclick="edit_referencia(this)">\
                            <i class="mdi mdi-file-document-edit"></i>\
                        </button>`
                // }
                // if (row.delete) {
                   a += `\
                        <button data-object='${dataObject}' data-id='${ data}'  type="button" class="btn btn-danger waves-effect" title="Eliminar" onclick="eliminar_referencia(this)">\
                            <i class="mdi mdi-delete"></i>\
                        </button>`
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
        searching: false,
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
        { title: "Acciones", data: "interPersonaId",
                render: function(data, type, row) {
                     const dataObject = JSON.stringify(row);
                    a = ''
                    // if (row.delete) {

                        a += `\
                            <button data-object='${dataObject}' data-id='${ data}'  type="button" class="btn btn-danger waves-effect" title="Eliminar" onclick="eliminar_linea(this)">\
                                <i class="mdi mdi-delete"></i>\
                            </button>`
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
        "order": [ [0, 'asc'] ],
        columnDefs: [ { width: '10%', targets: [0,1,2,3,4] }],
        "initComplete": function() {}
    });
    tabla.draw()
}

function delete_reload_table_lineasAgregadas(self){
    for (var i = 0; i < lineasAgregadas.length; i++) {
            if (parseInt(lineasAgregadas[i].fklinea) == parseInt(self.fklinea) && parseInt(lineasAgregadas[i].fkinterno) == parseInt(self.fkinterno)) {
                lineasAgregadas.splice(i, 1);
                break;
                }
            }
        load_table_lineasAgregadas(lineasAgregadas)
}

function add_reload_table_lineasAgregadas(lineaInterno){
    lineasAgregadas.push(lineaInterno);

    load_table_lineasAgregadas(lineasAgregadas);
    $('#fklinea').selectpicker("val", '');
    $('#fkinterno').selectpicker("val", '');
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
            { title: "Foto", data: "foto",
                render: function(data, type, row) {

                    image = ![null, '', 'None', 'S/I'].includes(data)?
                            '<a data-fancybox="gallery" href="/static/upload/' + data + '"><img class="d-flex align-self-center rounded img-thumbnail" src="/static/upload/' + data + '" alt="Imagen" height="64"></a>':
                            "<i class='mdi mdi-account-box mdi-48px'></i>";

                    return '<div class="media mx-auto align-middle">' + image + '</div>'

                }
            },
            { title: "Ci", data: "ci" },
            { title: "Nombre", data: "nombre" },
            { title: "Apellidos", data: "apellidos" },
            { title: "Domicilio", data: "domicilio" },
            { title: "Telefono", data: "telefono" },
            { title: "Lugar de Nacimiento", data: "lugarNacimiento", visible: false },
            { title: "Lineas", data: "id",
                render: function (data, type, row) {
                    a = ''
                    for (var i = 0; i < row.asignaciones.length; i++) {
                        a += '<p>' + row.asignaciones[i].linea +'</p>'
                    }
                    return a
                }
            },
            { title: "Internos", data: "id",
                render: function (data, type, row) {
                    a = ''
                    for (var i = 0; i < row.asignaciones.length; i++) {
                        a += '<p>' + row.asignaciones[i].interno + '</p>'
                    }
                    return a
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

                        a += '\
                            <button data-json="' + data + '"  type="button" class="btn btn-danger waves-effect" title="Reporte" onclick="reporte_item(this)">\
                                <i class="mdi mdi-print"></i>\
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
               exportOptions : { columns : [0, 1, 2, 3, 4,5,6,7,8]},
                sheetName: 'Lista de Socios',
               title: 'Lista de Socios'  },
            {  extend : 'pdfHtml5',
                orientation: 'landscape',
               customize: function(doc) {
                    doc.styles.tableBodyEven.alignment = 'center';
                    doc.styles.tableBodyOdd.alignment = 'center';
               },
               exportOptions : {
                    columns : [0, 1, 2, 3, 4,5,6,7,8]
                },
               title: 'Lista de Socios'
            }
        ],
        "order": [ [0, 'desc'] ],
        columnDefs: [ { width: '10%', targets: [0,1,2,3,4,5,6,7,8] }],
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

            console.log(response)
            load_table(response)
        },
        error: function (jqXHR, status, err) {
        }
    });
}

function limpiar(){
    $('#id').val(0);
    $('#fklinea').selectpicker("val", '');
    $('#fkinterno').selectpicker("val", '');

    $('#socioConductor').selectpicker("val", '');
    $('#lugarNacimiento').selectpicker("val", '');
    $('#genero').selectpicker("val", '');
    $('#licenciaCategoria').selectpicker("val", '');

    $("input[type=file]").fileinput("clear");


    $(".icon-preview").removeClass("d-none");
    $(".image-preview").addClass("d-none");
    $(".image-preview").prop("src", "");

}

$('#btn_agregar_linea').on('click', async function() {
    if($("#fklinea").val() !="" && $("#fkinterno").val() !=""){
        newArray = lineasAgregadas.filter(x => x.fklinea == $('#fklinea').val() && x.fkinterno == $('#fkinterno').val());

        if(newArray.length == 0){

            const lineaInterno = {
                interPersonaId: 0,
                fkpersona: $("#id").val(),
                fklinea: $("#fklinea").val(),
                linea:  $("#fklinea option:selected").html(),
                fkinterno: $("#fkinterno").val(),
                interno:  $("#fkinterno option:selected").html()
            }

            if($('#id').val() !=0)
                await add_interno(lineaInterno)
            else
                add_reload_table_lineasAgregadas(lineaInterno)

        }else showSmallMessage("warning","Linea e Interno, ya ingresados","center");
    }else showSmallMessage("warning","Seleccione Linea e Interno","center");

})

function add_interno(lineaInterno) {
    Swal.fire({
        icon: "warning",
        title: "¿Está seguro de que desea agregar?",
        text: "",
        showCancelButton: true,
        allowOutsideClick: false,
        confirmButtonColor: '#009688',
        cancelButtonColor: '#ef5350',
        confirmButtonText: 'Aceptar',
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.value) {
        

       //  const response = fetchData(
       //      "/persona/agregarInternos/",
       //      "POST",
       //      JSON.stringify({'obj':lineaInterno})
       // );
       //  if(response.success){
       //     showSmallMessage(response.tipo,response.mensaje,"center");
       //      setTimeout(function () {
       //          add_reload_table_lineasAgregadas(lineaInterno)
       //          reload_table()
       //      }, 2000);
       //  }else showSmallMessage(response.tipo,response.mensaje,"center");

        // const response = ajaxCall(
        //     '/persona/agregarInternos/',
        //     JSON.stringify({'obj':lineaInterno})
        // )
        //
        // console.log(response)
        const getCookieLocal = (name) => {
          const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
          return r ? r[1] : undefined;
        }
        $.ajax({
            method: "POST",
            url: '/persona/agregarInternos/',
            dataType: 'json',
            data: JSON.stringify({'obj':lineaInterno}),
            headers:{
                "X-CSRFToken" : getCookieLocal('csrftoken')
            },
            async: false,
            success: function (response) {

                if(response.success){
                   showSmallMessage(response.tipo,response.mensaje,"center");
                    setTimeout(function () {
                        add_reload_table_lineasAgregadas(lineaInterno)
                        reload_table()
                    }, 2000);
                }else showSmallMessage(response.tipo,response.mensaje,"center");

            },
            error: function (jqXHR, status, err) {
            }
        });
    }

    })
}

function eliminar_linea(e) {
    const self = JSON.parse(e.dataset.object);
    if($('#id').val() !="")
        if(self.interPersonaId != 0)
            delete_interno(self)
        else
            delete_reload_table_lineasAgregadas(self)
    else
        delete_reload_table_lineasAgregadas(self)
}

function delete_interno(self) {
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
        $.ajax({
            method: "GET",
            url: '/persona/eliminarInternos/'+self.interPersonaId,
            dataType: 'json',
            async: false,
            success: function (response) {

                if(response.success){
                   showSmallMessage(response.tipo,response.mensaje,"center");
                    setTimeout(function () {
                        delete_reload_table_lineasAgregadas(self)
                        reload_table()
                    }, 2000);
                }else showSmallMessage(response.tipo,response.mensaje,"center");

            },
            error: function (jqXHR, status, err) {
            }
        });
    }

    })
}

$('#fklinea').change(function () {

     $.ajax({
        method: "GET",
        url: '/linea/listarTodoInternosXLinea/'+$(this).val(),
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

    // $("#general").addClass("active");
    // $("#adjuntos").removeClass("active");

    $("#general").attr("aria-expanded", true);
    $("#adjuntos").attr("aria-expanded", false);

    limpiar();
    $("#submit_form").attr("hidden", false);
    $("#submit_form-referencia").attr("hidden", true);

    referencias = []
    load_table_referencia(referencias)
    lineasAgregadas = []
    load_table_lineasAgregadas(lineasAgregadas)
    $('#div_tabla_lineas').show()
    $("#upsert").show();
    $(".form-control").val("");
    $("#submit_form").removeClass('was-validated');
    $("#modal").modal("show");
});
$("#newReferencia").click(function () {

  $(".referencia").val("");
  $("#referencia-id").val(0),
  $('#referencia-Categoria').selectpicker("val", "");

  $("#submit_form").attr("hidden", true);
  $("#submit_form-referencia").attr("hidden", false);

  $("#referencia-atras").attr("hidden", false);
  $("#upsert").hide();
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
  $("#upsert").show();
  $("#cerrar").show();
  $("#modalLabel").attr("hidden", false);
  $("#modalLabelRefencia").attr("hidden", true);
});

$("#referencia-insert").on("click", async function () {
  const validationData = formValidation('submit_form-referencia');
  if (validationData.error) {
    showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
    return;
  }
     const referencia = {
            id: $("#referencia-id").val(),
            categoria: $("#referencia-Categoria").val(),
            genero: $("#referencia-Genero").val(),
            nombre: $("#referencia-Nombre").val(),
            apellidos: $("#referencia-Apellido").val(),
            ci: $("#referencia-Carnet").val(),
            telefono: $("#referencia-Telefono").val(),
            fkpersona: $("#id").val()
      };

    debugger

    if(parseInt($('#id').val()) !=0)
        if(parseInt(referencia.id) !=0)
          await update_referencia(referencia)
        else
          await add_referencia(referencia)
    else
        add_reload_table_referencias(referencia)

});

function add_reload_table_referencias(referencia){
    let sw = 0;
    for (var i = 0; i < referencias.length; i++) {
        if (referencias[i].ci == referencia.ci) {
            referencias[i].categoria = referencia.categoria;
            referencias[i].nombre = referencia.nombre;
            referencias[i].apellidos = referencia.apellidos;
            referencias[i].ci = referencia.ci;
            referencias[i].telefono = referencia.telefono;
            sw = 1;
            break;
        }
    }
    if(sw === 0)
        referencias.push(referencia);
    load_table_referencia(referencias);
    $("#submit_form").attr("hidden", false);
    $("#submit_form-referencia").attr("hidden", true);
    $("#referencia-atras").attr("hidden", true);
    $("#upsert").show();
    $("#cerrar").show();
}

function add_referencia(referencia) {
    Swal.fire({
        icon: "warning",
        title: "¿Está seguro de que desea agregar?",
        text: "",
        showCancelButton: true,
        allowOutsideClick: false,
        confirmButtonColor: '#009688',
        cancelButtonColor: '#ef5350',
        confirmButtonText: 'Aceptar',
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.value) {

        const getCookieLocal = (name) => {
          const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
          return r ? r[1] : undefined;
        }
        $.ajax({
            method: "POST",
            url: '/persona/agregarReferencia/',
            dataType: 'json',
            data: JSON.stringify({'obj':referencia}),
            headers:{
                "X-CSRFToken" : getCookieLocal('csrftoken')
            },
            async: false,
            success: function (response) {

                if(response.success){
                   showSmallMessage(response.tipo,response.mensaje,"center");
                    setTimeout(function () {
                        add_reload_table_referencias(referencia)
                    }, 2000);
                }else showSmallMessage(response.tipo,response.mensaje,"center");

            },
            error: function (jqXHR, status, err) {
            }
        });
    }

    })
}

function update_referencia(referencia) {
    Swal.fire({
        icon: "warning",
        title: "¿Está seguro de que desea actualizar?",
        text: "",
        showCancelButton: true,
        allowOutsideClick: false,
        confirmButtonColor: '#009688',
        cancelButtonColor: '#ef5350',
        confirmButtonText: 'Aceptar',
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.value) {

        const getCookieLocal = (name) => {
          const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
          return r ? r[1] : undefined;
        }
        $.ajax({
            method: "POST",
            url: '/persona/modificarReferencia/',
            dataType: 'json',
            data: JSON.stringify({'obj':referencia}),
            headers:{
                "X-CSRFToken" : getCookieLocal('csrftoken')
            },
            async: false,
            success: function (response) {

                if(response.success){
                   showSmallMessage(response.tipo,response.mensaje,"center");
                    setTimeout(function () {
                        add_reload_table_referencias(referencia)
                    }, 2000);
                }else showSmallMessage(response.tipo,response.mensaje,"center");

            },
            error: function (jqXHR, status, err) {
            }
        });
    }

    })
}

function eliminar_referencia(e) {
    const self = JSON.parse(e.dataset.object);
    if($('#id').val() !="")
        if(self.id != 0)
            delete_referencias(self)
        else
            delete_reload_table_referencias(self)
    else
        delete_reload_table_referencias(self)
}

function edit_referencia(e) {

    const self = JSON.parse(e.dataset.object);
      console.log(self)

        $("#referencia-id").val(self.id),
        $('#referencia-Categoria').selectpicker("val", String(self.categoria));
        $("#referencia-Nombre").val(self.nombre),
        $("#referencia-Apellido").val(self.apellidos),
        $("#referencia-Carnet").val(self.ci),
        $("#referencia-Telefono").val(self.telefono),

      $("#submit_form").attr("hidden", true);
      $("#submit_form-referencia").attr("hidden", false);

      $("#referencia-atras").attr("hidden", false);
      $("#upsert").hide();
      $("#cerrar").hide();
      $("#modalLabel").attr("hidden", true);
      $("#modalLabelRefencia").attr("hidden", false);
}

function delete_reload_table_referencias(self){
    for (var i = 0; i < referencias.length; i++) {
        if (referencias[i].ci == self.ci) {
            referencias.splice(i, 1);
            break;
        }
    }
    load_table_referencia(referencias)
}

function delete_referencias(self) {
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
        $.ajax({
            method: "GET",
            url: '/persona/eliminarReferencia/'+self.id,
            dataType: 'json',
            async: false,
            success: function (response) {

                if(response.success){
                   showSmallMessage(response.tipo,response.mensaje,"center");
                    setTimeout(function () {
                        delete_reload_table_referencias(self)
                    }, 2000);
                }else showSmallMessage(response.tipo,response.mensaje,"center");

            },
            error: function (jqXHR, status, err) {
            }
        });
    }
    })
}

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

// $("#insert").on("click",async function () {
//     const validationData = formValidation('submit_form');
//   if (validationData.error) {
//     showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
//     return;
//   }
//
//   const objectData = {
//     ci: $("#ci").val(),
//     nombre: $("#nombre").val(),
//     apellidos: $("#apellidos").val(),
//     genero: $("#genero").val(),
//     licenciaNro: $("#licenciaNro").val(),
//     licenciaCategoria: $("#licenciaCategoria").val(),
//     fechaNacimiento: $("#fechaNacimiento").val(),
//     licenciaFechaVencimiento: $("#licenciaFechaVencimiento").val(),
//     telefono: $("#telefono").val(),
//     domicilio: $("#domicilio").val(),
//       lugarNacimiento: $("#lugarNacimiento").val(),
//       socioConductor: $("#socioConductor").val(),
//     tipo: "Socio"
//     // fkciudad: $("#fkciudad").val() ? $("#fkciudad").val() : null,
//   };
//
//     const obj ={
//         obj:objectData,
//         referencias:referencias,
//         lineas:lineasAgregadas
//     }
//
//    const response =await fetchData(
//         "/persona/insert/",
//         "POST",
//         JSON.stringify({'response':obj})
//    );
//     if(response.success){
//        showSmallMessage(response.tipo,response.mensaje,"center");
//         setTimeout(function () {
//             $('#modal').modal('hide')
//             reload_table()
//         }, 2000);
//     }else showSmallMessage(response.tipo,response.mensaje,"center");
//
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

            console.log(self)

            limpiar()
            $(".form-control").val("");
            $('#id').val(self.id)
            $('#ci').val(self.ci)
            $('#nombre').val(self.nombre)
            $('#apellidos').val(self.apellidos)
            $('#telefono').val(self.telefono)
            $('#genero').selectpicker("val", String(self.genero));
            $('#licenciaNro').val(self.licenciaNro)
            $('#licenciaCategoria').selectpicker("val", String(self.licenciaCategoria));
            $('#fechaNacimiento').val(self.fechaNacimiento)
            $('#licenciaFechaVencimiento').val(self.licenciaFechaVencimiento);
            $('#lugarNacimiento').selectpicker("val", String(self.lugarNacimiento));
            $('#domicilio').val(self.domicilio)
            $('#socioConductor').selectpicker("val", String(self.socioConductor));

            if (self.foto) {
              $('#icon-foto').addClass('d-none');
              $('#img-foto').prop('src', '/static/upload/'+self.foto);
              $('#img-foto').removeClass('d-none');
            }

            if (self.fotoCi) {
              $('#icon-ci').addClass('d-none');
              $('#img-ci').prop('src', '/static/upload/'+self.fotoCi);
              $('#img-ci').removeClass('d-none');
            }

            if (self.fotoLicencia) {
              $('#icon-licencia').addClass('d-none');
              $('#img-licencia').prop('src', '/static/upload/'+self.fotoLicencia);
              $('#img-licencia').removeClass('d-none');
            }

            $('#fklinea').selectpicker("val", '');
            $('#fkinterno').selectpicker("val", '');

            referencias = response.referencias
            load_table_referencia(referencias)
            lineasAgregadas = response.asignaciones
            load_table_lineasAgregadas(lineasAgregadas)

            $("#submit_form").attr("hidden", false);
            $("#submit_form-referencia").attr("hidden", true);

            $('.item-form').parent().addClass('focused')
            $('#upsert').show()
            $('#modal').modal('show')
        },
        error: function (jqXHR, status, err) {
        }
    });
}

$('#upsert').on('click', async function() {
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
            fechaNacimiento: $("#fechaNacimiento").val(),
            licenciaFechaVencimiento: $("#licenciaFechaVencimiento").val(),
            telefono: $("#telefono").val(),
            domicilio: $("#domicilio").val(),
            lugarNacimiento: $("#lugarNacimiento").val(),
            socioConductor: $("#socioConductor").val(),
            tipo: "Socio"
      }

      let url = "/persona/insert/";
      let object = null;

      if (objeto.id != 0){
              url = "/persona/update/";
             object = objeto;
      }else{
             object ={
                obj:objeto,
                referencias:referencias,
                lineas:lineasAgregadas
            }
      }

        const getCookieLocal = (name) => {
          const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
          return r ? r[1] : undefined;
        }

        // let data = new FormData($('#submit_form')[0]);
        var data = new FormData($('#submit_form').get(0));

        data.append('obj',JSON.stringify(object))

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
      // const response = await fetchData(
      //       url,
      //       "POST",
      //       JSON.stringify({'obj':data})
      // );
      //
      //
      // if(response.success){
      //      showSmallMessage(response.tipo,response.mensaje,"center");
      //       setTimeout(function () {
      //           $('#modal').modal('hide')
      //           reload_table()
      //       }, 2000);
      // }else showSmallMessage(response.tipo,response.mensaje,"center");
})

// $('#upsert').on('click', async function() {
//     const validationData = formValidation('submit_form');
//       if (validationData.error) {
//         showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
//         return;
//       }
//       const objeto ={
//             id: parseInt($("#id").val()),
//             ci: $("#ci").val(),
//             nombre: $("#nombre").val(),
//             apellidos: $("#apellidos").val(),
//             genero: $("#genero").val(),
//             licenciaNro: $("#licenciaNro").val(),
//             licenciaCategoria: $("#licenciaCategoria").val(),
//             fechaNacimiento: $("#fechaNacimiento").val(),
//             licenciaFechaVencimiento: $("#licenciaFechaVencimiento").val(),
//             telefono: $("#telefono").val(),
//             domicilio: $("#domicilio").val(),
//             lugarNacimiento: $("#lugarNacimiento").val(),
//             socioConductor: $("#socioConductor").val(),
//             tipo: "Socio"
//       }
//
//       let url = "/persona/insert/";
//       let data = null;
//
//       if (objeto.id != 0){
//               url = "/persona/update/";
//              data = objeto;
//       }else{
//              data ={
//                 obj:objeto,
//                 referencias:referencias,
//                 lineas:lineasAgregadas
//             }
//       }
//       const response = await fetchData(
//             url,
//             "POST",
//             JSON.stringify({'obj':data})
//       );
//       if(response.success){
//            showSmallMessage(response.tipo,response.mensaje,"center");
//             setTimeout(function () {
//                 $('#modal').modal('hide')
//                 reload_table()
//             }, 2000);
//       }else showSmallMessage(response.tipo,response.mensaje,"center");
// })

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


function reporte_item(elemento){
    obj = JSON.stringify({
        'idPersonal': parseInt(JSON.parse($(elemento).attr('data-json'))),
        '_xsrf': getCookie("_xsrf")
    })

    $.ajax({
        method: "POST",
        url: '/personal_report',
        data: {object: obj, _xsrf: getCookie("_xsrf")}
    }).done(function(response){
        dictionary = JSON.parse(response)
        dictionary = dictionary.response
        servidor = ((location.href.split('/'))[0])+'//'+(location.href.split('/'))[2];
        url = servidor + dictionary;

        window.open(url)
    })
}
