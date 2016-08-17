'use strict';

angular.module('py-ferry')
.factory('Route', ['$http', '$window', '$q', 'apiUrl', '_', '$rootScope', function($http, $window, $q, apiUrl, _, $rootScope) {
  function Route() {}
  
    Route.create = function(gameId, data) {
        var d = $q.defer();
        $http({
          method: 'POST',
          url: apiUrl + '/games/' + gameId + '/routes',
          data: data
        })
        .then(function(response) {
            $rootScope.$emit('updateGame', gameId);
            d.resolve(response.data);
        })
        .catch(function(error) {
            d.reject(error);
        });
        return d.promise;
    };
  
    Route.list = function(gameId) {
        var d = $q.defer();
        $http({
          method: 'GET',
          url: apiUrl + '/games/' + gameId + '/routes'
        })
        .then(function(response) {
            d.resolve(response.data);
        })
        .catch(function(error) {
            d.reject(error);
        });
        return d.promise;
    }
    
    Route.save = function(gameId, data) {
        var d = $q.defer();
        var routeId = data.id;
        delete data.id;
        $http({
          method: 'PUT',
          url: apiUrl + '/games/' + gameId + '/routes/' + routeId,
          data: data
        })
        .then(function(response) {
            console.log(response.data);
            $rootScope.$emit('updateGame', gameId);
            d.resolve(response.data);
        })
        .catch(function(error) {
            d.reject(error);
        });
        return d.promise;
    }

  return Route;
}]);
