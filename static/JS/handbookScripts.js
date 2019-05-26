
// -------------------------- GETTING OBJECTS DYNAMIC -------------------------


function click_handler(object){
    let column_id = "column_" + parseInt(object.id.split("_")[0]);
    if (column_id !== "column_3"){
        if (object.checked){
            let event = 0;
            AJAX_add_data(object, event);
        }
        else{
            let event = 1;
            AJAX_remove_data(object, event);
        }
    }
    else{
        let elements_block = document.getElementById(column_id);
        elements_block.setAttribute("class", "checked");
        if ((coins === 0) && (object.checked === true)) {
            offer_to_earn(coins);
            object.checked = false;
        }
    }
    if (document.getElementById("column_3").children.length === 0){document.getElementById("coins").value = start_coins}
}


function AJAX_add_data(object, event) {
    let column_id = "column_" + (parseInt(object.id.split("_")[0]) + 1);
    let object_id = parseInt(object.id.split("_")[1]);
    $.ajax({
        type: "GET",   // Тип запроса
        url: "/collect_data/",   // Путь к сценарию, обработающему запрос
        dataType: "json",   // Тип данных, в которых сервер должен прислать ответ
        data: "id=" + object.id +"&event=" + event,
        error: function () {
            console.log("При выполнении запроса произошла ошибка :(");
        },
        success: function (data) {
            for (let i = 0; i < data.length; i++) {
                let current_container = $('<div id="container_' + data[i]["id"] + '"></div>');
                $('#' + column_id).append(current_container);
                current_container.append('<input id="' + data[i]['id'] +'" name="' + data[i]['id'] + '" type="checkbox" value="' + data[i]['id'] + '" onchange="click_handler(this)">' + '<label for="' + data[i]['id'] + '"> ' + data[i]['name'] + '</label> <br>');
            }
        }
    })
}


function AJAX_remove_data(object, event) {
    $.ajax({
        type: "GET",   // Тип запроса
        url: "/collect_data/",   // Путь к сценарию, обработающему запрос
        dataType: "json",   // Тип данных, в которых сервер должен прислать ответ
        data: "id=" + object.id + "&event=" + event,
        async: false,
        error: function () {
            console.log("При выполнении запроса произошла ошибка :(");
        },
        success: function (data) {
            for (let i = 0; i < data.length; i++) {
                console.log(data[i]);
                $('#container_' + data[i]).remove();
            }
        }
    })
}













// set default states to checkboxes
function set_checkbox_state() {
    $(":checkbox").prop("checked", false);
}


// removing excel and pdf files
function activate_removing() {
    window.onbeforeunload = function(){$.get("/remove_files/");}
}


function offer_to_earn() {
    let message = "У вас закончились деньги, чтобы доюавить больше элементов, участвуйте в развитии проекта";
    let href = "<a href='/offer_element/'> Заработать валюту </a>";
    let content = "<div>" + message + href + "</div>";
    alert(message)
}


// observe changes in elements
function observe_mutations(){
  let mutationObserver = new MutationObserver(function(mutations) {
  mutations.forEach(function(mutation) {
      let current_value = 0;
      let children = document.getElementById("column_3").children;
      for(let child = 0; child < children.length; child++){
          let element_id =  document.getElementById(children[child].id).id;
          let object = element_id.split('_')[1] + '_' + element_id.split('_')[2];
          console.log(object);
          if (document.getElementById(object).checked === true) {current_value += 1}
      }
      coins += old_checked_value - current_value;
      old_checked_value = current_value;
      document.getElementById("coins").value = coins;
    });
  });


  mutationObserver.observe(document.getElementById("column_3"), {
  attributes: true,
  characterData: true,
  childList: true,
  subtree: true,
  attributeOldValue: true,
  characterDataOldValue: true
});
}


// start observation
function prepare_observe(){
    start_coins = parseInt(document.getElementById("coins").value);
    old_checked_value = 0;
    coins = parseInt(document.getElementById("coins").value);
    if (coins === 0) {offer_to_earn(coins)}
    observe_mutations();
}


// on load function
function initialize_page() {
    set_checkbox_state();
    prepare_observe();
}

