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
