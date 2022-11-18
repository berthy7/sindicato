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
