(function () {

	'use strict';

	angular
		.module('newTitles', [])
		.controller('MainController',
			function ($http) {

				const $ctrl = this;
				const scrollCont = document.getElementById('bu-outer-carousel');
				const innerCar = document.getElementById('bu-inner-carousel');

				// Set scroll position to zero on component initilalization
				scrollCont.scrollLeft = 0;

				var loadCursor = 0;
				var dispCursor = 0;
				var screenWidth = 0;
				var scrollWidth = 0;

				$ctrl.newbooks = [];
				$ctrl.display = [];
				$ctrl.dataLoaded = false;

				// Retrieve daily data, load 20 books and calculate width
				$http.get('http://rtod.library.brocku.ca:8080/data/gtitles.json').then(
					function success(response) {
						$ctrl.newbooks = response.data;
						$ctrl.dataLoaded = true;
						loadBooks(19);
						findWidth();
					},
					function error(response) {
						console.log(response);
					});

				// Load n books from full array into display array, infinitely
				function loadBooks(n) {
					let i = 1;
					while (i <= n && loadCursor < $ctrl.newbooks.length) {
						$ctrl.display[dispCursor] = $ctrl.newbooks[loadCursor]
						i++;
						loadCursor++;
						dispCursor++;
						if (loadCursor == $ctrl.newbooks.length) {
							loadCursor = 0;
						};
					};
				};

				// Retrieve viewport width, dynamically sets scroll distance
				function findWidth() {
					screenWidth = scrollCont.offsetWidth;
					scrollWidth = (screenWidth > 500) ? 500 : screenWidth;
				};

				// Adds space to inner carousel container to make room for new items
				function setWidth() {
					innerCar.style.width = String(innerCar.offsetWidth + 1000) + "px";
				};

				// Scrolls left
				$ctrl.scrollLeft = function () {
					scrollCont.scrollLeft -= scrollWidth;
				};

				// Scrolls left, extends if near the end of loaded covers
				$ctrl.scrollRight = function () {
					if (scrollCont.scrollLeft + screenWidth >= innerCar.offsetWidth - 1000) {
						loadBooks(8);
						setTimeout(() => {
							setWidth();
						}, 0);
					};
					scrollCont.scrollLeft += scrollWidth;
				};

				//Screen Resize Event
      	//Calls the find width function to update the width
				addEventListener('resize', (Event) => {
					findWidth();
				});

			});

})();
