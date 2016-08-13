'use strict';

angular.module('py-ferry')
.factory('Game', ['$http', '$window', '$q', 'apiUrl', '_', '$rootScope', function($http, $window, $q, apiUrl, _, $rootScope) {
  function Game() {}
  
  Game.games = [];
  Game.activeGame = {};
  Game.gameId = 0;
  
  $rootScope.$on('updateGame', function(event, gameId) {
    Game.activeGameId = gameId;
    Game.fetch(gameId);
  });

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
  
  Game.fetch = function(gameId) {
    var self = this;
    var d = $q.defer();
    $http({
      method: 'GET',
      url: apiUrl + '/games/' + gameId
    })
    .then(function(response) {
      self.activeGame = response.data;
      d.resolve(self.activeGame);
    })
    .catch(function(error) {
      d.reject(error);
    });
    return d.promise;
  };
  
  Game.getActiveGame = function() {
    return this.activeGame;
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
  
  Game.deleteGame = function(gameId) {
    var self = this;
    $http({
        method: 'DELETE',
        url: apiUrl + '/games/' + gameId
    })
    .then(function(response) {
        _.remove(self.games, {id: gameId});
        return true;
    })
    .catch(function() {
        return Error;
    });
  };
  
  Game.endTurn = function(gameId) {
    var self = this;
    var d = $q.defer();
    $http({
      method: 'GET',
      url: apiUrl + '/games/' + gameId + '/endturn'
    })
    .then(function(response) {
        self.activeGame = response.data;
        d.resolve(self.activeGame);
    })
    .catch(function(error) {
        d.reject(error);
    });
    return d.promise;
  };

  return Game;
}]);
