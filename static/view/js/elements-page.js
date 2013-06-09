$(function() {
	var gridster = $("#widgetsmatrix").gridster({
		widget_selector: ".widgetinstance",
		widget_margins: [10, 10],
		widget_base_dimensions: [140, 140],
		serialize_params: function($w, wgd) {
			param = { col: wgd.col, row: wgd.row, instanceid: $w.data('instanceid') }
			if ($w.data('widgetid')) {
				param['widgetid'] = $w.data('widgetid');
			}
			return param;
		}
	}).data('gridster');

    $('#show_widgets').click(function (e) {
		$('#widgetslist').modal();
		return false;
    });
    
    $("a#save").click(function() {
		placement = gridster.serialize();
		$("#pageForm #widgetsplacement").val(JSON.stringify(placement));
		$("#pageForm").submit();
    });

    $("body").on("click", ".del_widget", function() {
		var id = $(this).data("instanceid");
		$("#widgetinstance_" + id).remove();
		$("#configinstance_" + id).remove();
		$.modal.close();
    });

    $("#widgetsmatrix").on("click", ".widgetinstance button", function() {
		var id = $(this).data("instanceid");
		$("#configinstance_" + id).modal();
		return false;
    });
    
    $("#widgetslist").on("click", ".add_widget", function () {
        var widgetid = $(this).data("widgetid");

        var randomnumber=Math.floor(Math.random()*10001)
        var id = 'n' + randomnumber;
		gridster.add_widget("<div id='widgetinstance_" + id + "' class='widgetinstance gs_w'"
							+ "data-instanceid='" + id + "' data-widgetid='" + widgetid + "'>"
							+ widgetid + "<button>Configure</button></div>", 1, 1);
		
        $('#configpanel').append("<div id='configinstance_" + id + "' style='display: none'> \
            <h2>Widget " + id + " parameters</h2> \
            <p><a href='#' class='remove_widget' data-instanceid='" + id + "' role='button'>Remove</a><p> \
            <div class='content'></div> \
            </div>");

        $('#configinstance_' + id + ' .content').load(VIEW_URL + "/elements/widgetparams/" + id + "/" + widgetid);
        $.modal.close();
    });
});