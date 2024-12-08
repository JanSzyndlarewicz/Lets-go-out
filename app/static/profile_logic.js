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