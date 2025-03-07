/**
 * LabEase Logout Functionality
 * Handles user logout process and token removal
 */

document.addEventListener('DOMContentLoaded', function() {
    // Find all logout buttons in the application
    const logoutButtons = document.querySelectorAll('.nav-item.logout');
    
    // Add click event listener to each logout button
    logoutButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Prevent the default link behavior
            e.preventDefault();
            
            // Clear all authentication data from localStorage
            localStorage.removeItem('labease_auth_token');
            localStorage.removeItem('labease_user_data');
            
            // Force redirect to login page
            window.location.replace('login_page.html');
        });
    });
});
