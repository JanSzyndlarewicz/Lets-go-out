function set_cache(new_cache) {
    cache = new_cache
}

var cache

function switch_profile(user) {
    //console.log("Switching to user " + user.id)
    document.querySelector("#message-input").value = ""
    document.querySelector("#date-input").value = ""
    name_label = document.querySelector("#name")
    name_label.innerHTML = user.name
    id_hidden_input = document.querySelector("#id-hidden")
    id_hidden_input.value = user.id
    //actually change images here once they exist
    img = document.querySelector("#profile-img")
    img.src = "https://thispersondoesnotexist.com?" + new Date().getTime();
    
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
    if (cache.length <= 5) {
        load_new_suggestions()
    } 
}

function switch_invitation(invitation) {
    //console.log("Switching to user " + user.id)
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
    console.log(invitation.date)
    date_input.value=invitation.date

    //actually change images here once they exist
    img = document.querySelector("#profile-img")
    img.src = "https://thispersondoesnotexist.com?" + new Date().getTime();
    
}

function next_invitation() {
    if (cache == null || cache.length == 0) {
        document.querySelector("#profile-block").style.display = "none"
        document.querySelector("#empty-block").style.display = "block"
        return
    }
    switch_invitation(cache[0])
}

function clear_error_messages(){
    let error_box = document.querySelector("#date-errors")
    error_box.innerHTML = ""
    error_box = document.querySelector("#message-errors")
    error_box.innerHTML = ""
}


const invite_path = $('#invite-path').data().path

function send_invite() {
    let form = document.querySelector("#invite-form")
    let data = new FormData(form)
    fetch(invite_path, {
        method: "POST",
        body: data,
    })
    .then(response => response.json())
    .then(response => {
        clear_error_messages()
        if (response === true) {
            // Handle success - maybe notify the user or load another match
            cache.shift()
            next_user()   
        } else {
            return response; // Parse JSON for error messages
        }
        
        })
        .then(data => {
            for (var key in data) {
                let error_box = document.querySelector("#" + key + "-errors")
                error_box.innerHTML = ""
                for (let i = 0; i < data[key].length; i++) {
                    error_box.innerHTML += "<li>" + data[key][i] + "</li>"
                }
            }
        })
        .catch(error => {
            console.error("Error during rejection:", error);
        });
}

const reject_path = $('#reject-path').data().path



function send_reject() {
    let form = document.querySelector("#invite-form")
    let data = new FormData(form)
    clear_error_messages()
    fetch(reject_path, {
        method: "POST",
        body : data,
    })
    .then(response => {
        if (response.ok) {
            // Handle success - maybe notify the user or load another match
            cache.shift()
            next_user()
        } else {
            return response.json(); // Parse JSON for error messages
        }
    })
    .then(data => {
        if (data) {
            // Display errors dynamically
            let error_box = document.querySelector("#date-errors"); // Adjust the selector for errors
            error_box.innerHTML = "";
            if (data.errors) {
                data.errors.forEach(error => {
                    error_box.innerHTML += `<li>${error}</li>`;
                });
            }
        }
    })
    .catch(error => {
        console.error("Error during rejection:", error);
    });  
}

function prepare_invite(){
    const invite_button = document.querySelector("#invite")
    invite_button.addEventListener("click", send_invite)

    const reject_button = document.querySelector("#reject");
    reject_button.addEventListener("click", send_reject);
}

const accept_path = $('#accept-path').data().path

function reply_accept() {
    let form = document.querySelector("#invite-form")
    let data = new FormData(form)
    fetch(accept_path, {
        method: "POST",
        body: data,
    })
    .then(response => response.json())
    .then(response => {
        clear_error_messages()
        if (response === true) {
            // Handle success - maybe notify the user or load another match
            cache.shift()
            next_invitation()   
        } else {
            return response; // Parse JSON for error messages
        }
        
        })
        .then(data => {
            for (var key in data) {
                let error_box = document.querySelector("#" + key + "-errors")
                error_box.innerHTML = ""
                for (let i = 0; i < data[key].length; i++) {
                    error_box.innerHTML += "<li>" + data[key][i] + "</li>"
                }
            }
        })
        .catch(error => {
            console.error("Error during accepting:", error);
        });
}

const reject_invitation_path = $('#reject-invitation-path').data().path

function reply_reject() {
    let form = document.querySelector("#invite-form")
    let data = new FormData(form)
    fetch(reject_invitation_path, {
        method: "POST",
        body: data,
    })
    .then(response => response.json())
    .then(response => {
        clear_error_messages()
        if (response === true) {
            // Handle success - maybe notify the user or load another match
            cache.shift()
            next_invitation()   
        } else {
            return response; // Parse JSON for error messages
        }
        
        })
        .then(data => {
            for (var key in data) {
                let error_box = document.querySelector("#" + key + "-errors")
                error_box.innerHTML = ""
                for (let i = 0; i < data[key].length; i++) {
                    error_box.innerHTML += "<li>" + data[key][i] + "</li>"
                }
            }
        })
        .catch(error => {
            console.error("Error during rejecting:", error);
        });
}

const ignore_path = $('#ignore-path').data().path

function reply_ignore() {
    let form = document.querySelector("#invite-form")
    let data = new FormData(form)
    fetch(ignore_path, {
        method: "POST",
        body: data,
    })
    .then(response => response.json())
    .then(response => {
        clear_error_messages()
        if (response === true) {
            // Handle success - maybe notify the user or load another match
            cache.shift()
            next_invitation()   
        } else {
            return response; // Parse JSON for error messages
        }
        
        })
        .then(data => {
            for (var key in data) {
                let error_box = document.querySelector("#" + key + "-errors")
                error_box.innerHTML = ""
                for (let i = 0; i < data[key].length; i++) {
                    error_box.innerHTML += "<li>" + data[key][i] + "</li>"
                }
            }
        })
        .catch(error => {
            console.error("Error during ignoring:", error);
        });
}

const reschedule_path = $('#reschedule-path').data().path

function reply_reschedule() {
    let form = document.querySelector("#invite-form")
    let data = new FormData(form)
    fetch(reschedule_path, {
        method: "POST",
        body: data,
    })
    .then(response => response.json())
    .then(response => {
        clear_error_messages()
        if (response === true) {
            // Handle success - maybe notify the user or load another match
            cache.shift()
            next_invitation()   
        } else {
            return response; // Parse JSON for error messages
        }
        
        })
        .then(data => {
            for (var key in data) {
                let error_box = document.querySelector("#" + key + "-errors")
                error_box.innerHTML = ""
                for (let i = 0; i < data[key].length; i++) {
                    error_box.innerHTML += "<li>" + data[key][i] + "</li>"
                }
            }
        })
        .catch(error => {
            console.error("Error during rescheduling:", error);
        });
}

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