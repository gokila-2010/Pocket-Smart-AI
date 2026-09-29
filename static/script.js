document.addEventListener("DOMContentLoaded", function () {

    const recommendation = document.querySelector(".recommendation");

    if (recommendation) {
        recommendation.style.whiteSpace = "pre-wrap";
        recommendation.style.lineHeight = "1.75";
    }


    const budgetInput = document.querySelector("#budget");

    if (budgetInput) {
        budgetInput.addEventListener("input", function () {
            if (Number(this.value) <= 0) {
                this.setCustomValidity("Budget must be greater than 0.");
            } else {
                this.setCustomValidity("");
            }
        });
    }


    const guestInput = document.querySelector("#guest_count");

    if (guestInput) {
        guestInput.addEventListener("input", function () {
            if (Number(this.value) <= 0) {
                this.setCustomValidity("Number of guests must be greater than 0.");
            } else {
                this.setCustomValidity("");
            }
        });
    }

});