const interestsPath = $('#interests-path').data().path

var unselectedInterests = []
async function init() {
    unselectedInterests = await getInitUnselectedInterests()
    initButtons()
    updateInterestsInput()
}

async function getAllInterests() {
    const response = await fetch(interestsPath) 
    const data = await response.json()
    return data.interests
}

async function getInitUnselectedInterests() {
    // selectedInterests is a global variable
    let interests = await getAllInterests()
    interests = interests.filter(interest => !selectedInterests.some(selectedInterest => selectedInterest.id === interest.id))
    return interests
}

function makeButton(interest, unselected) {
    class_name = unselected ? 'interest-unselected-button' : 'interest-selected-button'
    const tag_html = `<a class="${class_name}">${interest.name}</a>`
    const tag = document.createElement('li')
    tag.id = interest.id
    tag.innerHTML = tag_html
    tag.addEventListener('click', () => {
        if (unselected && selectedInterests.length <= 4) {
            unselectedInterests = unselectedInterests.filter(i => i.id !== interest.id)
            selectedInterests = selectedInterests.concat(interest)
            removeButton(interest, true)
            makeButton(interest, false)
        } else {
            selectedInterests = selectedInterests.filter(i => i.id !== interest.id)
            unselectedInterests = unselectedInterests.concat(interest)
            removeButton(interest, false)
            makeButton(interest, true)
        }
        updateInterestsInput()
    })
    parent = document.querySelector(unselected ? '.to-be-chosen-interests' : '.chosen-interests')
    parent.appendChild(tag)
}

function removeButton(interest, unselected) {
    parent = document.querySelector(unselected ? '.to-be-chosen-interests' : '.chosen-interests')
    parent.removeChild(document.getElementById(interest.id))
}

function initButtons() {
    unselectedInterests.forEach(interest => makeButton(interest, true))
    selectedInterests.forEach(interest => makeButton(interest, false))
}

function updateInterestsInput() {
    const interestsInput = document.getElementById('interests')
    interestsInput.value = JSON.stringify(selectedInterests)
}