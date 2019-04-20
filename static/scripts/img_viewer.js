// Get the modal
var imgModal = document.getElementById('imgModal');

// Get the image and insert it inside the modal - use its "alt" text as a caption
var imgModalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
function onClick(element) {
    imgModal.style.display = "block";
    imgModalImg.src = element.src;
    captionText.innerHTML = element.alt;
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    imgModal.style.display = "none";
}