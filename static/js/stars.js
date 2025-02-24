// Wait for the page to load
document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll("#star-rating .star");
    const ratingInput = document.querySelector("input[name='rating']");

    // Function to update the display of stars
    function updateStars(selectedValue) {
        stars.forEach(star => {
            const starValue = parseInt(star.getAttribute('data-value'));
            if (starValue <= selectedValue) {
                star.classList.remove('far'); // not filled
                star.classList.add('fas');    // filled
            } else {
                star.classList.remove('fas');
                star.classList.add('far');
            }
        });
    }

    // When clicking on a star
    stars.forEach(star => {
        star.addEventListener('click', function () {
            const selectedValue = parseInt(this.getAttribute('data-value'));
            ratingInput.value = selectedValue;
            updateStars(selectedValue);
        });
        // Add a hover handler to temporarily highlight
        star.addEventListener('mouseover', function () {
            const hoverValue = parseInt(this.getAttribute('data-value'));
            updateStars(hoverValue);
        });
    });

    // When the cursor leaves the star area, reset the display to the selected value
    document.getElementById('star-rating').addEventListener('mouseout', function () {
        const currentValue = parseInt(ratingInput.value) || 0;
        updateStars(currentValue);
    });
});