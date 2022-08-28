setTimeout(function() {
    var col = document.getElementsByClassName("notification");
    if (col.length != 0) {
        col = col[0]
        col.style.transition = '1.5s';
        col.style.opacity = '0';
        col.style.visibility = 'hidden';
    }
  }, 2000)
