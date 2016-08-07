'use strict';

angular.module('py-ferry')
.factory('Game', ['$http', '$window', '$q', 'apiUrl', '_', function($http, $window, $q, apiUrl, _) {
  function Game() {}
  
  Game.games = [];

  Game.list = function() {
    var self = this;
    var d = $q.defer();
    $http({
      method: 'GET',
      url: apiUrl + '/games'
    })
    .then(function(response) {
        self.games = response.data;
        d.resolve(response);
    })
    .catch(function(error) {
        d.reject(error);
    });
    return d.promise;
  };
  
  Game.createGame = function() {
    var self = this;
    $http({
        method: 'POST',
        url: apiUrl + '/games'
    })
    .then(function(response) {
        self.games.push(response.data);
        return true;
    })
    .catch(function() {
        return Error;
    });
  };

  return Game;
}]);
