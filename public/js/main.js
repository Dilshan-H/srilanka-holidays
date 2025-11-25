// ------------------------------
// |             NavBar         |
// ------------------------------

// add classes for mobile navigation toggling
var CSbody = document.querySelector("body");
const CSnavbarMenu = document.querySelector("#cs-navigation");
const CShamburgerMenu = document.querySelector("#cs-navigation .cs-toggle");

CShamburgerMenu.addEventListener("click", function () {
  CShamburgerMenu.classList.toggle("cs-active");
  CSnavbarMenu.classList.toggle("cs-active");
  CSbody.classList.toggle("cs-open");
  // run the function to check the aria-expanded value
  ariaExpanded();
});

// checks the value of aria expanded on the cs-ul and changes it accordingly whether it is expanded or not
function ariaExpanded() {
  const csUL = document.querySelector("#cs-expanded");
  const csExpanded = csUL.getAttribute("aria-expanded");

  if (csExpanded === "false") {
    csUL.setAttribute("aria-expanded", "true");
  } else {
    csUL.setAttribute("aria-expanded", "false");
  }
}

// mobile nav toggle code
const dropDowns = Array.from(
  document.querySelectorAll("#cs-navigation .cs-dropdown")
);
for (const item of dropDowns) {
  const onClick = () => {
    item.classList.toggle("cs-active");
  };
  item.addEventListener("click", onClick);
}

// ------------------------------
// |             Hero           |
// ------------------------------

// perspective image effect
const image = document.querySelector("#perspective-image");

image.addEventListener("mousemove", (e) => {
  const { width, height, left, top } = image.getBoundingClientRect();
  const mouseX = e.clientX - left; // X position of the mouse inside the image
  const mouseY = e.clientY - top; // Y position of the mouse inside the image

  const centerX = width / 2;
  const centerY = height / 2;

  // Calculate the mouse movement in percentage
  const percentX = (mouseX - centerX) / centerX;
  const percentY = (mouseY - centerY) / centerY;

  // Adjust the perspective effect based on mouse position
  const rotateX = percentY * 10; // Adjust the amount of tilt on the Y axis
  const rotateY = -percentX * 10; // Adjust the amount of tilt on the X axis

  image.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
});

image.addEventListener("mouseleave", () => {
  image.style.transform = `rotateX(0deg) rotateY(0deg)`; // Reset when the mouse leaves
});

// -------- Show meme content image on click --------

// Coordinates of the "three dots" area (this will be where the user clicks)
const dotArea = { x: 8, y: 8, width: 40, height: 40 }; // Customize based on where your three dots are located

image.addEventListener("click", (e) => {
  const mouseX = e.offsetX; // Mouse X position relative to the image
  const mouseY = e.offsetY; // Mouse Y position relative to the image

  console.log(`MouseX: ${mouseX}, MouseY: ${mouseY}`);
  // Check if the click happened within the three dots area
  if (
    mouseX >= dotArea.x &&
    mouseX <= dotArea.x + dotArea.width &&
    mouseY >= dotArea.y &&
    mouseY <= dotArea.y + dotArea.height
  ) {
    console.log("User clicked the sensitive area");
    const contentImage = document.getElementById("content-image");

    image.style.display = "none";
    contentImage.style.display = "block";
  }
});

// ------------------------------
// |        FAQ Section         |
// ------------------------------
const faqItems = Array.from(document.querySelectorAll(".cs-faq-item"));
for (const item of faqItems) {
  const onClick = () => {
    const wasActive = item.classList.contains("active");

    // Collapse all items first
    faqItems.forEach((i) => i.classList.remove("active"));

    // If the clicked item wasn't active before, activate it
    if (!wasActive) {
      item.classList.add("active");
    }
  };
  item.addEventListener("click", onClick);
}
