let id_table = '#data_table';
let id_table_categoria = '#data_table_categoria';
let fechahoy = new Date();
let admin = null;
let vehiculos = [];

$(document).ready( function () {
    reload_table();
    reload_table_categoria();
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

$('#soatVencimiento').datepicker({
    format: 'dd/mm/yyyy',
    language: "es",
    daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"],
});

$('#inspeccionVencimiento').datepicker({
    format: 'dd/mm/yyyy',
    language: "es",
    daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"],
});


$('#seguroVencimiento').datepicker({
    format: 'dd/mm/yyyy',
    language: "es",
    daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"],
});



function add_columns(admin) {
    let a_cols = []
    a_cols.push(
        { title: "ID", data: "id" },
        { title: "Categoria", data: "categoria" },
        { title: "Placa", data: "placa" },
        { title: "Marca", data: "modelo" },
        { title: "Tipo", data: "tipo" },
        { title: "Año", data: "año" },
        { title: "Linea", data: "linea" },
        { title: "Interno", data: "interno" }
    );

    a_cols.push(
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
                if (admin) {
                    a += '\
                        <button data-json="' + data + '"  type="button" class="btn btn-danger waves-effect" title="Eliminar" onclick="delete_item(this)">\
                            <i class="mdi mdi-delete"></i>\
                        </button>'

                     a += `\
                        <button data-object='${dataObject}'  type="button" class="btn btn-success " title="Transferir" onclick="transferencia_item(this)">\
                            <i class="mdi mdi-send"></i>\
                        </button>`
                }

                //     a += `\
                //         <button data-object='${dataObject}'  type="button" class="btn btn-primary" title="Asignar a linea" onclick="asignacion_item(this)">\
                //             <i class="mdi mdi-store"></i>\
                //         </button>`

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

function load_table(_data) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: _data["lista"],
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: add_columns(_data["admin"]),
        dom: "Bfrtip",
        buttons: [
            {  extend : 'excelHtml5',
               exportOptions : { columns : [0, 1, 2, 3, 4,5,6,7]},
                sheetName: 'Lista de Vehiculos',
               title: 'Lista de Vehiculos' },
            {  extend : 'pdfHtml5',
                orientation: 'portrait',
               customize: function(doc) {
                    doc.styles.tableBodyEven.alignment = 'center';
                    doc.styles.tableBodyOdd.alignment = 'center';
               },
               exportOptions : {
                    columns : [0, 1, 2, 3, 4,5,6,7]
                },
               title: 'Lista de Vehiculos'
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
        url: '/vehiculo/list',
        dataType: 'json',
        async: false,
        success: function (response) {

            admin = response["admin"];
            load_table(response)
            load_select(response["lista"])
        },
        error: function (jqXHR, status, err) {
        }
    });
}

function load_select(lista){

    $('#listaVehiculo').html('');
    $('#listaVehiculo').selectpicker('destroy');
    $('#listaVehiculo').selectpicker({
      size: 10,
      liveSearch: true,
      liveSearchPlaceholder: 'Buscar',
      title: 'Seleccione una opción'
    });


        $('#listaVehiculo_trans').html('');
    $('#listaVehiculo_trans').selectpicker('destroy');
    $('#listaVehiculo_trans').selectpicker({
      size: 10,
      liveSearch: true,
      liveSearchPlaceholder: 'Buscar',
      title: 'Seleccione una opción'
    });



    var select = document.getElementById("listaVehiculo")

    var select_trans = document.getElementById("listaVehiculo_trans")


    var option = document.createElement("OPTION");

    var option_trans = document.createElement("OPTION");

    for (i of lista) {

        option = document.createElement("OPTION");
        option.innerHTML = i.placa;
        option.value = i.id;
        option.setAttribute('data-fklinea', i.fklinea)
        option.setAttribute('data-linea', i.linea)
        option.setAttribute('data-fkinterno', i.fkinterno)
        option.setAttribute('data-interno', i.interno)
        select.appendChild(option);

        option_trans = document.createElement("OPTION");
        option_trans.innerHTML = i.placa;
        option_trans.value = i.id;
        option_trans.setAttribute('data-fklinea', i.fklinea)
        option_trans.setAttribute('data-linea', i.linea)
        option_trans.setAttribute('data-fkinterno', i.fkinterno)
        option_trans.setAttribute('data-interno', i.interno)
        select_trans.appendChild(option_trans);
    }

    $('#listaVehiculo').selectpicker('refresh');
    $('#listaVehiculo_trans').selectpicker('refresh');

}

$('#listaVehiculo').change(function () {

    $("#lineaVehiculo").val($("#listaVehiculo option:selected").attr("data-linea"))
    $("#internoVehiculo").val($("#listaVehiculo option:selected").attr("data-interno"))

});


$('#listaVehiculo_trans').change(function () {

    $("#lineaVehiculo_trans").val($("#listaVehiculo_trans option:selected").attr("data-linea"))
    $("#internoVehiculo_trans").val($("#listaVehiculo_trans option:selected").attr("data-interno"))

});




$('#listaVehiculo_trans').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione una opción'
});


$('#fklinea_trans').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione una opción'
});


$('#fkinterno_trans').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione una opción'
});

$('#listaVehiculo').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione una opción'
});

$('#seleccione_trans').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione una opción'
});


$('#seleccion').selectpicker({
  size: 10,
  liveSearch: true,
  liveSearchPlaceholder: 'Buscar',
  title: 'Seleccione una opción'
});

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

function transferencia_item(e){
    const self = JSON.parse(e.dataset.object);
    $('#vehiculoId').val(self.id)
    $('#vehiculoPlaca').val(self.placa + " " + self.categoria)

    $('#lineaId').val(self.fklinea)
    $('#linea').val(self.linea)
    
    $('#internoId').val(self.fkinterno)
    $('#interno').val(self.interno)

    $('#tipo-trans').val(self.tipo + " " + self.año)
    $('#modelo-trans').val(self.modelo)

    $('#vehiculoTransferencia').html('');
    $('#vehiculoTransferencia').selectpicker('destroy');
    $('#vehiculoTransferencia').selectpicker({
      size: 10,
      liveSearch: true,
      liveSearchPlaceholder: 'Buscar',
      title: 'Seleccione una opción'
    });

    var select = document.getElementById("vehiculoTransferencia")
    for (var i = 0; i < vehiculos; i++) {
        var option = document.createElement("OPTION");
        option.innerHTML = response[i]['placa'];
        option.value = response[i]['id'];
        select.appendChild(option);
    }
    $('#vehiculoTransferencia').selectpicker('refresh');



    $('#seleccione_trans').selectpicker("val", '');
    $('#fklinea_trans').selectpicker("val", '');

    $('#fkinterno_trans').html('');
    $('#fkinterno_trans').selectpicker('destroy');
    $('#fkinterno_trans').selectpicker({
      size: 10,
      liveSearch: true,
      liveSearchPlaceholder: 'Buscar',
      title: 'Seleccione una opción'
    });





    $('#div_seleccion_trans').show()
    $('#div_vehiculo_trans').hide()
    $('#div_linea_trans').hide()


  $("#modal-transferencia").modal("show");
}

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
function listar_internos(idLinea,idInterno,numInterno){
         $.ajax({
        method: "GET",
        url: '/linea/listarInternosXLinea/'+idLinea,
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

            // option.innerHTML = numInterno;
            // option.value = idInterno;
            // select.appendChild(option);


            for (i of response) {

                option = document.createElement("OPTION");
                option.innerHTML = i.numero;
                option.value = i.id;
                // option.setAttribute('data-state', '')
                select.appendChild(option);
            }
            $('#fkinterno').selectpicker('refresh');
            $('#fkinterno').selectpicker("val", String(idInterno));


        },
        error: function (jqXHR, status, err) {
        }
    });
}
function listar_internosTrans(idLinea){
         $.ajax({
        method: "GET",
        url: '/linea/listarInternosXLinea/'+idLinea,
        dataType: 'json',
        async: false,
        success: function (response) {
            $('#fkinterno_trans').html('');
            $('#fkinterno_trans').selectpicker('destroy');
            $('#fkinterno_trans').selectpicker({
              size: 10,
              liveSearch: true,
              liveSearchPlaceholder: 'Buscar',
              title: 'Seleccione una opción'
            });

            var select = document.getElementById("fkinterno_trans")
            var option = document.createElement("OPTION");

            for (i of response) {

                option = document.createElement("OPTION");
                option.innerHTML = i.numero;
                option.value = i.id;
                // option.setAttribute('data-state', '')
                select.appendChild(option);
            }
            $('#fkinterno_trans').selectpicker('refresh');
        },
        error: function (jqXHR, status, err) {
        }
    });
}

$('#fklinea').change(function () {
    listar_internos($(this).val(),'','');
});

$('#fklinea_trans').change(function () {
    listar_internosTrans($(this).val());
});

$('#seleccion').change(function () {

    if($(this).val() != "1"){

        $('#div_vehiculo').show()
        $('#div_linea').hide()

    }else{

        $('#div_vehiculo').hide()
        $('#div_linea').show()

    }

});

$('#seleccione_trans').change(function () {

    if(parseInt($(this).val()) == 1)
    {
        $('#div_vehiculo_trans').hide()
        $('#div_linea_trans').show()

        $('#fklinea_trans').prop("required", true);
        $('#fkinterno_trans').prop("required", true);
        $('#listaVehiculo_trans').prop("required", false);
    }
    else
    {
         $('#div_vehiculo_trans').show()
        $('#div_linea_trans').hide()

        $('#fklinea_trans').prop("required", false);
        $('#fkinterno_trans').prop("required", false);
        $('#listaVehiculo_trans').prop("required", true);
    }

});

$('#btnTransferir').on('click', async function() {
    const validationData = formValidation('submit_form-transferencia');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }

    let req = {
        obj : {
              fkvehiculo: parseInt($("#vehiculoId").val()),
              fklinea: parseInt($("#lineaId").val()),
              fkinterno: parseInt($("#internoId").val()),

              fklineatrans: parseInt($("#fklinea_trans").val()),
              fkinternotrans: parseInt($("#fkinterno_trans").val())

          },
          fklinea:parseInt($("#fklinea_trans").val()),
          fkinterno: parseInt($("#fkinterno_trans").val()),

          seleccion: parseInt($("#seleccione_trans").val()),
          transfklinea:parseInt($("#listaVehiculo_trans option:selected").attr("data-fklinea")),
          transfkinterno: parseInt($("#listaVehiculo_trans option:selected").attr("data-fkinterno")),
          transvehiculo: parseInt($("#listaVehiculo_trans").val())

        }


           const response = await fetchData(
            "/vehiculo/transferir/",
            "POST",
            JSON.stringify({'obj':req})
       );
        if(response.success){
           showSmallMessage(response.tipo,response.mensaje,"center");
            setTimeout(function () {
               $('#modal-transferencia').modal('hide')
                reload_table()
            }, 2000);
        }else showSmallMessage(response.tipo,response.mensaje,"center");

})


$("#new").click(function () {

    $("#general").attr("aria-expanded", true);
    $("#adjuntos").attr("aria-expanded", false);
    $('#id').val(0)
    $('#fklinea').selectpicker("val", '');
    $('#seleccion').selectpicker("val", '');

    $('#div_seleccion').show()

    $('#div_vehiculo').hide()
    $('#div_listaVehiculo').show()

    $('#div_linea').hide()

    $('#fkinterno').html('');
    $('#fkinterno').selectpicker('destroy');
    $('#fkinterno').selectpicker({
      size: 10,
      liveSearch: true,
      liveSearchPlaceholder: 'Buscar',
      title: 'Seleccione una opción'
    });

   $("#upsert").show();
    $('#insertfile').hide()
   $("#cerrar").show();
   $(".form-control").val("");
   $("#submit_form").removeClass('was-validated');

   $("input[type=file]").fileinput("clear");

    $(".icon-preview").removeClass("d-none");
    $(".image-preview").addClass("d-none");
    $(".image-preview").prop("src", "");

    $('#fkcategoria').selectpicker("val", '1');
    $('#modelo').val('TOYOTA');
    $('#tipo').val('COASTER');

    $('#soat').val('');
    $('#inspeccion').val('');
    $('#seguro').val('');

    $("#modal").modal("show");
});

$('#insertfile').on('click', async function() {
const obj ={
            id: parseInt($("#id").val()),
                soatVencimiento: $("#soatVencimiento").val(),
            inspeccionVencimiento: $("#inspeccionVencimiento").val(),
            seguroVencimiento: $("#seguroVencimiento").val()
      }

      let url = "/vehiculo/insertfile/";

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

$('#insertfile2').on('click', async function() {
const obj ={
            id: parseInt($("#id").val()),
            soatVencimiento: $("#soatVencimiento").val(),
            inspeccionVencimiento: $("#inspeccionVencimiento").val(),
            seguroVencimiento: $("#seguroVencimiento").val()
      }

      let url = "/vehiculo/insertfile/";

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

$('#upsert').on('click',async function() {
      const validationData = formValidation('submit_form');
      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }

    let req = {
        obj : {
            id: parseInt($("#id").val()),
            placa: $("#placa").val(),
            modelo: $("#modelo").val(),
            tipo: $("#tipo").val(),
            año: $("#año").val(),
            fkcategoria: parseInt($("#fkcategoria").val()),
            fklinea: parseInt($("#fklinea").val()),
            fkinterno: parseInt($("#fkinterno").val()),
            soatVencimiento: $("#soatVencimiento").val(),
            inspeccionVencimiento: $("#inspeccionVencimiento").val(),
            seguroVencimiento: $("#seguroVencimiento").val(),

      },
      fklinea:parseInt($("#fklinea").val()),
      fkinterno: parseInt($("#fkinterno").val()),

      seleccion: parseInt($("#seleccion").val()),
      transfklinea:parseInt($("#listaVehiculo option:selected").attr("data-fklinea")),
      transfkinterno: parseInt($("#listaVehiculo option:selected").attr("data-fkinterno")),
      transvehiculo: parseInt($("#listaVehiculo").val())

    }

    $('#upsert').hide();
      let url = "/vehiculo/insert/";
      if (parseInt($("#id").val()) != 0){
              url = "/vehiculo/update/";
      }

  const getCookieLocal = (name) => {
      const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
      return r ? r[1] : undefined;
    }


    let data = new FormData($('#submit_form').get(0));
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


$('#seleccion').change(function () {

    if(parseInt($(this).val()) == 1)
    {
        $('#fklinea').prop("required", true);
        $('#fkinterno').prop("required", true);
        $('#listaVehiculo').prop("required", false);
    }
    else
    {
        $('#fklinea').prop("required", false);
        $('#fkinterno').prop("required", false);
        $('#listaVehiculo').prop("required", true);
    }

});


function botones_admin(adm){
    if(adm){
        $('#upsert').show();
    }else{
        $('#upsert').hide();
       
    }
}

function edit_item(e) {
    const self = JSON.parse(e.dataset.object);

    $('#id').val(self.id)
    $('#placa').val(self.placa)
    $('#modelo').val(self.modelo)
    $('#tipo').val(self.tipo)
    $('#año').val(self.año)

    $('#soatVencimiento').val(self.soatVencimiento);
    $('#inspeccionVencimiento').val(self.inspeccionVencimiento);
    $('#seguroVencimiento').val(self.seguroVencimiento);


    $('#fkcategoria').selectpicker("val", String(self.fkcategoria));

    $("input[type=file]").fileinput("clear");

    $('#fklinea').selectpicker("val", String(self.fklinea));

    $('#lineaVehiculo').val(self.linea);
    $('#internoVehiculo').val(self.interno);

    listar_internos(self.fklinea,self.fkinterno,self.interno)

    if (self.ruat) {
      $('#icon-ruat').addClass('d-none');
      $('#img-ruat').prop('src', self.ruat);
      $('#img-ruat').removeClass('d-none');
    }

        if (self.frontal) {
      $('#icon-frontal').addClass('d-none');
      $('#img-frontal').prop('src', self.frontal);
      $('#img-frontal').removeClass('d-none');
    }

        if (self.lateral) {
      $('#icon-lateral').addClass('d-none');
      $('#img-lateral').prop('src', self.lateral);
      $('#img-lateral').removeClass('d-none');
    }

            if (self.soat) {
      $('#icon-soat').addClass('d-none');
      $('#img-soat').prop('src', self.soat);
      $('#img-soat').removeClass('d-none');
    }

                if (self.inspeccion) {
      $('#icon-inspeccion').addClass('d-none');
      $('#img-inspeccion').prop('src', self.inspeccion);
      $('#img-inspeccion').removeClass('d-none');
    }


                if (self.seguro) {
      $('#icon-seguro').addClass('d-none');
      $('#img-seguro').prop('src', self.seguro);
      $('#img-seguro').removeClass('d-none');
    }

$('#div_linea').hide();
    $('#div_seleccion').hide();

     $('#div_vehiculo').show();
    $('#div_listaVehiculo').hide();




    $('.item-form').parent().addClass('focused')
    $('#upsert').show()
    $('#insertfile').show()
    $("#cerrar").show();


    botones_admin(admin)

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
        buttons: [
            {  extend : 'excelHtml5',
               exportOptions : { columns : [0, 1, 2]},
                sheetName: 'Lista de Categorias',
               title: 'Lista de Categorias'  },
            {  extend : 'pdfHtml5',
                orientation: 'landscape',
               customize: function(doc) {
                    doc.styles.tableBodyEven.alignment = 'center';
                    doc.styles.tableBodyOdd.alignment = 'center';
               },
               exportOptions : {
                    columns : [0, 1, 2]
                },
               title: 'Lista de Categorias'
            }
        ],
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

$('#transferir').on('click',async function() {

    const obj = {
        id: $("#id").val(),
        fklinea: $("#fklinea").val(),
        fkinterno: $("#fkinterno").val(),
    }


    Swal.fire({
        icon: "warning",
        title: "¿Está seguro de que desea Transferir?",
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
            url: '/vehiculo/transferir/',
            dataType: 'json',
            data: JSON.stringify({'obj':obj}),
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
    }
    })
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
