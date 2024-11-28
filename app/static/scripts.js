function getOnlyFirstDirIn(url=null) {
    url = url || window.location.href;
    const baseUrl = `${window.location.protocol}//${window.location.host}`;
    const firstDirectory = url.split('/')[3]; // Get the first directory
    const fullPath = firstDirectory ? `${baseUrl}/${firstDirectory}` : baseUrl;
    return fullPath;
}

// Change color of nav links when clicked
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('.nav-link');
    const root = document.documentElement;
    const mainColor = getComputedStyle(root).getPropertyValue('--primary-color').trim();;
    
    var redirectLink = null;
    if (sessionStorage.getItem('clickedLink') !== null) {
        redirectLink = sessionStorage.getItem('clickedLink');
    } else {
        const fullPath = getOnlyFirstDirIn();
        links.forEach(link => {   
            if (getOnlyFirstDirIn(link.href) === fullPath) {
                redirectLink = fullPath;            
            }
        });
    }

    links.forEach(link => {
        // If the link matches the saved one, apply the color
        console.log("check",link.href,"redirect", redirectLink ,1);
        if (getOnlyFirstDirIn(link.href) === redirectLink) {
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
            sessionStorage.setItem('clickedLink', this.href);
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

// Slider for the age range preferences
document.addEventListener("DOMContentLoaded", function() {
    const slider = document.getElementById('range-slider');
    const leftValue = document.getElementById('left-value');
    const rightValue = document.getElementById('right-value');

    const initialLower = document.getElementById('lower-difference').value;
    const initialUpper = document.getElementById('upper-difference').value;

    noUiSlider.create(slider, {
        start: [-1*initialLower, initialUpper],
        connect: true,
        range: {
            'min': -30,
            'max': 30
        },
        step: 1,
        format: {
            to: function (value) {
                return Math.round(value);
            },
            from: function (value) {
                return Number(value);
            }
        }
    });

    // Update the values on the slider
    slider.noUiSlider.on('update', function(values, handle) {
        const lower = values[0];
        const upper = values[1];

        if (handle === 0) {
            leftValue.innerText = lower;
            if (lower > 0) {
                slider.noUiSlider.set([0, upper]);
            }
        }

        if (handle === 1) {
            rightValue.innerText = upper;
            if (upper < 0) {
                slider.noUiSlider.set([lower, 0]);
            }
        }

        // Update the hidden input fields
        const lowerInput = document.getElementById('lower-difference');
        const upperInput = document.getElementById('upper-difference');

        if (lowerInput && upperInput) {
            lowerInput.value = Math.abs(lower);
            upperInput.value = upper;
        }
    });
});

