function moveToNextInput(currentInput) {
    // Move focus to the next input
    var nextInput = currentInput.nextElementSibling;
    if (nextInput && currentInput.value !== '') {
      nextInput.focus();
    }
  }
  function moveToPreviousInput(event, currentInput) {
    if (event.key === 'ArrowLeft' && currentInput.selectionStart === 0) {
      var previousInput = currentInput.previousElementSibling;
      if (previousInput) {
        previousInput.focus();
      }
    }
  }

  document.addEventListener("DOMContentLoaded", function() {
    let currentImageIndex = 0;
    const images = document.querySelectorAll(".fade-in-out");

    function showNextImage() {
      const currentImage = images[currentImageIndex];
      currentImage.style.opacity = 0; // fade out the current image

      currentImageIndex = (currentImageIndex + 1) % images.length;

      const nextImage = images[currentImageIndex];
      
      nextImage.style.opacity = 1; // fade in the next image

      setTimeout(showNextImage, 3000); // wait for 3 seconds and repeat
    }

    showNextImage(); // start the initial transition
  });