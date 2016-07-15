(function(){
  "use strict";
  {% if qrcode.url -%}
  var generateQRCode = function(secret) {
    $.ajax("{{ qrcode.url }}", {
      data: {secret: secret},
      dataType: "text"
    }).done(function(data) {
      $("#otpauthQR{{input_args.id}}").html(data);
    });
  };
  {%- endif %}
  window.addEventListener("load", function() {
    $("#{{button_args.id}}").on("click", function() {
      var m="ABCDEFGHIJKLMNOPQRSTUVWXYZ234567", v = [], i;
      for(i=0; i<16; i++) {1
        v.push(m[Math.floor(Math.random() * 32)]);
      }
      v = v.join("");
      $("#{{input_args.id}}").val(v);
      {% if qrcode.url -%}
        generateQRCode(v);
      {%- endif %}
    });
    {% if qrcode.url and input_args.value -%}
    generateQRCode("{{ input_args.value }}")
    {%- endif %}
  });
})()
