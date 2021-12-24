
function showBrightness() {
  let range = document.getElementById("range");
  let span = document.getElementById("cur-brightness");
  span.innerText = range.value;
  if (done) {
    changeBrightness();
  }
}

let done = true;
function changeBrightness() {
  done = false;
  $.post('/admin/brightness/send/', $('.form').serialize(), function () {
    done = true;
  });
}
