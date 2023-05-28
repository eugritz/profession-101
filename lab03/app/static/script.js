"use strict";
var selected = 0, previousSelected = 0;
var calculationLabelOriginalText;

function ready() {
  let figures = document.getElementsByClassName("figure");
  for (let i = 0; i < figures.length; i++) {
    figures[i].addEventListener("click", selectFigure);
  }

  let label = document.getElementById("calculator-label");
  calculationLabelOriginalText = label.innerText;
  if (calculationLabelOriginalText === undefined)
    calculationLabelOriginalText = "";

  setSelected(0);
}

function selectFigure(event) {
  let id = event.currentTarget.dataset.id;
  if (id) {
    setSelected(id);
  }
}

function setSelected(index) {
  let options = document.getElementsByClassName("figure__content");
  let calculators = document.getElementById("calculator-list");
  let label = document.getElementById("calculator-label");
  if (index >= options.length)
    return;

  options[index].classList.add("figure__content-selected");
  calculators.children[index].classList.remove("hidden");
  let names = options[index].getElementsByClassName("figure__content__name");
  if (names.length == 1)
    label.innerText = calculationLabelOriginalText + " «" + names[0].innerText + "»";
  selected = index;

  if (selected != previousSelected) {
    options[previousSelected].classList.remove("figure__content-selected");
    calculators.children[previousSelected].classList.add("hidden");
    previousSelected = selected;
  }
}

document.addEventListener("DOMContentLoaded", ready);
