function loginUser() {
    // Example credentials
    const userToken = 'exampleToken123';
    
    // Store the token in local storage
    localStorage.setItem('userToken', userToken);
    
    // Redirect to the protected page
    window.location.href = 'protected.html';
}

function logoutUser() {
    // Remove the token from local storage
    localStorage.removeItem('userToken');
    
    // Redirect to the login page
    window.location.href = 'login.html';
}

// document.addEventListener('DOMContentLoaded', () => {
//     // Get the token from local storage
//     const userToken = localStorage.getItem('userToken');
//
//     // Check if the token exists
//     if (userToken) {
//         // User is logged in, show the protected content
//         console.log('User is logged in');
//     } else {
//         // User is not logged in, redirect to the login page
//         window.location.href = 'login.html';
//     }
// });