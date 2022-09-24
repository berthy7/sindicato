
// TODO: make generic (filter column data, width & export)
const addColumns = () => {
  let aCols = [];

  aCols.push(
    { title: "ID", data: "id" },
    { title: "Codigo", data: "codigo" },
    { title: "Numero", data: "numero" },
    {
      title: "Estado",
      data: "estado",
      render: function (data, type, row) {
        return `
           <div class="form-group">
            <div class="custom-control custom-checkbox">
              <input type="checkbox" class="custom-control-input enable" id="check${row.id}" 
                data-id="${row.id}" ${row.check}>
                <label class="custom-control-label" for="check${row.id}">
                  ${data}
                </label>
            </div>
           </div>`;
      },
    }
  );

  aCols.push({
    title: "Acciones",
    data: "id",
    render: function (data, type, row) {
      let actionHtml = `
        <button data-id="${data}" type="button" class="btn btn-primary edit" title="Editar">
          <i class="mdi mdi-file-document-edit"></i>
        </button>
        <button data-id="${data}" type="button" class="btn btn-danger delete" title="Eliminar">
          <i class="mdi mdi-delete"></i>
        </button>`;

      if (!actionHtml) actionHtml = "Sin permisos";

      return actionHtml;
    },
  });

  return aCols;
};

const reloadTable = async () => {
  const response = await fetchData(
    "/domicilio/list",
    "GET",
    getFormData()
  );

    console.log("response",response)
  if (response.hasOwnProperty("data")) {
    loadTable({
      tableId: "data_table",
      data: response.data,
      columns: addColumns(),
      order: [[0, "desc"]],
      columnWidth: [
        { width: "15%", targets: [0] },
        { width: "30%", targets: [1, 2] },
        { width: "25%", targets: [3] },
      ],
    });
  } else showToast("warning", "No se pudo obtener los datos.");
};

$("#new").click(function () {
  $("#update").hide();
  $("#insert").show();
  $(".form-control").val("");
  $("#modal").modal("show");
});

$("#data_table").on("click", "button.edit", async function (e) {
  editItem({
    id: Number(this.dataset.id),
    route: "ciudad_update",
    method: "PUT",
    callback: (item) => {
      $("#id").val(item.id);
      $("#nombre").val(item.nombre);

      $(".form-control").parent().find("label").addClass("active");
      $("#insert").hide();
      $("#update").show();
      $("#modal").modal("show");
    },
  });
});

// TODO: validate form
$("#insert, #update").on("click", async function () {
  const objectData = {
    nombre: $("#nombre").val(),

  };

  upsertItem({
    id: Number($("#id").val()),
    actionId: this.id,
    objectData,
    routes: ["ciudad_insert", "ciudad_update"],
    method: "POST",
    callback: () => reloadTable(),
  });
});

$("#data_table").on("click", "input.enable", async function (e) {
  enableItem({
    item: this,
    route: "ciudad_state",
    method: "POST",
    callback: () => reloadTable(),
  });
});

$("#data_table").on("click", "button.delete", async function (e) {
  deleteItem({
    id: Number(this.dataset.id),
    route: "ciudad_delete",
    method: "POST",
    callback: () => reloadTable(),
  });
});

document.addEventListener("DOMContentLoaded", function (e) {
  reloadTable();
});
