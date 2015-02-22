(function() {

  var showModal = function(element, action, label) {
    $("#modal-content").empty().append(element);
    $("#modal-submit").text(label);
    $("#modal-submit").attr("data-modal-action", action);
    $("#oscarslam-modal").modal("show");
  };

  var retrySocket = function(uri) {
    window.setTimeout(function() { setupSocket(uri); }, 5000);
  };

  var setupSocket = function(socket_uri) {
    console.log("Connecting to socket " + socket_uri);

    var newSocket = new window.WebSocket(socket_uri);
    newSocket.onopen = function() {
      console.log("Connected to socket.");
    };

    newSocket.onclose = function() {
      retrySocket(socket_uri);
    };

    newSocket.onmessage = function() {
      //var data = window.JSON.parse(e.data);
      showModal(
          $("<p><b>Update:</b> a winner has been awarded. Refresh the page to see how you did!<p>"),
          "refresh", "Refresh");
    };

    newSocket.onerror = function() {
      console.log("Error connecting to websocket.");
    };
  };

  $(document).on("click", "[data-modal-action='refresh']", function(e) {
    e.preventDefault();
    window.location.reload();
  });

  $(document).ready(function() {
    var contest_id = $(document.body).data("contest-id");
    if (!contest_id) {
      return;
    }
    var protocol = (window.location.protocol === "https") ? "wss" : "ws";
    var hostname = window.location.host;

    var path = "/contests/" + contest_id + "/events";
    var socket_uri = protocol + "://" + hostname + path;

    setupSocket(socket_uri);
  });

})();
