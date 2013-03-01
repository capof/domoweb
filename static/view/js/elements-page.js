$(function() {
    $('#show_widgets').click(function (e) {
	$('#widgetslist').modal();
	return false;
    });
    
    $("a#save").click(function() {
	$("#pageForm").submit();
    });

    $("body").on("click", ".del_widget", function() {
	var id = $(this).data("instanceid");
	$("#widgetinstance_" + id).remove();
	$("#configinstance_" + id).remove();
	$.modal.close();
    });

    $("#widgetsmatrix").on("click", ".widgetinstance", function() {
	var id = $(this).data("instanceid");
	$("#configinstance_" + id).modal();
	return false;
    });
    
    $("#widgetslist").on("click", ".add_widget", function () {
        var widgetid = $(this).data("widgetid");

        var randomnumber=Math.floor(Math.random()*10001)
        var id = 'n' + randomnumber;
        $('#widgetsmatrix').append("<button id='widgetinstance_" + id + "' class='widgetinstance' data-instanceid='" + id + "'>" + widgetid + " \
                <input type='hidden' name='instance[" + id + "][widgetid]' value='" + widgetid + "' /> \
                </button>");
    
        $('#configpanel').append("<div id='configinstance_" + id + "' style='display: none'> \
            <h2>Widget " + id + " parameters</h2> \
            <p><a href='#' class='remove_widget' data-instanceid='" + id + "' role='button'>Remove</a><p> \
            <div class='content'></div> \
            </div>");

        $('#configinstance_' + id + ' .content').load(VIEW_URL + "/elements/widgetparams/" + id + "/" + widgetid);
        $.modal.close();
    });
});

(function($) {    

})(jQuery);