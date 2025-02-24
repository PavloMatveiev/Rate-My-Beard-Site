// When the user scrolls the page - show the button if the page is scrolled more than 200px
window.onscroll = function () {
    let btn = document.getElementById('back-to-top');
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        btn.style.display = "block";
    } else {
        btn.style.display = "none";
    }
};

// When clicked, smoothly scroll the page to the top
document.getElementById('back-to-top').addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});