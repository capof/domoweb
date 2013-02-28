(function($) {
    $.create_widget({
        // default options
        options: {
            version: 0.1,
            creator: 'Domogik',
            id: 'dmg_3x1_basicNoStateActuatorBinary',
            name: 'Stateless basic widget',
            description: 'Basic switch widget (x10, broken plcbus, . . .)',
            screenshot: 'dmg_3x1_basicNoStateActuatorBinary.png',
            type: 'actuator.binary',
            height: 1,
            width: 3,
            displayname: true,
            displayborder: true
        },

        _init: function() {
            var self = this, o = this.options;
            this.param = o.params[0];
            this.element.addClass("icon32-usage-" + o.usage)
              .processing();
            // Building widget content
            var main = $("<div class='main'></div>");
            var on_action = $('<div class="command on">ON</div>');
            on_action.click(function (e) {self.action(self.param.values[1]);e.stopPropagation();})
                .keypress(function (e) {if (e.which == 33 || e.which == 38) {self.action(o.values[1]); e.stopPropagation();}});
            main.append(on_action);
            var off_action = $('<div class="command off">OFF</div>');
            off_action.click(function (e) {self.action(self.param.values[0]);e.stopPropagation();})
                .keypress(function (e) {if (e.which == 34 || e.which == 40) {self.action(o.values[0]); e.stopPropagation();}});
            main.append(off_action);
            
            this.element.append(main);
        },
        
        _statsHandler: function(stats) {
        },
        
        _eventHandler: function(timestamp, value) {
        },
        
        action: function(command_code) {
            var self = this, o = this.options;
      	    data = {};
            data[this.param.key] = command_code;
	    rinor.put(['api', 'command', o.featureid], data)
                .done(function(data, status, xhr){
                    self.valid(o.featureconfirmation);
                })
                .fail(function(jqXHR, status, error){
                    self.cancel();
                    if (jqXHR.status == 400)
                        $.notification('error', jqXHR.responseText);
                });
        },
        cancel: function() {
            this.element.stopProcessingState();
        },

        /* Valid the processing state */
        valid: function(confirmed) {
            this.element.stopProcessingState();
        }
    });
})(jQuery);
