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
            if (lower > 0){
              lowerInput.value = 0  
            }
            else{
                lowerInput.value = Math.abs(lower);
            }
            
            if (upper < 0){
                upperInput.value = 0  
            }
            else{
                upperInput.value = upper;
            }
            
        }
    });
});
