/**
 * Created by bvargas on 10/10/2022.
 */

function ajax_call(url, data, render, callback) {
    $.ajax({
        method: "POST",
        url: url,
        data: data,
        success: function (response) {
            if (render != null) $(render).html(response);
            if (callback != null) callback(response);
        },
        error: function (jqXHR, status, err) {
            // show_message(jqXHR.responseText, 'danger', 'remove');
        }
    });
}