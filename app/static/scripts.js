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


document.addEventListener("DOMContentLoaded", function() {
    var slider = document.getElementById('range-slider');
    var leftValue = document.getElementById('left-value');
    var rightValue = document.getElementById('right-value');

    // Ustawienia suwaka
    noUiSlider.create(slider, {
        start: [-5, 5], // początkowe wartości dla lewej i prawej granicy
        connect: true,  // Łączenie suwaków
        range: {
            'min': -30,  // minimalna wartość
            'max': 30    // maksymalna wartość
        },
        step: 1,  // Krok zmiany
        format: {
            to: function (value) {
                return Math.round(value);  // Zaokrąglanie wartości
            },
            from: function (value) {
                return Number(value);
            }
        }
    });

    // Aktualizacja wartości na suwaku oraz w ukrytych inputach
    slider.noUiSlider.on('update', function(values, handle) {
        var lower = values[0]; // Lewa granica
        var upper = values[1]; // Prawa granica

        // Ustawienie wartości lewej granicy
        if (handle === 0) {
            leftValue.innerText = lower;  // Zaktualizuj wyświetlaną wartość
            // Ogranicz ruch lewego suwaka do zakresu [-50, 0]
            if (lower > 0) {
                slider.noUiSlider.set([0, upper]);
            }
        }

        // Ustawienie wartości prawej granicy
        if (handle === 1) {
            rightValue.innerText = upper; // Zaktualizuj wyświetlaną wartość
            // Ogranicz ruch prawego suwaka do zakresu [0, 50]
            if (upper < 0) {
                slider.noUiSlider.set([lower, 0]);
            }
        }

        // Ustawienie wartości w ukrytych inputach
        var lowerInput = document.getElementById('lower-difference');
        var upperInput = document.getElementById('upper-difference');
        if (lowerInput && upperInput) {
            lowerInput.value = lower;
            upperInput.value = upper;
        }
    });
});

