let id_table = '#data_table';
let id_table_categoria = '#data_table_categoria';
let fechahoy = new Date();

$(document).ready( function () {
    reload_table();
    reload_table_categoria();
});

function add_columns() {
    let a_cols = []
    a_cols.push(
        { title: "ID", data: "id" },
        { title: "Categoria", data: "categoria" },
        { title: "Placa", data: "placa" },
        { title: "Modelo", data: "modelo" },
        { title: "Tipo", data: "tipo" },
        { title: "Año", data: "año" },
        { title: "Linea", data: "linea" },
        { title: "Interno", data: "interno" }
    );

    a_cols.push(
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

                    a += `\
                        <button data-object='${dataObject}'  type="button" class="btn btn-primary" title="Asignar a linea" onclick="asignacion_item(this)">\
                            <i class="mdi mdi-store"></i>\
                        </button>`

                if (a === '') a = 'Sin permisos';
                return a
            }
        },
        { title: "Estado", visible: false, data: "estado",
            render: function(data, type, row) {
                return data? 'Activo': 'Inactivo'
            }
        }
    );

    return a_cols;

}

function load_table(data_tb) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: data_tb,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: add_columns(),
        dom: "Bfrtip",
        buttons: [],
        "order": [ [0, 'desc'] ],
        columnDefs: [ { width: '10%', targets: [0] }, { width: '27.5%', targets: [1, 2] }, { width: '20%', targets: [3] }, { width: '15%', targets: [4] } ],
        "initComplete": function() {}
    });
    tabla.draw()
}

function reload_table() {
    $.ajax({
        method: "GET",
        url: '/vehiculo/list',
        dataType: 'json',
        async: false,
        success: function (response) {
            load_table(response)
        },
        error: function (jqXHR, status, err) {
        }
    });
}

$('#fkcategoria').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione una opción'
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

$("#recargar").click(function () {
    reload_select_categoria()
});

function reload_select_categoria() {
    $.ajax({
        method: "GET",
        url: '/vehiculoCategoria/list',
        dataType: 'json',
        async: false,
        success: function (response) {

        $('#fkcategoria').html('');

        $('#fkcategoria').selectpicker('destroy');
        $('#fkcategoria').selectpicker({
          size: 10,
          liveSearch: true,
          liveSearchPlaceholder: 'Buscar',
          title: 'Seleccione una opción'
        });
            
        var select = document.getElementById("fkcategoria")
        for (var i = 0; i < response.length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = response[i]['nombre'];
            option.value = response[i]['id'];
            select.appendChild(option);
        }
        $('#fkcategoria').selectpicker('refresh');

        },
        error: function (jqXHR, status, err) {
        }
    });
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

    $('#fklinea').selectpicker("val", '');

    $('#fkinterno').html('');
    $('#fkinterno').selectpicker('destroy');
    $('#fkinterno').selectpicker({
      size: 10,
      liveSearch: true,
      liveSearchPlaceholder: 'Buscar',
      title: 'Seleccione una opción'
    });

    $('#fkcategoria').selectpicker("val", '');


  $("#update").hide();
  $("#insert").show();
  $("#cerrar").show();
  $(".form-control").val("");
  $("#submit_form").removeClass('was-validated');
  $("#modal").modal("show");
});

$('#insert').on('click',async function() {
      const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }

    let req = {
        objeto : {
            placa: $("#placa").val(),
            modelo: $("#modelo").val(),
            tipo: $("#tipo").val(),
            año: $("#año").val(),
            fkcategoria: parseInt($("#fkcategoria").val()),
            fklinea: parseInt($("#fklinea").val()),
            fkinterno: parseInt($("#fkinterno").val())
      },
      fklinea:parseInt($("#fklinea").val()),
      fkinterno: parseInt($("#fkinterno").val())
    }

    $("#insert").hide();
    $("#update").hide();
    $("#cerrar").hide();

       const response =await fetchData(
            "/vehiculo/insert/",
            "POST",
            JSON.stringify({'obj':req})
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
    console.log(self)

    $('#id').val(self.id)
    $('#placa').val(self.placa)
    $('#modelo').val(self.modelo)
    $('#tipo').val(self.tipo)
    $('#año').val(self.año)
    $('#fkcategoria').selectpicker("val", String(self.fkcategoria));
    
    $('.item-form').parent().addClass('focused')
    $('#insert').hide()
    $('#update').show()
    $("#cerrar").show();
    $('#modal').modal('show')

}

function asignacion_item(e) {
    const self = JSON.parse(e.dataset.object);
    // clean_data()
    $('#id').val(self.id)
    $('#lineavehiculoid').val(self.lineavehiculoid)
    $('#fklinea').selectpicker("val", String(self.fklinea));


    $('#fecha').val(fechahoy)

    $('.item-form').parent().addClass('focused')
    $('#modal_asignacion').modal('show')
}

$('#update').click(function() {
    const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      objeto ={
            id: $("#id").val(),
            placa: $("#placa").val(),
            modelo: $("#modelo").val(),
            tipo: $("#tipo").val(),
            año: $("#año").val(),
          fkcategoria: parseInt($("#fkcategoria").val())
      }

        $("#insert").hide();
    $("#update").hide();
    $("#cerrar").hide();

       const response = fetchData(
            "/vehiculo/update/",
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

            fetch("/vehiculo/state/",{
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
            fetch("/vehiculo/delete/",{
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

$('#asignar').click(function() {

    const validationData = formValidation('submit_form_asignacion');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }

      objeto ={
            fkvehiculo: parseInt($("#id").val()),
          fklinea: parseInt($("#fklinea").val()),
          fklineaInterno: parseInt($("#fkinterno").val()),
      }

       const response = fetchData(
            "/vehiculo/asignacion/",
            "POST",
            JSON.stringify({'obj':objeto})
       );
       showSmallMessage("success" , "Asignado Correctamente", "center");
        setTimeout(function () {
            $('#modal_asignacion').modal('hide')
            reload_table()
        }, 2000);
})

$('#retirar').click(function() {

    const validationData = formValidation('submit_form_asignacion');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }

      objeto ={
          lineavehiculoid: parseInt($("#lineavehiculoid").val()),
          fechaRetiro: $("#fecha").val()
      }

       const response = fetchData(
            "/vehiculo/retiro/",
            "POST",
            JSON.stringify({'obj':objeto})
       );
       showSmallMessage("success" , "Retirado Correctamente", "center");
        setTimeout(function () {
            $('#modal_asignacion').modal('hide')
            reload_table()
        }, 2000);
})



// Acciones Categoria
function reload_table_categoria() {
    $.ajax({
        method: "GET",
        url: '/vehiculo/categoriaList',
        dataType: 'json',
        async: false,
        success: function (response) {
            load_table_categoria(response)
        },
        error: function (jqXHR, status, err) {
        }
    });
}
function load_table_categoria(data_tb) {
    var tabla = $(id_table_categoria).DataTable({
        destroy: true,
        data: data_tb,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: [
            { title: "ID", data: "id" },
            { title: "Nombre", data: "nombre" },
            { title: "Estado", data: "estado",
                render: function(data, type, row) {
                    let check = data ? 'checked' : ''
                    return '\
                    <div title="' + row.estado + '">\
                        <input id="enabled' + row.id + '" type="checkbox" class="chk-col-indigo enabled" onclick="set_enable_categoria(this)" data-id="' + row.id + '" ' + check + ' ' + row.disable + '>\
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
                            <button data-object='${dataObject}'  type="button" class="btn btn-primary edit" title="Editar" onclick="edit_item_categoria(this)">\
                                <i class="mdi mdi-file-document-edit"></i>\
                            </button>`
                    // }
                    // if (row.delete) {
                        a += '\
                            <button data-json="' + data + '"  type="button" class="btn btn-danger waves-effect" title="Eliminar" onclick="delete_item_categoria(this)">\
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
$("#new-categoria").click(function () {
    $("#nombre-categoria").val("");
  $("#update-categoria").hide();
  $("#insert-categoria").show();
  $("#submit_form-categoria").removeClass('was-validated');
  $("#modal-categoria").modal("show");
});
$('#insert-categoria').on('click',async function() {
      const validationData = formValidation('submit_form-categoria');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      const objeto ={
            nombre: $("#nombre-categoria").val()
      }
       const response = await fetchData(
            "/vehiculo/categoriaInsert/",
            "POST",
            JSON.stringify({'obj':objeto})
       );
        if(response.success){
           showSmallMessage(response.tipo,response.mensaje,"center");
            setTimeout(function () {
                $('#modal-categoria').modal('hide')
                reload_table_categoria()
                reload_select_categoria()
            }, 2000);
        }else showSmallMessage(response.tipo,response.mensaje,"center");
});
function edit_item_categoria(e) {
    const self = JSON.parse(e.dataset.object);
    // clean_data()
    $('#id-categoria').val(self.id)
    $('#nombre-categoria').val(self.nombre)

    $('.item-form').parent().addClass('focused')
    $('#insert-categoria').hide()
    $('#update-categoria').show()
    $('#modal-categoria').modal('show')

}
$('#update-categoria').on('click', async function() {
    const validationData = formValidation('submit_form-categoria');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      objeto ={
            id: $("#id-categoria").val(),
            nombre: $("#nombre-categoria").val()
      }
       const response = await fetchData(
            "/vehiculo/categoriaUpdate/",
            "POST",
            JSON.stringify({'obj':objeto})
       );
        if(response.success){
           showSmallMessage(response.tipo,response.mensaje,"center");
            setTimeout(function () {
                $('#modal-categoria').modal('hide')
                reload_table_categoria()
                reload_select_categoria()
            }, 2000);
        }else showSmallMessage(response.tipo,response.mensaje,"center");
})
function set_enable_categoria(e) {
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

            fetch("/vehiculo/categoriaState/",{
                method: "POST",
                body:JSON.stringify({'obj':objeto}),
                headers:{
                    "X-CSRFToken" : getCookie('csrftoken')
                }
            })
            .then(function(response){
               showSmallMessage("success" , "Cambio Estado", "center");
                setTimeout(function () {
                    reload_table_categoria()
                    reload_select_categoria()
                }, 2000);
             })
        }
        else if (result.dismiss === 'cancel') $(cb_delete).prop('checked', !$(cb_delete).is(':checked'));
        else if (result.dismiss === 'esc') $(cb_delete).prop('checked', !$(cb_delete).is(':checked'));
    })
}
function delete_item_categoria(e) {
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
            fetch("/vehiculo/categoriaDelete/",{
                method: "POST",
                body:JSON.stringify({'obj':objeto}),
                headers:{
                    "X-CSRFToken" : getCookie('csrftoken')
                }
            })
            .then(function(response){
               showSmallMessage("success" , "Se elimino Correctamente", "center");
                setTimeout(function () {
                    reload_table_categoria()
                    reload_select_categoria()
                }, 2000);
             })

        }
    })
}
