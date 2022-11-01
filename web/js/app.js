(function() {

  'use strict';

  angular
    .module('newTitles', [
      'ngRoute',
      'myControllers'
    ])
    .config(config);

  function config($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'mainController',
        controllerAs: '$ctrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  }


})();
