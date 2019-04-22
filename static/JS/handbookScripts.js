function AJAX_add_data(name, column_id, event_id, column_for_adding) {
    $.ajax({
        type: "GET",   // Тип запроса
        url: "/collect_data/",   // Путь к сценарию, обработающему запрос
        dataType: "json",   // Тип данных, в которых сервер должен прислать ответ
        data: "column_id=" + column_id + "&name=" + name + "&event_id=" + event_id,
        error: function () {
            alert("При выполнении запроса произошла ошибка :(");
        },
        success: function (data) {
            for (let i = 0; i < data.length; i++) {
                let current_container = $('<div id="container_' + data[i] + '"></div>');
                $('#' + column_for_adding).append(current_container);
                current_container.append('<input id="' + data[i] +'" type="checkbox" value="' + data[i] + '" onchange="click_on_class(this)">' + '<label for="' + data[i] + '"> ' + data[i] + '</label> <br>');
            }
        }
    })
}


function AJAX_remove_data(name, column_id, event_id) {
    $.ajax({
        type: "GET",   // Тип запроса
        url: "/collect_data/",   // Путь к сценарию, обработающему запрос
        dataType: "json",   // Тип данных, в которых сервер должен прислать ответ
        data: "column_id=" + column_id + "&name=" + name + "&event_id=" + event_id,
        error: function () {
            alert("При выполнении запроса произошла ошибка :(");
        },
        success: function (data) {
            for (let i = 0; i < data.length; i++) {
                $('#container_' + data[i]).remove();
            }
        }
    })
}


function click_on_class(class_element) {
    let columns = ['classes', 'groups', 'subgroups', 'elements'];
    let class_name = class_element.id;
    let column_id = $(class_element).parent().parent().attr("id");
    if (column_id !== 'elements'){
        if (class_element.checked){
            let event_id = 0;
            AJAX_add_data(class_name, column_id, event_id, columns[columns.indexOf(column_id) + 1]);
        }
        else{
            let event_id = 1;
            AJAX_remove_data(class_name, column_id, event_id);
        }
    }
}

