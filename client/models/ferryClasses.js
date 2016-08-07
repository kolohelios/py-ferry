'use strict';

angular.module('py-ferry')
.factory('FerryClass', ['$http', '$window', '$q', 'apiUrl', '_', function($http, $window, $q, apiUrl, _) {
  function FerryClass() {}
  
  FerryClass.ferryClasses = [];

  FerryClass.list = function() {
    var d = $q.defer();
    var self = this;
    if(this.ferryClasses.length) {
        d.resolve(this.ferryClasses);
    } else {
        $http({
          method: 'GET',
          url: apiUrl + '/ferry_classes'
        })
        .then(function(response) {
            self.ferryClasses = response.data;
            d.resolve(self.ferryClasses);
        })
        .catch(function(error) {
            d.reject(error);
        });
    }
    return d.promise;
  };

  return FerryClass;
}]);
