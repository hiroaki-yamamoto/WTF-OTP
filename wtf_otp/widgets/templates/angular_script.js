{% macro print_tmp() -%}
{% include('tags.html') -%}
{%- endmacro %}
(function() {
  "use strict";
  angular.module("OTP{{script_args.fieldid}}Directive", []).directive(
    "otpField{{script_args.fieldid}}", [
      function() {
        return {
          "restrict": "AC",
          "scope": {
            "ngModel": "="
          },
          "template": "{{ print_tmp()|replace('"', '\\"')|replace('\n', ' ') }}",
          "controller": "OTP{{script_args.fieldid}}Controller"
        }
      }
    ]
  ).controller(
    "OTP{{script_args.fieldid}}Controller", [
      "$scope",{% if qrcode.url %} "$element", "$http",{% endif %}
      function(scope{% if qrcode.url %}, element, http{% endif %}) {
        var m="ABCDEFGHIJKLMNOPQRSTUVWXYZ234567", i;
        scope.click{{ script_args.fieldid }} = function() {
          var v = [];
          for(i=0; i<16; i++) {
            v.push(m[Math.floor(Math.random() * 32)]);
          }
          scope.ngModel = v.join("");
          {% if qrcode.url -%}
          http.get("{{ qrcode.url }}?secret=" + scope.ngModel).then(
            function(data) {
              element.find("#otpauthQR{{input_args.id}}").html(data.data);
            }
          ).catch(function (data) {
            element.find("#otpauthQR{{input_args.id}}").text(
              "Error:" + angular.toJson(data)
            );
          });
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
