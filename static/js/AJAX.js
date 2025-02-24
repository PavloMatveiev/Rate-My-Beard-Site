// Global flags to control simultaneous AJAX requests
let postsAjaxLoading = false;
let commentsAjaxLoading = false;

/**
* Function for binding click handlers to post sorting links.
* When clicked, an AJAX request is sent, updating the post list and URL.
*/
function bindPostsSortLinks() {
    const sortLinks = document.querySelectorAll('.sort-posts-link');
    sortLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            // If an AJAX request for posts is already running, stop executing
            if (postsAjaxLoading) return;
            postsAjaxLoading = true;

            // Save the current scroll position
            const currentScrollY = window.scrollY;

            // Form a full URL without hash
            let url = new URL(this.href, window.location.origin);
            url.hash = '';

            // Send an AJAX request with a header so the server knows it's AJAX
            fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok.');
                    return response.text();
                })
                .then(html => {
                    // Update the contents of the post container with the new HTML
                    document.getElementById('posts').innerHTML = html;
                    // Update URL in address bar without reloading page
                    window.history.pushState(null, '', url);
                    // Restore the scroll position
                    window.scrollTo(0, currentScrollY);
                    postsAjaxLoading = false;
                    // Rebind handlers to newly loaded sorting and pagination links
                    bindPostsPaginationLinks();
                    bindPostsSortLinks();
                })
                .catch(error => {
                    console.error('Error in AJAX post sorting:', error);
                    postsAjaxLoading = false;
                });
        });
    });
}

/**
* Function for binding click handlers to comment sorting links.
* When clicked, an AJAX request is sent, updating the comment list and URL.
*/
function bindCommentsSortLinks() {
    const sortLinks = document.querySelectorAll('.sort-comments-link');
    sortLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            if (commentsAjaxLoading) return;
            commentsAjaxLoading = true;

            const currentScrollY = window.scrollY;
            let url = new URL(this.href, window.location.origin);
            url.hash = '';

            fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok.');
                    return response.text();
                })
                .then(html => {
                    document.getElementById('comments-container').innerHTML = html;
                    window.history.pushState(null, '', url);
                    window.scrollTo(0, currentScrollY);
                    commentsAjaxLoading = false;
                    bindCommentsPaginationLinks();
                    bindCommentsSortLinks();
                })
                .catch(error => {
                    console.error('Error in AJAX comment sorting:', error);
                    commentsAjaxLoading = false;
                });
        });
    });
}

/**
* Function for binding click handlers to post pagination links.
* When clicked, an AJAX request is sent, updating the post list and URL.
*/
function bindPostsPaginationLinks() {
    const postsPaginationLinks = document.querySelectorAll('#posts a.page-link');
    postsPaginationLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            if (postsAjaxLoading) return;
            postsAjaxLoading = true;

            const currentScrollY = window.scrollY;
            let url = new URL(this.href, window.location.origin);
            url.hash = '';

            fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok.');
                    return response.text();
                })
                .then(html => {
                    document.getElementById('posts').innerHTML = html;
                    window.history.pushState(null, '', url);
                    window.scrollTo(0, currentScrollY);
                    postsAjaxLoading = false;
                    bindPostsPaginationLinks();
                })
                .catch(error => {
                    console.error('Error in AJAX posts pagination:', error);
                    postsAjaxLoading = false;
                });
        });
    });
}

/**
* Function for binding click handlers to comment pagination links.
* When clicked, an AJAX request is sent, updating the comment list and URL.
*/
function bindCommentsPaginationLinks() {
    const commentsPaginationLinks = document.querySelectorAll('#comments-container a.page-link');
    commentsPaginationLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            if (commentsAjaxLoading) return;
            commentsAjaxLoading = true;

            const currentScrollY = window.scrollY;
            let url = new URL(this.href, window.location.origin);
            url.hash = '';

            fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok.');
                    return response.text();
                })
                .then(html => {
                    document.getElementById('comments-container').innerHTML = html;
                    window.history.pushState(null, '', url);
                    window.scrollTo(0, currentScrollY);
                    commentsAjaxLoading = false;
                    bindCommentsPaginationLinks();
                })
                .catch(error => {
                    console.error('Error in AJAX comments pagination:', error);
                    commentsAjaxLoading = false;
                });
        });
    });
}

/**
* Function for adding comments.
* When clicked, an AJAX request is sent, updating the comment list.
*/
document.addEventListener('DOMContentLoaded', function () {
    // Find the comment form
    const commentForm = document.getElementById('comment-form');
    if (commentForm) {
        commentForm.addEventListener('submit', function (e) {
            e.preventDefault(); // Preventing standard form submission
            const formData = new FormData(this);

            // Sending an AJAX request via fetch
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'  // Be sure to add this title
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(html => {
                    // Updating the contents of the comment container
                    document.getElementById('comments-container').innerHTML = html;
                    // Reset the form (if necessary)
                    commentForm.reset();
                })
                .catch(error => {
                    console.error('Error posting comment:', error);
                });
        });
    }
});

// Bind all handlers after DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    bindPostsPaginationLinks();
    bindPostsSortLinks();
    bindCommentsPaginationLinks();
    bindCommentsSortLinks();
});