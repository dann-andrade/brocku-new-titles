(function () {

	'use strict';

	angular
		.module('newTitles', [])
		.controller('MainController',
			function ($http, $scope) {

				const $ctrl = this;
				var scrollCont = document.getElementById('bu-outer-carousel');
				var innerCar = document.getElementById('bu-inner-carousel');

				// Set scroll position to zero on component initilalization
				scrollCont.scrollLeft = 0;

				var loadCursor = 0;
				var dispCursor = 0;
				var screenWidth = 0;
				var scrollWidth = 0;
				
				var mouseDown = false;
				var startX = 0;
				var endX = 0;

				$ctrl.newbooks = [];
				$ctrl.display = [];
				$ctrl.dataLoaded = false;
				$ctrl.showDisplay = true;

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
					screenWidth = document.body.offsetWidth;
					scrollWidth = (screenWidth > 500) ? 500 : screenWidth;
					$ctrl.showDisplay = (screenWidth >= 700) ? true : false;
				};

				// Adds space to inner carousel container to make room for new items
				function setWidth(w) {
					innerCar.style.width = String(innerCar.offsetWidth + w) + "px";
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
							setWidth(1000);
						}, 0);
					};
					scrollCont.scrollLeft += scrollWidth;
				};

				$ctrl.viewAll = function() {
					window.location.href = 'https://ocul-bu.primo.exlibrisgroup.com/discovery/search?query=any,contains,%3F%3F&tab=New_Titles&search_scope=New_Books&vid=01OCUL_BU:BU_DEFAULT&lang=en&offset=0';
				}

				$ctrl.toStart = function() {
					scrollCont.scrollLeft = 0;
				}

				//Screen Resize Event
      	//Calls the find width function to update the width
				addEventListener('resize', (Event) => {
					findWidth();
					$scope.$apply();
				});

			});
})();
