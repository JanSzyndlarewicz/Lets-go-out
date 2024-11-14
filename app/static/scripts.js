document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('.nav-link');
    const root = document.documentElement;
    const mainColor = getComputedStyle(root).getPropertyValue('--primary-color').trim();;

    // Retrieve the saved clicked link from localStorage
    const savedLink = window.location.href;

    links.forEach(link => {
        // If the link matches the saved one, apply the color
        if (link.href === savedLink) {
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
        });
    });
});
