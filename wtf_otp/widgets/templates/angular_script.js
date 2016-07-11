{% macro print_tmp() -%}
{% include('tags.html') -%}
{%- endmacro %}
(function() {
  "use strict";
  angular.module("OTP{{script_args.fieldid}}Directive", []){%if qrcode.url -%}
  .factory("getQRCode", ["$http", function(http) {
    return function(element, model) {
      http.get("{{ qrcode.url }}?secret=" + model).then(function(data) {
        element.html(data.data);
      }).catch(function (data) {
        element.text("Error:" + angular.toJson(data));
      });
    }
  }])
  {%- endif -%}
  .directive(
    "otpField{{script_args.fieldid}}", [
      {% if qrcode.url %}"getQRCode", {% endif -%}
      function({% if qrcode.url %}getQRCode{% endif %}) {
        return {
          restrict: "AC",
          scope: {ngModel: "="},
          template: "{{ print_tmp()|replace('"', '\\"')|replace('\n', ' ') }}",
          {% if script_args.data -%}
          link: function(scope, tElem) {
            scope.ngModel = "{{ script_args.data }}";
            {% if qrcode.url -%}
            getQRCode(
              tElem.find("#otpauthQR{{input_args.id}}"), scope.ngModel
            );
            {%- endif %}
          },
          {%- endif %}
          controller: "OTP{{script_args.fieldid}}Controller"
        }
      }
    ]
  ).controller(
    "OTP{{script_args.fieldid}}Controller", [
      "$scope",{% if qrcode.url %} "$element", "getQRCode",{% endif %}
      function(scope{% if qrcode.url %}, element, getQRCode{% endif %}) {
        var m="ABCDEFGHIJKLMNOPQRSTUVWXYZ234567", i;
        scope.click{{ script_args.fieldid }} = function() {
          var v = [];
          for(i=0; i<16; i++) {
            v.push(m[Math.floor(Math.random() * 32)]);
          }
          scope.ngModel = v.join("");
          {% if qrcode.url -%}
          getQRCode(
            element.find("#otpauthQR{{input_args.id}}"), scope.ngModel
          );
          {%- endif %}
        };
      }
    ]
  );
  // I don't think this is effective; needs optimization.
  window.addEventListener("load", function() {
    angular.injector([
      "ng", "OTP{{script_args.fieldid}}Directive"
    ]).invoke([
      "$compile", "$document",
      function (compile, doc) {
        var element = angular.element(doc).find(
          "[data-otp-field{{script_args.fieldid}}]"
        ), scope = element.scope();
        scope.$apply(function () {
          compile(element)(scope);
        });
      }
    ]);
  }, false);
})()
