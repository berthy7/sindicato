let id_table = '#data_table';

let hoy = get_current_date(new Date());

$(document).ready( function () {
    reload_table();
});


$('#fechaFundacion').datepicker({
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
            { title: "Codigo", data: "codigo" },
            { title: "Razon Social", data: "razonSocial" },
            { title: "Fecha Fundacion", data: "fechaFundacion" },
            { title: "Nro. Autorizacion", data: "nroAutorizacion" },
            { title: "Descripcion Ruta", data: "descripcionRuta" },
            { title: "Cant. de Internos", data: "internos" },
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
        columnDefs: [ { width: '10%', targets: [0] }, { width: '27.5%', targets: [1, 2] }, { width: '20%', targets: [3] }, { width: '15%', targets: [4] } ],
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

$("#new").click(function () {
  $('#div_internos').show()
  $('#div_btn_internos').hide()
     $('#form_interno').prop("hidden", true);
    $('#cantInternos').val('');

  $('#internos').prop("required", true);
  $("#update").hide();
  $("#insert").show();
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


$('#insert').on('click', async function() {
      const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }
      const objeto ={
          codigo: $("#codigo").val(),
          razonSocial: $("#razonSocial").val(),
          fechaFundacion: $("#fechaFundacion").val(),
          nroAutorizacion: $("#nroAutorizacion").val(),
          descripcionRuta: $("#descripcionRuta").val(),
          internos: $("#internos").val()
      }
       const response = await fetchData(
            "/linea/insert/",
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

    console.log(self)
    // clean_data()
    $('#id').val(self.id)
    $('#codigo').val(self.codigo)
    $('#razonSocial').val(self.razonSocial)
    $('#fechaFundacion').val(self.fechaFundacion)
    $('#nroAutorizacion').val(self.nroAutorizacion)
    $('#descripcionRuta').val(self.descripcionRuta)
    $('#internos').val(self.internos)
    $('#label_internos').html(self.internos)
    
    $('.item-form').parent().addClass('focused')
    $('#div_internos').hide()
    $('#div_btn_internos').show()
    $('#internos').prop("required", false);
    
    $('#form_interno').prop("hidden", true);
    $('#cantInternos').val('');

    
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
      const objeto ={
            id: $("#id").val(),
            codigo: $("#codigo").val(),
            razonSocial: $("#razonSocial").val(),
            fechaFundacion: $("#fechaFundacion").val(),
              nroAutorizacion: $("#nroAutorizacion").val(),
              descripcionRuta: $("#descripcionRuta").val(),
          internos: $("#internos").val()
      }

    const response = await fetchData(
            "/linea/update/",
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
