let id_table = '#data_table';

$(document).ready( function () {
    reload_table();
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
            { title: "Usuario", data: "usuario" },
            { title: "Nombre", data: "nombre" },
            { title: "Apellidos", data: "apellidos" },
            { title: "Acciones", data: "id",
                render: function(data, type, row) {
                     const dataObject = JSON.stringify(row);
                    a = ''
                    // if (row.disable === '') {
                    //     a += `\
                    //         <button data-object='${dataObject}'  type="button" class="btn btn-primary edit" title="Editar" onclick="edit_item(this)">\
                    //             <i class="mdi mdi-file-document-edit"></i>\
                    //         </button>`
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
        buttons: [],
        "order": [ [0, 'desc'] ],
        columnDefs: [ { width: '10%', targets: [0] } ],
        "initComplete": function() {}
    });
    tabla.draw()
}

function reload_table() {
    $.ajax({
        method: "GET",
        url: '/usuario/list',
        dataType: 'json',
        async: false,
        success: function (response) {
            load_table(response)
        },
        error: function (jqXHR, status, err) {
        }
    });
}

$('#fkrol').selectpicker({
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

$("#new").click(function () {

    $('#fkrol').selectpicker("val", '');
    $('#fklinea').selectpicker("val", '');

  $("#update").hide();
  $("#insert").show();
  $(".form-control").val("");
  $("#submit_form").removeClass('was-validated');
  $("#modal").modal("show");
});

$('#insert').on('click', function() {
      const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }

    console.log($("#fklinea").val())

        let req = {
            usuario : {
                  username: $("#username").val(),
                  password: $("#contraseña").val(),
                  first_name: $("#nombre").val(),
                  last_name: $("#apellidos").val(),
                  email: $("#email").val()
              },
            persona : {
                  nombre: $("#nombre").val(),
                  apellidos: $("#apellidos").val(),
                  fkrol: $("#fkrol").val(),
                  fklinea: $("#fklinea").val() == "" ? null : $("#fklinea").val(),
                  tipo: "Usuario"
              },
              fklinea: $("#fklinea").val(),

        }

       const response = fetchData(
            "/usuario/insert/",
            "POST",
            JSON.stringify({'obj':req})
       );
       showSmallMessage("success" , "Insertado Correctamente", "center");
        setTimeout(function () {
            $('#modal').modal('hide')
            reload_table()
        }, 2000);
});

function edit_item(e) {
    const self = JSON.parse(e.dataset.object);
    // clean_data()
    $('#id').val(self.id)
    $('#nombre').val(self.nombre)
    $("#usuario").val(self.usuario),
    $("#contraseña").val(self.contraseña),
    $("#nombre").val(self.nombre),
    $("#apellidos").val(self.apellidos)

    $('.item-form').parent().addClass('focused')
    $('#insert').hide()
    $('#update').show()
    $('#modal').modal('show')

}

$('#update').click(function() {
    const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      objeto ={
            id: $("#id").val(),
            usuario: $("#usuario").val(),
            contraseña: $("#contraseña").val(),
            nombre: $("#nombre").val(),
            apellidos: $("#apellidos").val()
      }
       const response = fetchData(
            "/usuario/update/",
            "POST",
            JSON.stringify({'obj':objeto})
       );
       showSmallMessage("success" , "Modificado Correctamente", "center");
        setTimeout(function () {
            $('#modal').modal('hide')
            reload_table()
        }, 2000);
})

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
            fetch("/usuario/delete/",{
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
