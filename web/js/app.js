(function () {

	'use strict';

	angular
		.module('newTitles', [])
		.controller('MainController',
			function ($http) {

				const $ctrl = this;
				const scrollCont = document.getElementById('bu-outer-carousel');
				const innerCar = document.getElementById('bu-inner-carousel');

				scrollCont.scrollLeft = 0;

				var loadCursor = 0;
				var dispCursor = 0;
				var screenWidth = 0;

				$ctrl.newbooks = [];
				$ctrl.display = [];
				$ctrl.dataLoaded = false;

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


				function loadBooks(n) {

					let i = 1;

					while (i <= n && loadCursor < $ctrl.newbooks.length) {
						$ctrl.display[dispCursor] = $ctrl.newbooks[loadCursor]
						i++;
						loadCursor++;
						dispCursor++;

						if (loadCursor == $ctrl.newbooks.length) {
							loadCursor = 0;
						}

					}

				}

				function findWidth() {
					screenWidth = scrollCont.offsetWidth;
				}

				function setWidth() {
					innerCar.style.width = String(innerCar.offsetWidth + 1000) + "px";
				}

				$ctrl.scrollLeft = function () {
					scrollCont.scrollLeft -= 500;
				};

				$ctrl.scrollRight = function () {
					
					if (scrollCont.scrollLeft + screenWidth >= innerCar.offsetWidth - 1000) {

						loadBooks(8);

						setTimeout(() => {
							setWidth();
						}, 0);

					};

					scrollCont.scrollLeft += 500;

				};

				addEventListener('resize', (Event) => {
					findWidth();
				});

			});

})();
