function create_post_form(action){
    let post_form = document.createElement("form");
    post_form.action = action;
    post_form.method = "post";
    return post_form
}


function exam_element(decision){
    let action;
    if (decision === "confirm"){action = "/admin/offer/confirm/"}
    else {action = "/admin/offer/reject/"}
    let page_content = document.body.innerHTML;
    let post_form = create_post_form(action);
    post_form.innerHTML = page_content;
    document.body.appendChild(post_form);
    post_form.submit();
}

