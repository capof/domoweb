    var chart = {} ;
    var ChartCore = Class.extend({
        // default options
        defaults : {
            device_id: null,
            key: null,
            title: '',
            unit: '',
        },
		
		setup: function(options) {
			this.options = $.extend({}, this.defaults, options);
            var self = this, o = this.options;
        },
        
        show: function(params) {
            this.now = new Date();
            switch(params.type) {
                case '8h':
                    this.from = new Date(this.now.getFullYear(), this.now.getMonth(), this.now.getDate(),this.now.getHours()-8-(8*params.shift),0,0);
                    this.to = new Date(this.now.getFullYear(), this.now.getMonth(), this.now.getDate(),this.now.getHours()+1-(8*params.shift),0,0);
                    break;
                case '24h':
                    this.from = new Date(this.now.getFullYear(), this.now.getMonth(), this.now.getDate()-1-params.shift,this.now.getHours(),0,0);
                    this.to = new Date(this.now.getFullYear(), this.now.getMonth(), this.now.getDate()-params.shift,this.now.getHours()+1,0,0);
                    break;
                case '7d':
                    this.from =new Date(this.now.getFullYear(), this.now.getMonth(), this.now.getDate()-(7*(params.shift+1)),this.now.getHours(),0,0);
                    this.to = new Date(this.now.getFullYear(), this.now.getMonth(), this.now.getDate()-(7*params.shift),this.now.getHours()+1,0,0);
                    break;
                case 'month':            
                    var lastDayMonth = (new Date((new Date(this.now.getFullYear(), this.now.getMonth()-params.shift+1,1))-1)).getDate();
                    this.from = new Date(this.now.getFullYear(), this.now.getMonth()-params.shift, 1,0,0,0);
                    this.to = new Date(this.now.getFullYear(), this.now.getMonth()-params.shift, lastDayMonth,23,59,59);
                    break;
                case 'year':
                    this.from = new Date(this.now.getFullYear()-params.shift, 0, 1,0,0,0);
                    this.to = new Date(this.now.getFullYear()-params.shift, 11, 31,23,59,59);
                    break;
            }
        },
        
        getdata: function(type) {
            var self = this, o = this.options;
            var restparams = null;
            switch(type) {
                case '8h':
                    restparams = ['api','state', 'from', Math.round(self.from.getTime() / 1000), 'to', Math.round(self.to.getTime() / 1000),'interval', 'minute', 'selector', 'avg', o.device_id, o.key];
                    break;
                case '24h':
                    restparams = ['api','state', 'from', Math.round(self.from.getTime() / 1000), 'to', Math.round(self.to.getTime() / 1000),'interval', 'minute', 'selector', 'avg', o.device_id, o.key];
                    break;
                case '7d':
                    restparams = ['api', 'state', 'from', Math.round(self.from.getTime() / 1000), 'to', Math.round(self.to.getTime() / 1000),'interval', 'hour', 'selector', 'avg', o.device_id, o.key];
                    break;
                case 'month':
                    restparams = ['api', 'state', 'from', Math.round(self.from.getTime() / 1000), 'to', Math.round(self.to.getTime() / 1000),'interval', 'day', 'selector', 'avg', o.device_id, o.key];
                    break;
                case 'year':
                    restparams = ['api', 'state', 'from', Math.round(self.from.getTime() / 1000), 'to', Math.round(self.to.getTime() / 1000),'interval', 'day', 'selector', 'avg', o.device_id, o.key];

                    break;
            }

            defer = $.Deferred();

            rinor.get(restparams)
                .done(function(data, status, xhr){
                    defer.resolve(data.values, data.global_values.min, data.global_values.max, data.global_values.avg);
                })
                .fail(function(jqXHR, status, error){
                    if (jqXHR.status == 400)
                        $.notification('error', gettext('Data creation failed') + ' (' + jqXHR.responseText + ')');
                    defer.reject(jqXHR, status, error);
                });
            return defer.promise();
        },
    });
