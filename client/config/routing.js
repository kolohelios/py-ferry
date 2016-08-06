'use strict';

angular.module('py-ferry')
.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise('/');

  $stateProvider
  .state('home', {url: '/', templateUrl: 'views/home/home.html', controller: 'HomeCtrl'})
  .state('login', {url: '/login', templateUrl: 'views/user/user-login.html', controller: 'UserCtrl'})
  .state('games', {url: '/games', templateUrl: 'views/games/games.html', controller: 'GamesCtrl'})
  .state('register', {url: '/register', templateUrl: 'views/user/user-register.html', controller: 'UserCtrl'});
  
  ;
}])
.config(['$locationProvider', function($locationProvider) {
  $locationProvider.html5Mode(true);
  $locationProvider.hashPrefix('!');
}]);
