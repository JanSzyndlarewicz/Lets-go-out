const like_path = $('#like-path').data().path
const block_path = $('#block-path').data().path

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
    console.log(like_button)
    like_button.addEventListener("click", like)

    const block_button = document.querySelector('#block-button')
    block_button.addEventListener("click", block)
}

function change_like_button_appearance(){
    console.log("Now I'm supposed to change the appearance of the like button.")
}

function change_block_button_appearance(){
    console.log("Now I'm supposed to change the appearance of the block button.")
}

$(function(){
    prepare_event_handlers()
})