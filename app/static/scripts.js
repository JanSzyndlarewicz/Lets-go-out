// Change color of nav links when clicked
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('.nav-link');
    const root = document.documentElement;
    const mainColor = getComputedStyle(root).getPropertyValue('--primary-color').trim();;
    
    var redirectLink = null;
    if (localStorage.getItem('clickedLink') !== null) {
        redirectLink = localStorage.getItem('clickedLink');
        console.log(redirectLink)
    } else {
        links.forEach(link => {
            const baseUrl = `${window.location.protocol}//${window.location.host}`;
            const firstDirectory = window.location.pathname.split('/')[1]; // Get the first directory
            const fullPath = firstDirectory ? `${baseUrl}/${firstDirectory}` : baseUrl;
    
            if (link.href === fullPath) {
                redirectLink = fullPath;            
            }
        });
    }
    
    

    links.forEach(link => {
        // If the link matches the saved one, apply the color
        console.log(link.href, redirectLink);
        if (link.href === redirectLink) {
            link.style.color = mainColor;
        }

        link.addEventListener('click', function(event) {
            event.preventDefault();

            // Reset color for all links
            links.forEach(l => l.style.color = '');

            // Set color for clicked link
            this.style.color = mainColor;

            // Redirect to the link's href after the color change
            window.location.href = this.href;

            // Save the clicked link to localStorage
            localStorage.setItem('clickedLink', this.href);
        });
    });
});


// Change color of buttons set on click
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

            // Reset color for all links
            links.forEach(l => l.style.color = '');

            // Set color for clicked link
            this.style.backgroundColor = backgroundColor;

            // Redirect to the link's href after the color change
            window.location.href = this.href;
        });
    });
});