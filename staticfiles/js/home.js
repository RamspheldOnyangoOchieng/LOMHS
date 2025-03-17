// Toggle mobile navigation menu
document.getElementById('mobile-nav-toggle').addEventListener('click', function() {
    var menu = document.getElementById('mobile-nav-menu');
    menu.style.display = menu.style.display === "block" ? "none" : "block"; // Toggle between block and none
});
