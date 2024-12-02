//COMMON
const REFILL_SUGGESTION_THRESHOLD = 5

var cache

function set_cache(new_cache) {
    cache = new_cache
}

function clear_error_messages(){
    let error_box = document.querySelector("#date-errors")
    error_box.innerHTML = ""
    error_box = document.querySelector("#message-errors")
    error_box.innerHTML = ""
}

function display_errors(data){
    for (var key in data) {
        let error_box = document.querySelector("#" + key + "-errors")
        error_box.innerHTML = ""
        for (let i = 0; i < data[key].length; i++) {
            error_box.innerHTML += "<li>" + data[key][i] + "</li>"
        }
    }
}

//SUGGESTIONS

function switch_profile(user) {
    block = document.querySelector("#profile-block")
    block.classList.remove("fadeOut")
    block.classList.remove("fadeIn")
    block.offsetWidth
    block.classList.add("fadeOut")

    document.querySelector("#message-input").value = ""
    document.querySelector("#date-input").value = ""
    name_label = document.querySelector("#name")
    name_label.innerHTML = user.name
    id_hidden_input = document.querySelector("#id-hidden")
    id_hidden_input.value = user.id
    //actually change images here once they exist
    img = document.querySelector("#profile-img")
    img.src = user.image_url;
    block.offsetWidth
    block.classList.add("fadeIn")
}

const refill_path = $('#refill-path').data().path

function load_new_suggestions() {
    fetch(refill_path, {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify(cache),
    })
    .then(response => response.json())
    .then(data => {     
        cache.push(...data)
    })
}

function next_user() {
    if (cache == null || cache.length == 0) {
        document.querySelector("#profile-block").style.display = "none"
        document.querySelector("#empty-block").style.display = "block"
        return
    }
    switch_profile(cache[0])
    if (cache.length <= REFILL_SUGGESTION_THRESHOLD) {
        load_new_suggestions()
    } 
}

function handle_response_invite(response) {
    console.log(response)
    clear_error_messages()
    if (response.status == 200) {
        // Handle success - maybe notify the user or load another match
        cache.shift()
        next_user()   
    } else {
        return response.json(); // Parse JSON for error messages
    } 
}

function react_to_suggestion(endpoint, error_string){
    let form = document.querySelector("#invite-form")
    let data = new FormData(form)
    fetch(endpoint, {
        method: "POST",
        body: data,
    })
    .then(handle_response_invite)
    .then(display_errors)
    .catch(error => {
        console.error(error_string, error);
    });
}

//event handlers

const invite_path = $('#invite-path').data().path

function send_invite() {
    react_to_suggestion(invite_path, "Error at invite: ")
}

const reject_path = $('#reject-path').data().path

function send_reject() {
    react_to_suggestion(reject_path, "Error at reject: ")
}

//call to initialize invite page logic

function prepare_invite(){
    const invite_button = document.querySelector("#invite")
    invite_button.addEventListener("click", send_invite)

    const reject_button = document.querySelector("#reject");
    reject_button.addEventListener("click", send_reject);
}


// REPLIES TO INVITATION

function switch_invitation(invitation) {
    block = document.querySelector("#profile-block")
    block.classList.remove("fadeOut")
    block.classList.remove("fadeIn")
    block.offsetWidth
    block.classList.add("fadeOut")

    document.querySelector("#message-input").value = ""
    document.querySelector("#date-input").value = invitation.date
    name_label = document.querySelector("#name")
    name_label.innerHTML = invitation.name
    id_hidden_input = document.querySelector("#id-hidden")
    id_hidden_input.value = invitation.id

    invitation_message_field = document.querySelector("#message-inbound")
    invitation_message_field.value = invitation.message
    if (invitation.message.length == 0){
        invitation_message_field.style.display = "none"
    } else {
        invitation_message_field.style.display = "block"
    }

    date_input = document.querySelector("#date-input")
    date_input.value=invitation.date

    //actually change images here once they exist
    img = document.querySelector("#profile-img")
    img.src = "https://thispersondoesnotexist.com?" + new Date().getTime();
    
    block.offsetWidth
    block.classList.add("fadeIn")
}

function next_invitation() {
    if (cache == null || cache.length == 0) {
        document.querySelector("#profile-block").style.display = "none"
        document.querySelector("#empty-block").style.display = "block"
        return
    }
    switch_invitation(cache[0])
}

function handle_response_reply(response){
    clear_error_messages()
    if (response.status == 200) {
        // Handle success - maybe notify the user or load another match
        cache.shift()
        next_invitation()   
    } else {
        return response.json(); // Parse JSON for error messages
    }
}

function react_to_invitation(endpoint, error_string) {
    let form = document.querySelector("#invite-form")
    let data = new FormData(form)
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

//event handlers

const accept_path = $('#accept-path').data().path

function reply_accept() {
    react_to_invitation(accept_path, "Error at invitation accept: ")
}

const reject_invitation_path = $('#reject-invitation-path').data().path

function reply_reject() {
    react_to_invitation(reject_invitation_path, "Error at invitation reject: ")
}

const ignore_path = $('#ignore-path').data().path

function reply_ignore() {
    react_to_invitation(ignore_path, "Error at invitation ignore: ")
}

const reschedule_path = $('#reschedule-path').data().path

function reply_reschedule() {
    react_to_invitation(reschedule_path, "Error at invitation reschedule: ")
}

//call to initialize answear page logic

function prepare_answear(){
    const accept_button = document.querySelector("#accept");
    accept_button.addEventListener("click", reply_accept);

    const reject_invitation_button = document.querySelector("#reject-invitation");
    reject_invitation_button.addEventListener("click", reply_reject);

    const ignore_button = document.querySelector("#ignore");
    ignore_button.addEventListener("click", reply_ignore);

    const reschedule_button = document.querySelector("#reschedule");
    reschedule_button.addEventListener("click", reply_reschedule);
}