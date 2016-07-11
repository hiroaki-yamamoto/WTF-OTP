/* global angular */
(function(ng) {
  "use strict";
  ng.module("OTPApp", [
  ]).controller("OTPController", ["$scope", function(scope) {
    scope.model = {};
    scope.$watch("model", function(data) {
      console.log(data);
    }, true);
  }]);
})(angular);
