const like_path = $('#like-path').data().path
const block_path = $('#block-path').data().path
const invite_path = $('#invite-path').data().path
const reject_path = $('#reject-path').data().path

function call_endpoint(endpoint, on_success){
    fetch(endpoint, {
        method: "POST",
    })
    .then( (response) => response.status)
    .then(code => {
        if (code == 200) {
            on_success()
        } 
    })
}

function like(){
    call_endpoint(like_path, change_like_button_appearance)
}

function block(){
    call_endpoint(block_path, change_block_button_appearance)
}

function prepare_event_handlers(){
    const like_button = document.querySelector('#like-button')
    like_button.addEventListener("click", like)

    const block_button = document.querySelector('#block-button')
    block_button.addEventListener("click", block)

    const accept_button = document.querySelector("#invite");
    accept_button.addEventListener("click", invite);

    const reject_invitation_button = document.querySelector("#reject");
    reject_invitation_button.addEventListener("click", reject);
}

function change_like_button_appearance(){
    const like_button = document.querySelector('#like-button')
    if (like_button.classList.contains('fas')) {
        like_button.classList.remove('fas')
        like_button.classList.add('text-color')
        like_button.classList.add('far')
    } else {
        like_button.classList.remove('far')
        like_button.classList.remove('text-color')
        like_button.classList.add('fas')
    }
}

function change_block_button_appearance(){
    const block_button = document.querySelector('#block-button')
    if (block_button.classList.contains('text-color')) {
        block_button.classList.remove('text-color')
    } else {
        block_button.classList.add('text-color')
    }
}

$(function(){
    prepare_event_handlers()
})

function reject(){
    send_form(reject_path, "Error at reject: ")
}

function invite(){
    send_form(invite_path, "Error at invite: ")
}

function hide_invite_form(){
    const invite_form = document.querySelector('#date-request-tile')
    invite_form.innerHTML = "<h2 class='padding-all-15'>Invitation sent!</h2>"
    console.log(invite_form)
}

function send_form(endpoint, error_string){
    let form = document.querySelector("#invite-form")
    let data = new FormData(form)
    console.log(form)
    console.log(data)
    fetch(endpoint, {
        method: "POST",
        body: data,
    })
    .then(handle_response_reply)
    .then(display_errors)
    .catch(error => {
        console.error(error_string, error);
    });
}

function clear_error_messages(){
    let error_box = document.querySelector("#date-errors")
    error_box.innerHTML = ""
    error_box = document.querySelector("#message-errors")
    error_box.innerHTML = ""
}

function display_errors(data){
    console.log(data)
    for (var key in data) {
        let error_box = document.querySelector("#" + key + "-errors")
        error_box.innerHTML = ""
        for (let i = 0; i < data[key].length; i++) {
            error_box.innerHTML += "<li>" + data[key][i] + "</li>"
        }
    }
}

function handle_response_reply(response){
    clear_error_messages()
    if (response.status == 200) {
        hide_invite_form()
    } else {
        return response.json(); 
    }
}