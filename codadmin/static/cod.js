function run_cmd(button,server_id, action)
{
    url = "/ajax/server/" + server_id + "/" + action;
    jQuery(button).toggleClass('but_' + action).toggleClass('ajax-loading');
    
    jQuery.getJSON(url, function(data)
        {
            print_message(data)
        }
    )
    .fail(function (data)
        {
            jQuery.sticky('<h3>HTTP ERROR</h3>');
        }
    )
    .always(function (data)
        {
            jQuery(button).removeClass('ajax-loading').addClass('but_' + action);
        }
    );


}

function print_message(message)
{
    jQuery.sticky('<h3>' + message.status + "</h3><p>" + message.message + "</p>");
}
