// ANIMACIÓN DE ELEMENTOS AL HACER SCROLL

const elementsToAnimate = document.querySelectorAll(
    ".feature-card, .cta-section, .welcome-card"
);


const observer = new IntersectionObserver(

    (entries) => {

        entries.forEach((entry) => {

            if (entry.isIntersecting) {

                entry.target.classList.add("show");

            }

        });

    },

    {

        threshold: 0.2

    }

);


elementsToAnimate.forEach((element) => {

    element.classList.add("hidden");

    observer.observe(element);

});


// EFECTO DE ESCRITURA

const textElement = document.querySelector(".welcome-text");

const originalText = textElement.textContent;

let characterIndex = 0;


textElement.textContent = "";


function typeWriter() {

    if (characterIndex < originalText.length) {

        textElement.textContent += originalText.charAt(characterIndex);

        characterIndex++;

        setTimeout(typeWriter, 50);

    }

}


typeWriter();



// BOTÓN "COMENZAR AHORA"


const primaryButton = document.querySelector(".btn-primary");


primaryButton.addEventListener("click", (event) => {

    event.preventDefault();

    alert("🚀 ¡Bienvenido! Tu experiencia comienza ahora.");

});



// BOTÓN CTA


const ctaButton = document.querySelector(".btn-cta");


ctaButton.addEventListener("click", (event) => {

    event.preventDefault();

    alert("✨ ¡Excelente decisión! Gracias por comenzar.");

});



// ANIMACIÓN DE LA TARJETA PRINCIPAL


const welcomeCard = document.querySelector(".welcome-card");


let movement = 0;

let direction = 1;


function floatingAnimation() {

    movement += 0.03 * direction;


    if (movement > 1) {

        direction = -1;

    }


    if (movement < -1) {

        direction = 1;

    }


    welcomeCard.style.transform = `translateY(${movement * 5}px)`;


    requestAnimationFrame(floatingAnimation);

}


floatingAnimation();


// BOTÓN VOLVER ARRIBA

const backToTop = document.createElement("button");


backToTop.innerHTML = '<i class="fa-solid fa-arrow-up"></i>';


backToTop.classList.add("back-to-top");


document.body.appendChild(backToTop);


window.addEventListener("scroll", () => {

    if (window.scrollY > 400) {

        backToTop.classList.add("active");

    } else {

        backToTop.classList.remove("active");

    }

});


backToTop.addEventListener("click", () => {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

});