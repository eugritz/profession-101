"use strict";

var selected = 0, previousSelected = 0;
var calculationLabelOriginalText;

function ready() {
  const label = document.getElementById("calculator-label");
  calculationLabelOriginalText = label.innerText;
  if (calculationLabelOriginalText === undefined)
    calculationLabelOriginalText = "";

  const figures = document.getElementsByClassName("figure");
  for (let i = 0; i < figures.length; i++) {
    figures[i].addEventListener("click", selectFigure);
  }

  setupSliders();
  setSelectedFigure(0);
}

function setupSliders() {
  const slider = document.getElementsByClassName("slider");
  for (let i = 0; i < slider.length; i++) {
    const range = slider[i].querySelector('input[type="range"]');
    const label = slider[i].querySelector('.slider__value');
    const color = getComputedStyle(range).backgroundColor;

    if (range) {
      const update = (value) => {
        const progress = value / range.max * 100;
        if (label) {
          label.innerText = range.value;
        }
        range.style.background = `linear-gradient(to right,
            selecteditem ${progress}%, ${color} ${progress}%)`;
      };

      range.addEventListener("input", (event) => update(event.target.value));
      update(range.value);
    }
  }
}

function setSelectedFigure(index) {
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

function selectFigure(event) {
  let id = event.currentTarget.dataset.id;
  if (id) {
    setSelectedFigure(id);
  }
}

document.addEventListener("DOMContentLoaded", ready);
