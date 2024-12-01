const like_path = $('#like-path').data().path
const block_path = $('#block-path').data().path

function call_endpoint(endpoint){
    let user_id = $('#user-id').data().path
    fetch(endpoint + "/" + user_id, {
        method: "POST",
    })
}

function like(){
    call_endpoint(like_path)
}

function block(){
    call_endpoint(block_path)
}

function prepare_event_handlers(){

}