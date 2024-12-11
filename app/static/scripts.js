
function initIfNav() {
    const nav = document.querySelector('.nav');
    if (nav) {
        const navLinks = nav.querySelectorAll('.nav-link');
        const currentUrl = window.location.href;

        navLinks.forEach(link => {
            if (link.href === currentUrl) {
                link.classList.add('active');
            }
        });
    }
}


function getOnlyFirstDirIn(url=null) {
    url = url || window.location.href;
    const baseUrl = `${window.location.protocol}//${window.location.host}`;
    const firstDirectory = url.split('/')[3]; 
    const fullPath = firstDirectory ? `${baseUrl}/${firstDirectory}` : baseUrl;
    return fullPath;
}

$(document).ready(function() {
    const currentPage = window.location.href;

    const activeNavHref = sessionStorage.getItem('activeNav');

    $(".nav-link").on("click", function() {
        $(".nav-link").each(function() {
            $(this).removeClass('active');
        });

        $(this).addClass('active');

        // sessionStorage.setItem('activeNav', this.href);

        window.location.href = this.href;
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('.redirect-buttons-set-button');
    const root = document.documentElement;
    const backgroundColor = getComputedStyle(root).getPropertyValue('--primary-color').trim();;

    // Retrieve the saved clicked link from localStorage
    const savedLink = window.location.href;

    links.forEach(link => {
        // If the link matches the saved one, apply the color
        if (link.href === savedLink) {
            link.style.backgroundColor = backgroundColor;
        }

        link.addEventListener('click', function(event) {
            event.preventDefault();

            window.location.href = this.href;
        });
    });
});

function throwErrors(errors){
    alert(errors)
}

