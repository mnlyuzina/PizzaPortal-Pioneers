function addHandlers(count) {
  var minus = count.querySelector(".minus");
  var number = count.querySelector(".counter-value");
  var plus = count.querySelector(".plus");
  plus.addEventListener("click", function() {
    if (number.innerText == 10) {
        number.innerText = 10;
    } else {
        number.innerText++;
    }
  });
  minus.addEventListener("click", function() {
    if (number.innerText <= 1) {
        number.innerText = 1;
    } else {
        number.innerText--;
    }
  });
}

var counts = document.querySelectorAll(".counter");
counts.forEach(addHandlers);
 