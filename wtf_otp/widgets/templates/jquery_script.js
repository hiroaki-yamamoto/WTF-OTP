(function(){
  "use strict";
  $("#{{button_args.id}}").on("click", function() {
    var m="ABCDEFGHIJKLMNOPQRSTUVWXYZ234567", v = [], i;
    for(i=0; i<16; i++) {
      v.push(m[Math.floor(Math.random() * 32)]);
    }
    v = v.join("");
    $("#{{input_args.id}}").val(v);
    {% if qrcode.url -%}
      $("#otpauthQR{{input_args.id}}").css({
        "content": "url(\"{{ qrcode.url }}?secret=" + v + "\")"
      });
    {%- endif %}
  });
})()
