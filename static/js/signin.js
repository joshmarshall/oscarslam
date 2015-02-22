$(function() {

  var form = document.getElementById("signin-form");

  $("#signin-reset").click(function() {
    var password = $("#signin-password");
    var button = document.getElementById("signin-submit");
    if (this.checked) {
      form.action = "/reset_password";
      password.hide();
      button.value = "Reset Password";
    } else {
      form.action = "/signin";
      password.show();
      button.value = "Sign In";
    }
  });

  $(form).submit(function() {
    if ($("#signin-email").val() === "") {
      window.location.href = "/?message=unknown_user";
      return false;
    }
    return true;
  });

});
