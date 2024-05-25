function addHandlers(count) {
  var minus = count.querySelector(".minus");
  var number = count.querySelector(".counter-value");
  var plus = count.querySelector(".plus");

  plus.addEventListener("click", function() {
    if (number.value == 10) {
        number.value = 10;
    } else {
        number.value++;
    }
  });

  minus.addEventListener("click", function() {
    if (number.value <= 1) {
        number.value = 1;
    } else {
        number.value--;
    }
  });
}

var counts = document.querySelectorAll(".counter");
counts.forEach(addHandlers);
 