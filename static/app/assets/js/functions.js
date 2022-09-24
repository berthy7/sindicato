// http request
const ajaxCall = (url, data, render, callback) => {
    $.ajax({
        method: "POST",
        url: url,
        data: data,
        success: function (response) {
            if (render) $(render).html(response);
            if (callback) callback(response);
        },
        error: function (jqXHR, status, err) {
            showMessage(jqXHR.responseText, 'danger', 'remove');
        }
    });
}

const ajaxCallGet = (url, data, callback) => {
    $.ajax({
        method: "PUT",
        url: url,
        data: data,
        success: function (response) {
            if (callback) {
                // dictionary = JSON.parse(response)
                dictionary = response
                callback(dictionary)
            }
        },
        error: function (jqXHR, status, err) {
            showMessage('Error', jqXHR.responseText, 'danger', 'remove');
        }
    });
}

const ajaxCallLogin = (url, data, callback) => {
    $.ajax({
        method: "POST",
        url: url,
        data: data,
        success: function (response) {
            dictionary = JSON.parse(response);

            if (callback) callback(dictionary);
        },
        error: function (jqXHR, status, err) {
            showMessage(jqXHR.responseText, 'danger', 'remove');
        }
    });
}

const fetchData = (url, method, data) => {
  try {
    const resquest = fetch(url, {
      method: method,
      body: data,headers:{
            "X-CSRFToken" : getCookie('csrftoken')
        }

    });

    return resquest.json();
  } catch (error) {
    showSmallMessage("error", error);
  }
};

const ajaxData = (params) => {
  const objectRequest = {
    method: params.method,
    url: params.url,
    data: params.data,
    success: function (response) {
      if (params.callback) params.callback(response);
    },
    error: function (jqXHR, status, err) {
      showSmallMessage("error", jqXHR.responseText);
    },
  };

  if (params.hasOwnProperty('formData')) {
    objectRequest.contentType = false;
    objectRequest.processData = false;
    objectRequest.cache = false;
    objectRequest.async = true;
  }

  $.ajax(objectRequest);
};

// helpers
const getCookie = (name) => {
  const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
  return r ? r[1] : undefined;
}

// validate form
const printError = (element, validMessage) => {
  const itemError = document.getElementById(`help-${element.id}`);

  if (itemError) return;

  const invalidItem = document.createElement('div');
  
  invalidItem.setAttribute('id', `help-${element.id}`);
  invalidItem.classList.add('invalid-feedback');
  invalidItem.innerHTML = validMessage;
  element.parentElement.insertAdjacentElement("beforeend", invalidItem);
}

const eraseError = (element) => {
  const itemError = document.getElementById(`help-${element.id}`);
  if (itemError) itemError.parentElement.removeChild(itemError);
}

const getLabel = (itemId) => {
  const itemTag = document.querySelector(`label[for=${itemId}]`);
  return itemTag?.textContent ? itemTag.textContent.replace(" *", "").trim() : null;
}

const validateElements = (params) => {
  let { items, message, labels, flag } = params;

  items.forEach(item => {
      if (item.id) {
          const isValid = item.checkValidity();

          if (!isValid && item.hasAttribute('required')) {
              const errorMessage = item.validationMessage;
              const textFragment = `${item.id}: ${errorMessage}`;
              message += message ? `\n${textFragment}` : textFragment;
              printError(item, errorMessage);
              flag = true;

              const itemLabel = getLabel(item.id);
              if (itemLabel) labels.push(itemLabel);
          }
          else eraseError(item);
      }
  });

  return [flag, message, labels];
}

const formValidation = (id) => {
  let flag = false;
  let message = "";
  let labels = [];
  const formElement = document.getElementById(id);

  const elements = [
    "input[type=text]:enabled",
    "select[required]",
    "input[type=number]:enabled",
    "textarea:enabled",
    "input[type=email]:enabled",
    "input[type=password]:enabled",
    "input[type=file]:enabled",
    "input[type=search]:enabled",
    "input[type=time]:enabled",
  ];

  elements.forEach((item) => {
    const items = document.querySelectorAll(`#${id} ${item}`);
    [flag, message] = validateElements({ items, message, labels, flag });
  });
  formElement.classList.add("was-validated");

  return { error: flag, message: message, labels };
};
