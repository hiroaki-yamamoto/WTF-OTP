/* global angular */
(function(ng) {
  "use strict";
  ng.module("OTPApp", [
  ]).controller("OTPController", ["$scope", function(scope) {
    scope.model = {};
    scope.toJson = ng.toJson;
  }]).controller("OTPAuthController", [function() {
    return undefined;
  }]);
})(angular);
