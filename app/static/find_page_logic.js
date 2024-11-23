function set_users(new_users) {
    users = new_users
}

var users


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
        body: JSON.stringify(users),
    })
        .then(response => response.json())
        .then(data => {     
            users.push(...data)
        })
}

function next_user() {
    if (users == null || users.length == 0) {
        document.querySelector("#profile-block").style.display = "none"
        document.querySelector("#empty-block").style.display = "block"
        return
    }
    switch_profile(users[0])
    if (users.length <= 5) {
        load_new_suggestions()
    } 
}

const invite_path = $('#invite-path').data().path

function clear_error_messages(){
    let error_box = document.querySelector("#date-errors")
    error_box.innerHTML = ""
    error_box = document.querySelector("#message-errors")
    error_box.innerHTML = ""
}

invite_button = document.querySelector("#invite")
invite_button.addEventListener("click", send_invite)

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
            users.shift()
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

const reject_button = document.querySelector("#reject");
reject_button.addEventListener("click", send_reject);

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
                users.shift()
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


