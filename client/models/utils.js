'use strict';

angular.module('py-ferry')
.factory('Utils', ['$http', '$window', '$q', 'apiUrl', '_', 'User', function($http, $window, $q, apiUrl, _, User) {
  function Utils() {}

  Utils.userLoggedIn = function() {
    if(User.user.id && User.user.id > 0) {
        return true;
    }
    return false;
  };
  
  return Utils;
}]);
