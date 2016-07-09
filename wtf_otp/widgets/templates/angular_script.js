(function() {
  "use strict";
  angular.module("{{ script_args.module }}").controller(
    "OTP{{script_args.fieldid}}Controller", [
      "$scope", "$element",
      function(scope, element) {
        var m="ABCDEFGHIJKLMNOPQRSTUVWXYZ234567", v = [], i;
        scope.click{{ script_args.fieldid }} = function() {
          for(i=0; i<16; i++) {
            v.push(m[Math.floor(Math.random() * 32)]);
          }
          scope.{{ script_args.ng_model }} = v.join("");
          {% if qrcode.url -%}
            scope.qrcode = {'url': "{{ qrcode.url }}?secret=" + v};
          {%- endif %}
        };
      }
    ]
  );
})()
