const getFormData = (objectData = {}) => {
  const formData = new FormData();
  const params = {
    object: JSON.stringify(objectData),
    _xsrf: getCookie("_xsrf"),
  };

  Object.entries(params).forEach(([key, value]) => {
    formData.append(key, value);
  });

  return formData;
};

const processRequest = async (params) => {
  const response = await fetchData(
    params.route,
    params.method,
    getFormData(params.objectData)
  );
  const icon = response.success ? "success" : "warning";

  if (params?.hideModal && response.success) $("#modal").modal("hide");
  showSmallMessage(icon, response.message, "center");

  if (response.success) {
    setTimeout(() => {
      params.callback();
    }, 2000);
  }
};

const getButtons = (buttonsExport) => {
  const { items, data } = buttonsExport;
  const dataExport = items.map((button) => {
    const item = {
      extend: button,
      exportOptions: {
        columns: data.columnsExport,
      },
    };

    if (button == 'excel') {
        item.title = data.title;
        item.sheetName = data.sheet;
    }

    if (button == "pdf") {
      item.exportOptions.alignment = "center";
      item.title = data.title;
      item.footer = true;
      item.orientation = "portrait";
      item.pageSize = "letter";
      item.customize = (doc) => {
        doc.styles.tableHeader.alignment = "left";
        doc.pageMargins = [20, 30, 15, 30];
      };
    }

    return item;
  });

  return dataExport;
};

const loadTable = (params) => {
  const objectTable = {
    data: params.data,
    destroy: true,
    deferRender: true,
    columns: params.columns,
    language: {
      url: "/resources/app/plugins/jquery-datatable/es-ES.json",
    },
  };

  if (params?.order) objectTable.order = params.order;
  if (params?.columnWidth) objectTable.columnDefs = params.columnWidth;

  if (params?.createdRowCallback)
    objectTable.createdRow = (row, data, dataIndex) => {
      params.createdRowCallback(row, data, dataIndex);
    };

  if (params?.initCompleteCallback)
    objectTable.initComplete = (row, data, dataIndex) => {
      params.initCompleteCallback(row, data, dataIndex);
    };

  if (params?.buttonsExport) {
    objectTable.dom = "Bfrtip";
    objectTable.buttons = getButtons(params.buttonsExport);
  }

  $(`#${params.tableId}`).DataTable(objectTable);
};

const editItem = async (params) => {
  const objectData = {
    id: params.id,
  };
  const responseData = fetchData(
    params.route,
    params.method,
    getFormData(objectData)
  );

  if (responseData.success) {
    const item = responseData.response;
    params.callback(item);
  } else showSmallMessage("warning", response.message, "center");
};

const upsertItem = (params) => {
  const route =
    params.actionId == "update" ? params.routes[1] : params.routes[0];

  if (params.hasOwnProperty('formData')) {
    ajaxData({
      url: route,
      method: params.method,
      data: params.objectData,
      formData: true,
      callback: (response) => {
        const data = JSON.parse(response);
        const icon = data.success ? "success" : "warning";
        showSmallMessage(icon, data.message, "center");

        if (data.success) {
          $("#modal").modal("hide");
          params.callback();
        }
      },
    });
  } else {
    if (params.actionId == "update") 
      params.objectData.id = params.id;

    processRequest({
      route,
      method: params.method,
      objectData: params.objectData,
      hideModal: true,
      callback: () => params.callback(),
    });
  }
};

const enableItem = (params) => {
  const checkValue = params.item.checked;
  const fragmentTitle = "Está seguro de que desea";
  const dataTitle = checkValue
    ? `¿${fragmentTitle} Activar?`
    : `¿${fragmentTitle} Desativar?`;
  const dataIcon = checkValue ? "info" : "warning";
  $(`label[for=${params.item.id}]`).html(checkValue ? "Activo" : "Inactivo");

  Swal.fire({
    icon: dataIcon,
    title: dataTitle,
    text: "",
    showCancelButton: true,
    allowOutsideClick: false,
    confirmButtonColor: "#1565c0",
    cancelButtonColor: "#ef5350",
    confirmButtonText: "Aceptar",
    cancelButtonText: "Cancelar",
  }).then(async (result) => {
    if (result.value) {
      const objectData = {
        id: Number(params.item.dataset.id),
        state: checkValue,
      };

      processRequest({
        route: params.route,
        method: params.method,
        objectData,
        callback: () => params.callback(),
      });
    } else if (result.dismiss === "cancel" || result.dismiss === "esc") {
      $(params.item).prop("checked", !$(params.item).is(":checked"));
      $(`label[for=${params.item.id}]`).html(
        $(params.item).is(":checked") ? "Activo" : "Inactivo"
      );
    }
  });
};

const deleteItem = (params) => {
  Swal.fire({
    icon: "warning",
    title: "¿Está seguro de Eliminar?",
    text: "",
    showCancelButton: true,
    allowOutsideClick: false,
    confirmButtonColor: "#1565c0",
    cancelButtonColor: "#ef5350",
    confirmButtonText: "Aceptar",
    cancelButtonText: "Cancelar",
  }).then(async (result) => {
    if (result.value) {
      const objectData = {
        id: params.id,
      };

      processRequest({
        route: params.route,
        method: params.method,
        objectData,
        callback: () => params.callback(),
      });
    }
  });
};

// export { getFormData, processRequest, loadTable, editItem, upsertItem, enableItem, deleteItem };
