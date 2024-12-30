// Smooth Scroll Functionality for CTA Buttons
document.querySelectorAll('.cta-btn').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1); // Get target section ID
        const targetElement = document.getElementById(targetId);

        window.scrollTo({
            top: targetElement.offsetTop,
            behavior: 'smooth'
        });
    });
});

// Toggle Mobile Navigation (Example for Mobile Menu if you add a nav bar)
document.getElementById('mobile-nav-toggle').addEventListener('click', () => {
    const mobileNav = document.getElementById('mobile-nav');
    mobileNav.classList.toggle('active');
});
// Mobile Navigation Toggle
document.addEventListener("DOMContentLoaded", function () {
    const mobileNavToggle = document.getElementById("mobile-nav-toggle");
    const desktopNav = document.querySelector(".desktop-nav");

    mobileNavToggle.addEventListener("click", () => {
        if (desktopNav.style.display === "block") {
            desktopNav.style.display = "none";
        } else {
            desktopNav.style.display = "block";
        }
    });
});
