let id_table = '#data_table';

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


function load_table(data_tb) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: data_tb,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: [
            { title: "ID", data: "id" },
            { title: "Rol", data: "rol" },
            { title: "Linea", data: "linea" },
            { title: "Foto", data: "foto",
                render: function(data, type, row) {

                    image = ![null, '', 'None', 'S/I'].includes(data)?
                            '<a data-fancybox="gallery" href="' + data + '"><img class="d-flex align-self-center rounded img-thumbnail" src="' + data + '" alt="Imagen" height="64"></a>':
                            "<i class='mdi mdi-account-box mdi-48px'></i>";

                    return '<div class="media mx-auto align-middle">' + image + '</div>'
                }
            },
            { title: "Usuario", data: "usuario" },
            { title: "Nombre", data: "nombre" },
            { title: "Apellidos", data: "apellidos" },
            { title: "Acciones", data: "id",
                render: function(data, type, row) {
                     const dataObject = JSON.stringify(row);

                    const nombre  = row.nombre + " " + row.apellidos

                    a = ''
                        a += `\
                            <button data-object='${dataObject}'  type="button" class="btn btn-primary edit" title="Editar" onclick="edit_item(this)">\
                                <i class="mdi mdi-file-document-edit"></i>\
                            </button>`
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

                        a += '<button data-id="' + data + '" data-name="' + nombre + '" type="button" class="btn btn-info" data-toggle="tooltip" data-placement="left" title="" data-original-title="Cambiar password" onclick="change_pass(this)">\
                            <i class="mdi mdi-key"></i>\
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
$('#id').val(0)
    $('#fkrol').selectpicker("val", '');
    $('#fklinea').selectpicker("val", '');

  $('#contraseña').prop("required", true);
  $("#div_contraseña").show();
  $('#upsert').show()
  $(".form-control").val("");
  $("#submit_form").removeClass('was-validated');
  $("#modal").modal("show");
});

$('#upsert').on('click', async function() {
    const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }

        let req = {
            usuario : {
                  id: parseInt($("#id").val()),
                  username: $("#username").val(),
                  password: $("#contraseña").val(),
                  first_name: $("#nombre").val(),
                  last_name: $("#apellidos").val(),
                  email: $("#email").val()
              },
            persona : {
                  id: $("#personaid").val(),
                  nombre: $("#nombre").val(),
                  apellidos: $("#apellidos").val(),
                  fkrol: $("#fkrol").val(),
                  fklinea: $("#fklinea").val() == "" ? null : $("#fklinea").val(),
                  tipo: "Usuario"
              },
              fklinea: $("#fklinea").val(),
        }

      let url = "/usuario/insert/";

      if (parseInt($("#id").val()) != 0){
              url = "/usuario/update/";
      }

        const getCookieLocal = (name) => {
          const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
          return r ? r[1] : undefined;
        }

        // let data = new FormData($('#submit_form')[0]);
        var data = new FormData($('#submit_form').get(0));

        data.append('obj',JSON.stringify(req))

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

$('#insert').on('click', function() {
      const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
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
    $("#username").val(self.usuario)
    $("#email").val(self.email)
    $('#nombre').val(self.nombre)
    $('#fkrol').selectpicker("val", String(self.fkrol));
    $('#fklinea').selectpicker("val", String(self.fklinea));
    $('#contraseña').prop("required", false);

    $("#personaid").val(self.personaid),
    $("#nombre").val(self.nombre),
    $("#apellidos").val(self.apellidos)

    $("#div_contraseña").hide();

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


function change_pass(e) {

    idu = parseInt($(e).attr('data-id'))
    name_user = $(e).attr('data-name')
    $('#idu').val(idu)
    $('#name-user').val(name_user)

    $('.item-form').parent().find("label").addClass("active")
    $('#modal-credential').modal('show')
}

$('#upd-credentials').on('click',async function() {
      const validationData = formValidation('submit_form_credential');

      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }

      if ($('#new-pass').val() != $('#new-rpass').val()) {
        showSmallMessage("warning", 'Las contraseñas no coinciden');
        return;
      }

    const objeto={
           id: $('#idu').val(),
           newpassword: $('#new-pass').val()
      };

    $("#upd-credentials").hide();

   const response =await fetchData(
        "/usuario/changepassword/",
        "POST",
        JSON.stringify({'obj':objeto})
   );
    if(response.success){
       showSmallMessage(response.tipo,response.mensaje,"center");
        setTimeout(function () {
            $('#modal-credential').modal('hide')

        }, 2000);
    }else showSmallMessage(response.tipo,response.mensaje,"center");
});
