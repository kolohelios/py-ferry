'use strict';

angular.module('py-ferry')
.controller('GamesCtrl', ['$scope', '$state', 'Game', function($scope, $state, Game) {
    
    Game.list()
    .then(function(response) {
        $scope.games = response;
        console.log(response);
    })
    .catch(function(error){
        console.error(error);
    });
    
    $scope.createGame = function() {
      Game.createGame();  
    };
}]);