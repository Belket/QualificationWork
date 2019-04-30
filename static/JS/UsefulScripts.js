function add_table_row() {
    let rows_number = $('#offer_table >tbody >tr').length;
    let row_content = $('#row_' + rows_number).html();
    let row_id = 'row_' + (rows_number + 1);
    $('#offer_table >tbody').append('<tr id="' + row_id + '"></tr>');
    $('#' + row_id).append(row_content);
    $('#' + row_id + '>th').html((rows_number + 1));

    let class_column = $('#' + row_id + '> td > #class_' + rows_number);
    let group_column = $('#' + row_id + '> td > #group_' + rows_number);
    let subgroup_column = $('#' + row_id + '> td > #subgroup_' + rows_number);
    class_column.attr("id", 'class_' + (rows_number + 1));
    group_column.attr("id", 'group_' + (rows_number + 1));
    subgroup_column.attr("id", 'subgroup_' + (rows_number + 1));

    group_column.attr("list", 'groups_' + (rows_number + 1));
    subgroup_column.attr("list", 'subgroups_' + (rows_number + 1));
    $('#' + row_id + '> td > #groups_' + rows_number).attr("id", 'groups_' + (rows_number + 1));
    $('#' + row_id + '> td > #subgroups_' + rows_number).attr("id", 'subgroups_' + (rows_number + 1));
}


function collect_groups(element){
    let row = element.id.split('_')[1];
    let name = element.value;
    let groups_data_list = $('#row_' + row + '> td > #groups_' + row);
    $.ajax({
        type: "GET",   // Тип запроса
        url: "/collect_for_table/",   // Путь к сценарию, обработающему запрос
        dataType: "json",   // Тип данных, в которых сервер должен прислать ответ
        data: "name=" + name + '&type=' + 0,
        error: function () {
            alert("При выполнении запроса произошла ошибка :(");
        },
        success: function (data) {
            groups_data_list.html("");
            for (let i = 0; i < data.length; i++) {
                groups_data_list.append('<option>' + data[i] + '</option>');
            }
        }
    })
}


function collect_subgroups(element){
    let row = element.id.split('_')[1];
    let name = element.value;
    let subgroups_data_list = $('#row_' + row + '> td > #subgroups_' + row);
    $.ajax({
        type: "GET",   // Тип запроса
        url: "/collect_for_table/",   // Путь к сценарию, обработающему запрос
        dataType: "json",   // Тип данных, в которых сервер должен прислать ответ
        data: "name=" + name + '&type=' + 1,
        error: function () {
            alert("При выполнении запроса произошла ошибка :(");
        },
        success: function (data) {
            subgroups_data_list.html("");
            for (let i = 0; i < data.length; i++) {
                subgroups_data_list.append('<option>' + data[i] + '</option>');
            }
        }
    })
}