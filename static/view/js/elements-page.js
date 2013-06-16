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

    $("body").on("click", ".widgetinstance .del_widget", function() {
		var id = $(this).data("instanceid");
		gridster.remove_widget($("#widgetinstance_" + id));
		$("#configinstance_" + id).remove();
		$.modal.close();
    });

    $("#widgetsmatrix").on("click", ".widgetinstance .conf_widget", function() {
		var instanceid = $(this).data("instanceid");
		var widgetid = $(this).data("widgetid");
		$("#configinstance_" + instanceid).data('forceclose', false);

		$("#configinstance_" + instanceid).modal({
			persist: true,
			onClose: function() {
				var self=this;
				if ($("#configinstance_" + instanceid).data('forceclose') == true) {
					$.modal.close();
				} else {
					$.ajax({
						type:"POST",
						data: $("#simplemodal-container :input").serialize(),
						url:VIEW_URL + "/elements/widgetparams/" + instanceid + "/" + widgetid, 
						success: function(data, textStatus, jqXHR){
							$('#configinstance_' + instanceid + ' .widget_parameters').html(data);
							$('#configinstance_' + instanceid + ' .widget_parameters input[type=text].mask').maskInput();

							if (jqXHR.status==210) { // Validation error
								$("#simplemodal-container .force_close").show();
								$("#simplemodal-container").addClass('validation_errors');
								$("#widgetinstance_" + instanceid).addClass('not_configured');
								self.occb = false;
								self.bindEvents();
							} else {
								$("#simplemodal-container").removeClass('validation_errors');
								$("#widgetinstance_" + instanceid).removeClass('not_configured');
								$.modal.close();
							}
						}
					});
				}
			}
		});
		
		return false;
    });
    
	$("body").on("click", ".force_close", function() {
		var instanceid = $(this).data("instanceid");
		$("#configinstance_" + instanceid).data('forceclose', true);
		$.modal.close();
	});
	
    $("#widgetslist").on("click", ".add_widget", function () {
        var widgetid = $(this).data("widgetid");
        var width = $(this).data("width");
        var height = $(this).data("height");

        var randomnumber=Math.floor(Math.random()*10001)
        var id = 'n' + randomnumber;
		gridster.add_widget("<div id='widgetinstance_" + id + "' class='widgetinstance gs_w not_configured'"
							+ "data-instanceid='" + id + "' data-widgetid='" + widgetid + "'>"
							+ widgetid
							+ "<button class='conf_widget' data-instanceid=" + id + " data-widgetid='" + widgetid + "'>" + gettext('Configure') + "</button>"
							+ "<button class='del_widget' data-instanceid=" + id + ">" + gettext('Remove') + "</button>"
							, width, height);
		
        $('#widgetsconfig').append("<div id='configinstance_" + id + "' style='display: none'> \
            <h2>Widget " + id + " parameters</h2> \
            <div class='widget_parameters'></div> \
            </div>");

        $('#configinstance_' + id + ' .widget_parameters').load(VIEW_URL + "/elements/widgetparams/" + id + "/" + widgetid, function() {
			$('#configinstance_' + id + ' .widget_parameters input[type=text].mask').maskInput();
		});
        $.modal.close();
    });	
});