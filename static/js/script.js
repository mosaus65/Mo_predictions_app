document.addEventListener("DOMContentLoaded", function () {

    console.log("Mo Predictions is running!");

    // Welcome message
    console.log("Welcome to Mo Predictions");

    // Explore Matches button
    const exploreButton = document.querySelector(".btn");

    exploreButton.addEventListener("click", function () {
        alert("Welcome! Football fixtures are coming soon.");
    });

    // Automatically update footer year
    const footer = document.querySelector("footer p");

    footer.innerHTML = `&copy; ${new Date().getFullYear()} Mo Predictions. All rights reserved.`;

});
