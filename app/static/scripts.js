// ON EVERY PAGE INIT
initIfNav();

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
    const firstDirectory = url.split('/')[3]; // Get the first directory
    const fullPath = firstDirectory ? `${baseUrl}/${firstDirectory}` : baseUrl;
    return fullPath;
}

$(document).ready(function() {
    const currentPage = window.location.href;

    const activeNavHref = sessionStorage.getItem('activeNav');

    if (activeNavHref) {
        if (getOnlyFirstDirIn(currentPage) === getOnlyFirstDirIn(activeNavHref)) {
            $(".nav-link").each(function() {
                if (this.href === activeNavHref) {
                    $(this).addClass('active');
                }
            });
        } else {
            sessionStorage.removeItem('activeNav');
        }
    } else {
        $(".nav-link").each(function() {
            if (getOnlyFirstDirIn(this.href) === getOnlyFirstDirIn(currentPage)) {
                $(this).addClass('active');
            }
        });
    }

    $(".nav-link").on("click", function() {
        // $(".nav-link").each(function() {
        //     $(this).removeClass('active');
        // });

        // $(this).addClass('active');

        sessionStorage.setItem('activeNav', this.href);

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

            // // Reset color for all links
            // links.forEach(l => l.style.backgroundColor = '');

            // // Set color for clicked link
            // this.style.backgroundColor = backgroundColor;

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

    // Get initial values from the hidden input fields and ensure they are numbers
    const initialLower = parseInt(document.getElementById('lower-difference').value) || 0;
    const initialUpper = parseInt(document.getElementById('upper-difference').value) || 0;

    // Initialize the slider with the correct values
    noUiSlider.create(slider, {
        start: [-1*initialLower, initialUpper], // Use initialLower and initialUpper directly
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

