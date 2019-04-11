function send_for_result(result, test_number) {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', location.href, true);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));

    if (xhr.readyState === 4) {
        if (xhr.status === 200) {
            console.log("Status 200");
        } else {
            console.log("Error");
        }
    }

    let body = new FormData();
    body.append('result', result.toLowerCase());
    body.append('test_number', test_number);
    xhr.send(body);
}


function click_on_class(checked) {
    console.log(checked)
}




(function () {
    "use strict";
    jQuery(function () {
        $('#type').change(function () {
            alert("При выполнении запроса произошла ошибка :(");
            $('#kind, #category').find('option:not(:first)')    // Ищем все теги option, не являющиеся тегом по умолчанию
                .remove()   // Удаляем эти теги
                .end()      // Возвращаемся к исходному объекту
                .prop('disabled', true);       // Делаем поля неактивными
            let type_id = $(this).val();
            if (type_id == 0) {
                return;
            }
            $.ajax({
                type: "POST",   // Тип запроса
                url: "query.php",   // Путь к сценарию, обработающему запрос
                dataType: "json",   // Тип данных, в которых сервер должен прислать ответ
                data: "query=getKinds&type_id=" + type_id,  // Строка POST-запроса
                error: function () {    // Обработчик, который будет запущен в случае неудачного запроса
                    alert("При выполнении запроса произошла ошибка :(");  // Сообщение о неудачном запросе
                },
                success: function (data) {
                    for (let i = 0; i < data.length; i++) {
                        // Каждое полученное значение вставим в список видов транспорта
                        $('#kind').append('<option value="' + data[i].kind_id + '">' + data[i].kind + '</option>');
                    }
                    $('#kind').prop('disabled', false); // Включаем поле
                }
            });
        });
    });
});