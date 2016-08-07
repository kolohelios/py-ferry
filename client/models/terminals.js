'use strict';

angular.module('py-ferry')
.factory('Terminal', ['$http', '$window', '$q', 'apiUrl', '_', function($http, $window, $q, apiUrl, _) {
  function Terminal() {}
  
  Terminal.terminals = [];

  Terminal.list = function() {
    var d = $q.defer();
    var self = this;
    if(this.terminals.length) {
        d.resolve(this.terminals);
    } else {
        $http({
          method: 'GET',
          url: apiUrl + '/terminals'
        })
        .then(function(response) {
            self.terminals = response.data;
            d.resolve(self.terminals);
        })
        .catch(function(error) {
            d.reject(error);
        });
    }
    return d.promise;
  };

  return Terminal;
}]);
