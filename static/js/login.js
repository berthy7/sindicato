var id_table = '#data_table';
var class_item = '.item-form';

window.addEventListener("load", function () {
   // reload_table()
});

function add_columns() {
    let a_cols = []
    a_cols.push(
        { title: "ID", data: "id" },
        { title: "Usuario", data: "usuario.username" },
        { title: "IP", data: "ip" },
        { title: "Accion", data: "accion" },
        { title: "Fecha", data: "fecha" }
    );

    return a_cols;
}

function load_table(data_tb) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: data_tb,
        columns: add_columns(),
        order: [ [0, 'desc'] ],
        // columnDefs: [ { width: '33%', targets: [0, 1,2] } ],
        initComplete: function() {
        }
    });
    tabla.columns.adjust().draw();
}

function reload_table() {
    $.ajax({
        method: "POST",
        url: 'log_list',
        dataType: 'json',
        data: {_xsrf: getCookie("_xsrf")},
        async: false
    }).done(function(response) {
        load_table(response.data)
    }).fail(function() {
        show_toast('warning', 'No se pudo obtener los datos.')
    })
}

$('#new').click(function() {
    $('#update').hide()
    $('#insert').show()
    $('#modal').modal('show')
});

$('#insert').on('click', function() {
    objeto = JSON.stringify({
        'nombre': $('#nombre').val()
    })
    ajaxCall('log_insert', {
        object: objeto,
        _xsrf: getCookie("_xsrf")
    }, null, function (response) {
        self = JSON.parse(response)
        if (self.success) {
            setTimeout(function () {
                $('#modal').modal('hide')
                reload_table()
            }, 2000);
        }
    })
});

function edit_item(e) {
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(e).attr('data-json')))
    })
    ajaxCallGet('log_update',{
        _xsrf: getCookie("_xsrf"),
        object: obj
    },function(response){
        response = JSON.parse(response);
        self = response.response

        $('#id').val(self.id)
        $('#nombre').val(self.nombre)

        $('.item-form').parent().find("label").addClass("active")
        $('#insert').hide()
        $('#update').show()
        $('#modal').modal('show')
    })
}


$('#update').click(function() {
    objeto = JSON.stringify({
        'id': parseInt($('#id').val()),
        'nombre': $('#nombre').val()
    })
    ajaxCall('log_update', {
        _xsrf: getCookie("_xsrf"),
        object: objeto
    }, null, function(response) {
        self = JSON.parse(response)

        if (self.success) {
            setTimeout(function () {
                $('#modal').modal('hide')
                reload_table()
            }, 2000);
        }
    })
})

function set_enable(e) {
    cb_delete = e
    b = $(e).prop('checked')
    if(!b) {
        cb_title = "¿Está seguro de que desea Desativar?"
        cb_text = ""
        cb_type = "warning"
    } else {
        cb_title ="¿Está seguro de que desea Activar?"
        cb_text = ""
        cb_type = "info"
    }

    Swal.fire({
        icon: 'question',
        title: cb_title,
        text: cb_text,
        type: cb_type,
        showCancelButton: true,
        allowOutsideClick: false,
        confirmButtonColor: '#1565c0',
        cancelButtonColor: '#ef5350',
        confirmButtonText: 'Aceptar',
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.value) {
            $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))
            if (b) $(cb_delete).parent().prop('title', 'Activo')
            else $(cb_delete).parent().prop('title', 'Inhabilitado')

            objeto =JSON.stringify({
                id: parseInt($(cb_delete).attr('data-id')),
                state: b
            })
            ajaxCall('log_state', {
                object: objeto,_xsrf: getCookie("_xsrf")}, null,
                function () {
                    setTimeout(function() {
                        reload_table()
                    }, 2000);
                }
            )
        }
        else if(result.dismiss === 'cancel'){
            $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))
        }
        else if(result.dismiss === 'esc'){
            $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))
        }
    })
}

function delete_item(e) {

    Swal.fire({
    icon: 'question',
    title: "¿Está seguro de Eliminar?",
    text: "",
    type: "warning",
    showCancelButton: true,
    allowOutsideClick: false,
    confirmButtonColor: '#1565c0',
    cancelButtonColor: '#ef5350',
    confirmButtonText: 'Aceptar',
    cancelButtonText: "Cancelar"
}).then((result) => {
    if (result.value) {
        objeto = JSON.stringify({
            id: parseInt(JSON.parse($(e).attr('data-id'))),
        })
        ajaxCall('log_delete', {
            object: objeto,_xsrf: getCookie("_xsrf")}, null,
            function () {
                setTimeout(function() {
                    reload_table()
                }, 2000);
            }
        )
    }
})
}
