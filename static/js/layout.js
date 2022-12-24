/**
 * Created by bvargas on 21/9/2022.
 */

const btnLogout = document.querySelector(".logout");

btnLogout.addEventListener("click", function () {
  Swal.fire({
    icon: "question",
    title: "¿Desea cerrar sesión?",
    text: "",
    showCancelButton: true,
    allowOutsideClick: false,
    confirmButtonColor: "#727cf5",
    cancelButtonColor: "#ef5350",
    confirmButtonText: "Si",
    cancelButtonText: "No",
  }).then(async (result) => {
    if (result.value) {
      Swal.fire("Gracias por tu trabajo.", "", "success");

      setTimeout(() => (location.href = "/login/logout"), 1500);
    }
  });
});


const btnPerfil = document.querySelector(".account");

btnPerfil.addEventListener("click", function () {
     $.ajax({
        method: "GET",
        url: '/usuario/account',
        dataType: 'json',
        async: false,
        success: function (response) {

          $('#perfil-idu').val(response.userid)
         $('#perfil-name-user').val(response.username)

            if (response.foto) {
              $('#icon-perfil-foto').addClass('d-none');
              $('#img-perfil-foto').prop('src', response.foto);
              $('#img-perfil-foto').removeClass('d-none');
            }


         $('#modal-perfil').modal('show')
        },
        error: function (jqXHR, status, err) {
        }
    });
});

$('#perfil-upd-credentials').on('click',async function() {
      const validationData = formValidation('submit_form_perfil');

      if (validationData.error) {
        showSmallMessage("error", 'Por favor, ingresa todos los campos requeridos (*)');
        return;
      }

      if ($('#perfil-new-pass').val() != $('#perfil-new-rpass').val()) {
        showSmallMessage("warning", 'Las contraseñas no coinciden');
        return;
      }

    const objeto={
           id: $('#perfil-idu').val(),
           newpassword: $('#perfil-new-pass').val()
      };

    $("#perfil-upd-credentials").hide();

   const response =await fetchData(
        "/usuario/changepassword/",
        "POST",
        JSON.stringify({'obj':objeto})
   );
    if(response.success){
       showSmallMessage(response.tipo,response.mensaje,"center");
        setTimeout(function () {
            $('#modal-perfil').modal('hide')

          setTimeout(() => (location.href = "/login/logout"), 500);

        }, 2000);
    }else showSmallMessage(response.tipo,response.mensaje,"center");
});

$('#perfil-upd-foto').on('click',async function() {

    const obj={
           id: $('#perfil-idu').val()
      };

        const getCookieLocal = (name) => {
          const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
          return r ? r[1] : undefined;
        }

    var data = new FormData($('#submit_form_perfil').get(0));
     data.append('obj',JSON.stringify(obj))
        $.ajax({
            method: "POST",
            url: "/usuario/changefoto/",
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
                          $('#modal-perfil').modal('hide')
                    }, 2000);
              }else showSmallMessage(response.tipo,response.mensaje,"center");

            },
            error: function (jqXHR, status, err) {
            }
        });

});
