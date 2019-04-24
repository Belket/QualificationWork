
// click on checkbox to check
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



// click on checkbox to uncheck
function AJAX_remove_data(name, column_id, event_id) {
    $.ajax({
        type: "GET",   // Тип запроса
        url: "/collect_data/",   // Путь к сценарию, обработающему запрос
        dataType: "json",   // Тип данных, в которых сервер должен прислать ответ
        data: "column_id=" + column_id + "&name=" + name + "&event_id=" + event_id,
        async: false,
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


// next level of elements
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
    else{
        let elements_block = document.getElementById(column_id);
        elements_block.setAttribute("class", "checked");
    }

    if (document.getElementById("elements").children.length === 0){document.getElementById("coins").innerHTML = start_coins}
    console.log(document.getElementById("elements").children.length);
}


// set default states to checkboxes
function set_checkbox_state() {
    $(":checkbox").prop("checked", false);
}


// removing excel and pdf files
function activate_removing() {
    console.log("im heger");
    window.onbeforeunload = function(){$.get("/remove_files/");}
}


function observe_mutations(){
  let mutationObserver = new MutationObserver(function(mutations) {
  mutations.forEach(function(mutation) {
      let current_value = 0;
      let children = document.getElementById("elements").children;
      for(let child = 0; child < children.length; child++){
          let class_name = document.getElementById(children[child].id).id.split('_')[1];
          if (document.getElementById(class_name).checked === true) {current_value += 1}
          coins += old_checked_value - current_value;
          old_checked_value = current_value;
          document.getElementById("coins").innerHTML = coins;
      }
    });
  });


  mutationObserver.observe(document.getElementById("elements"), {
  attributes: true,
  characterData: true,
  childList: true,
  subtree: true,
  attributeOldValue: true,
  characterDataOldValue: true
});
}


function prepare_observe(){
    start_coins = parseInt(document.getElementById("coins").innerHTML);
    old_checked_value = 0;
    coins = parseInt(document.getElementById("coins").innerHTML);
    console.log("Observer");
    observe_mutations();
}


function initialize_page() {
    set_checkbox_state();
    prepare_observe();
}