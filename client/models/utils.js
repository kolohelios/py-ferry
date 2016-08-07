'use strict';

angular.module('py-ferry')
.factory('Utils', ['$http', '$window', '$q', 'apiUrl', '_', 'User', function($http, $window, $q, apiUrl, _, User) {
  function Utils() {}

  Utils.userLoggedIn = function() {
    if(User.user.id && User.user.id > 0) {
        return true;
    } else if(!User.checkedLocalStorage) {
      User.checkedLocalStorage = true;
      User.checkTokenFromLocalStorage()
      .then(function(response) {
        console.log(response);
      })
      .catch(function(error) {
        console.error(error);
      });
    }
  };
  
  return Utils;
}]);
