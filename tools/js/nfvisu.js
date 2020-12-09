var ETag = ""

function refreshIndexHTML() {
  $.ajax({
    type: "HEAD",
    async: true,
    url: 'http://192.168.3.251',
    success: function(message, text, response) {
      lastETag = response.getResponseHeader("ETag");
      if(ETag.length == 0) {
        ETag = lastETag;
      } else if(ETag != lastETag) {
        document.location.reload();
      }
    }
  });
}
