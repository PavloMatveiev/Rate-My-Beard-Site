document.addEventListener("DOMContentLoaded", function () {
    // Use event delegation so that the handler is applied to all "read-more-links"
    document.addEventListener("click", function (e) {
        // If you clicked on a link with the class read-more-link
        if (e.target && e.target.matches(".read-more-link")) {
            e.preventDefault();
            var link = e.target;
            var moreText = link.previousElementSibling; // assume this is a span with class "more-text"
            if (moreText.style.display === "none") {
                moreText.style.display = "inline";
                link.textContent = "less";
            } else {
                moreText.style.display = "none";
                link.textContent = "more";
            }
        }
    });
});