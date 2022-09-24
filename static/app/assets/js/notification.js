// Bootstrap Notify
const showMessage = (message, type, icon) => {
  $.notify(
    {
      icon: "glyphicon glyphicon-ok",
      message: message,
    },
    {
      type: type,
      allow_dismiss: false,
      placement: {
        from: "bottom",
        align: "center",
      },
      delay: 1000,
      timer: 1000,
      mouse_over: null,
      animate: {
        enter: "animated fadeInDown",
        exit: "animated fadeOutUp",
      },
      template: `
            <div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">
                <span class = "glyphicon glyphicon-${icon}"> </span>
                <span data-notify="message">{2}</span>
            </div>`,
    }
  );
};

const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    onOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})

// SweetAlert 2
const showToast = (category, message, posicion='top-end') => {
    Toast.fire({ icon: category, title: message, position: posicion })
}

const showSmallMessage = (icon, message, position='center', timer=2000) => {
    Swal.fire({
      position: position,
      icon: icon,
      title: message,
      showConfirmButton: false,
      timer: timer
    })
}
