//
// tool_timer.js
//
// implements browser-side behaviors for the tool timer
//
$(function () {

  tool_runtime_secs = 0;
  tool_started = false;
  total_charges = 0;

  // bind buttons to actions
  $('#home-button').on('click',RenderHomeDiv);
  $('#admin-button').on('click',RenderAdminDiv);
  $('#login-button').on('click',LoginUser);
  $('#start-tool-button').on('click',StartTool);
  $('#stop-tool-button').on('click',StopTool);
  $('#auth-id-input').change(LoginUser);

  // dynamically loaded elements
  $('#top-tool-div').on('click','.logout-button',StartLogout);
  $('#top-tool-div').on('click','.login-button',StartLoginButton);
  $('#top-tool-div').on('click','.pay-now-button',PayNowButton);
  

  $("#tool-div :button").prop('disabled',true); // tool buttons always start out disabled

  // make initial status request
  cmd = '&action=get_info' 
  server_ajax_request(cmd,GetInfoSuccess,GetInfoError);

  // Call OneSecChores() 1x per second
  setInterval(OneSecChores,1000);

function StartLoginButton() {
  $('#charges-message').html('');
  $('#login-div').show(250);
  tool_runtime_secs = 0;
  DisplayTime();
}

function StartLogout() {
  $('#top-message').html('')
  cmd = '&action=logout' 

  server_ajax_request(cmd,GetInfoSuccess,GetInfoError);
}

function GetInfoSuccess(json) {

  if (json.membership_level == 'logged_out') {
    // not logged in
    $("#tool-div :button").prop('disabled',true);
    //$("#login-div").show(250)
    $("#charges-message").html('');
    $("#auth-id-select-blank").prop('selected', true);
  } else {
    // logged in
    $("#tool-div :button").prop('disabled',true);
    if (json.tool_started)
      $("#stop-tool-button").prop('disabled',false);
    else
      $("#start-tool-button").prop('disabled',false);

    $("#charges-div").show(250);
    $("#rate-info-div").html(json.rate_info);
    $("#rate-info-div").show(250);
    $("#login-div").hide(250);
  }

  tool_started = json.tool_started;
  tool_runtime_secs = parseInt(json.tool_runtime_secs);
  total_charges = parseFloat(json.total_charges);

  if (json.tool_started)
    $("#tool-main-message").html("TOOL IS <strong>ON</strong>");
  else
    $("#tool-main-message").html("TOOL IS <strong>OFF</strong>");

  $("#charges-message").html(json.message)

  DisplayTime()
  DisplayCharge()
}


function GetInfoError() {

}

  

function RenderHomeDiv(ThisButton) {
  $('#top-nav').find('li').removeClass('active');
  $('#home-button').parent().addClass('active')
  $('.app-div').hide();
  $('#home-div').show();
}

function RenderAdminDiv(ThisButton) {
  $('#top-nav').find('li').removeClass('active');
  $('#admin-button').parent().addClass('active')
    $('.app-div').hide();
  $('#admin-div').show();
}

function server_ajax_request(form_data,success_callback,error_callback) {

  $.ajax( {
    async      : true,
    type       : "post",
    url        : "/ajax",
    data       : form_data,
    dataType   : 'json', // say 'jsonp' to get cross-domain posting capability
    beforeSend : function () { $("#messages").html(''); },
    success    : success_callback, // ajax_success ,
    error      : error_callback, // ajax_error,
  });
  return false;
}

function ajax_error(json) {
  //$("#messages").append('something bad happened. Server Didn\'t elaborate<br>');
  //$("#messages").fadeIn();
  return json
}

function ajax_success(json) {

  //$("#messages").html(json.message);
  //$("#messages").fadeIn();

  return json;
}
function LoginSuccess(json) {
  if (json.error == 0) {
    $("#tool-div :button").prop('disabled',false);
    $("#login-div").hide(250);
    $("#charges-div").show(250);
    $("#top-message").html(json.message)
  }
}
function LoginError() {
  $("#top-message").html("Something bad happened. Server did not respond as expected");
}

function LoginUser() {
  cmd = '&action=login&arg1=' + $("#auth-id-input").val() + '&arg2=' + $("#auth-password-input").val() 
  server_ajax_request(cmd,GetInfoSuccess,LoginError);
  return false;
}

function StartTool() {
  $("#stop-tool-button").prop('disabled',false);
  $("#start-tool-button").prop('disabled',true);
  server_ajax_request('&action=tool_start',ajax_success,ajax_error);
  $('#admin-messages').html('Relay CLOSED');
  server_ajax_request(cmd,GetInfoSuccess,GetInfoError);
}

function StopTool() {
  $("#stop-tool-button").prop('disabled',true);
  $("#start-tool-button").prop('disabled',false);
  server_ajax_request('&action=tool_stop',ajax_success,ajax_error);
  $('#admin-messages').html('Relay OPEN');
  server_ajax_request(cmd,GetInfoSuccess,GetInfoError);
}

function FifteenSecChores() {
  // periodic get info to server where state is kept 
  cmd = '&action=get_info' 
  server_ajax_request(cmd,GetInfoSuccess,GetInfoError);
}

function OneSecChores() {

  if (tool_started) {
    tool_runtime_secs++;
    if ( !(tool_runtime_secs % 15) ) {
      FifteenSecChores();
    }
  }
  DisplayTime();

}

function DisplayTime() {

  tool_runtime_secs_int = parseInt(tool_runtime_secs);

  time_display = '';
  time_display += sprintf("%02.2d:",(tool_runtime_secs_int / 3600) % 24);
  time_display += sprintf("%02.2d:",(tool_runtime_secs_int / 60) % 60);
  time_display += sprintf("%02.2d",tool_runtime_secs_int % 60);

  $('#total-time').html(time_display);

}

function DisplayCharge() {
  $('#total-charge').html(sprintf("%3.2f",total_charges));
}

function PayNowButton() {

    m = '';
    m += 'Log Into <a target="#" href="https://www.nova-labs.org/account/accounting.html">Your Nova Labs Account</a><br>';
    m += 'And make a one-time payment of <b>$' + total_charges + '</b><br>';
    m += '<button id="start-logout-button" class="btn btn-sm btn-primary logout-button">LOGOUT</button>';
    $('#charges-message').html(m);
}

});

