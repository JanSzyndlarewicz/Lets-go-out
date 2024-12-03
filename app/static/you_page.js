

$(document).ready(function() {
    const likedButton = $('.switch-to-liked').first()
    const blockedButton = $('.switch-to-blocked').first()
    console.log(likedButton)
    console.log(blockedButton)
    likedButton.on('click', getLiked)
    blockedButton.on('click', getBlocked)
    const editProfileIcon = $('#edit-profile-icon')
    editProfileIcon.on('click', function() {
        window.location.href = editProfilePath
    })
})

function getBlocked() {
    console.log('getBlocked')
    const blockedButton = $('.switch-to-blocked').first()
    if (blockedButton.hasClass('active-background')) {
        return
    }
    call_endpoint(blockedPath, viewToBlocked)
}

function getLiked() {
    const likedButton = $('.switch-to-liked').first()
    if (likedButton.hasClass('active-background')) {
        return
    }
    call_endpoint(likedPath, viewToLiked)
}

function viewToBlocked(data) {
    if (data.length == 0) {
        return
    }
    var youLeftCol = $('.you-left-col').first()
    youLeftCol.children().not('.save, .save *').remove();
    youLeftCol.append(data)
    const likedButton = $('.switch-to-liked').first()
    const blockedButton = $('.switch-to-blocked').first()
    blockedButton.addClass('active-background')
    likedButton.removeClass('active-background')
}

function viewToLiked(data) {
    if (data.length == 0) {
        return
    }
    var youLeftCol = $('.you-left-col').first()
    youLeftCol.children().not('.save, .save *').remove();
    youLeftCol.append(data)
    const likedButton = $('.switch-to-liked').first()
    const blockedButton = $('.switch-to-blocked').first()
    likedButton.addClass('active-background')
    blockedButton.removeClass('active-background')

}


function call_endpoint(endpoint, on_success){
    fetch(endpoint, {
        method: "GET",
    })
    .then( response => response.json())
    .then(data => {
        console.log(data)
        on_success(data.html)
    })
    .catch(error => console.error('Error:', error));
}
