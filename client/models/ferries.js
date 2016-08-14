'use strict';

angular.module('py-ferry')
.factory('Ferry', ['$http', '$window', '$q', 'apiUrl', '_', '$rootScope', function($http, $window, $q, apiUrl, _, $rootScope) {
  function Ferry() {}
  
  Ferry.buy = function(gameId, data) {
    var self = this;
    var d = $q.defer();
    $http({
      method: 'POST',
      url: apiUrl + '/games/' + gameId + '/ferries',
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
  
  Ferry.sell = function(gameId, ferryId) {
    var self = this;
    var d = $q.defer();
    $http({
      method: 'DELETE',
      url: apiUrl + '/games/' + gameId + '/ferries/' + ferryId
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
  
  Ferry.list = function(gameId) {
    var d = $q.defer();
      $http({
        method: 'GET',
        url: apiUrl + '/games/' + gameId + '/ferries'
      })
      .then(function(response) {
          d.resolve(response.data);
      })
      .catch(function(error) {
          d.reject(error);
      });
      return d.promise;
    }

  return Ferry;
}]);
