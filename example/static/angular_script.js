/* global angular */
(function(ng) {
  "use strict";
  ng.module("OTPApp", [
  ]).config(["$httpProvider", function(http) {
    // This is needed so that the backend can recognize the request is XHR.
    http.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest";
    // XSS preventation.
    http.defaults.xsrfCookieName =
      http.defaults.xsrfHeaderName = "X-CSRFToken";
  }]).controller("OTPController", ["$scope", function(scope) {
    scope.model = {};
    scope.toJson = ng.toJson;
  }]).controller("OTPAuthController", [
    "$scope", "$http", function(scope, http) {
      scope.submit = function() {
        scope.toJson = ng.toJson;
        http.post("/auth", scope.model).then(function(data) {
          scope.result = data.data;
        }).catch(function(err) {
          scope.result = err.data;
        });
      };
    }
  ]);
})(angular);
