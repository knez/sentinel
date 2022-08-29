// Get the modal
var modal;

function activateModal(id) {
  modal = document.getElementById(id);
  modal.style.display = "block";
}

// Get the <span> element that closes the modal
var spanList = document.getElementsByClassName("close");
// When the user clicks on <span> (x), close the modal
for (var i = 0; i < spanList.length; i++ ) {
  spanList[i].onclick = function () {
    modal.style.display = "none";
  };
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};
