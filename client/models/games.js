'use strict';

angular.module('py-ferry')
.factory('Game', ['$http', '$window', '$q', 'apiUrl', '_', function($http, $window, $q, apiUrl, _) {
  function Game() {}
  
  Game.games = [];

  Game.list = function() {
    var d = $q.defer();
    $http({
      method: 'GET',
      url: apiUrl + '/games'
    })
    .then(function(response) {
        d.resolve(response);
    })
    .catch(function(error) {
        d.reject(error);
    });
    return d.promise;
  };
  
  Game.createGame = function() {
    return $http({
        method: 'POST',
        url: apiUrl + '/games'
    });
  };

  return Game;
}]);
