var ChartRickshaw = ChartCore.extend({
        show: function(options) {
            this._super(options);
            var self = this, o = this.options;

/*            graph_options = this._init_graph['_'+o.type](graph_options, o, this.from, this.to);*/

            return this.getdata() // Get the data from RINOR
                .done(function(values, min, max, avg){
                    var data = self._process_data['_'+o.type](values);
                    console.log(data);
                                var graph_options = {
                element: document.querySelector("#dialog-graph"),
                width: 580,
                height: 250,
                series: []
            };
                    graph_options.series.push({
                        color: 'steelblue',
                        data: data
                        });
                    this.graph = new Rickshaw.Graph(graph_options);
                    var axes = new Rickshaw.Graph.Axis.Time( { graph: this.graph } );

                        this.graph.render();
                }); 
        },
        
        reset: function() {
            if (this.graph) this.graph.destroy();
        },
        
        _init_graph: {
            _8h: function(graph_options, o, from, to) {
                graph_options.title.text = Highcharts.dateFormat('%A %d %B %Y', to.getTime());
                graph_options.xAxis.min = Date.UTC(from.getFullYear(), from.getMonth(), from.getDate(),from.getHours(),0,0);
                graph_options.xAxis.max = Date.UTC(to.getFullYear(), to.getMonth(), to.getDate(),to.getHours(),0,0);
                graph_options.xAxis.dateTimeLabelFormats = {hour: '%H:%M'};
                graph_options.xAxis.tickInterval = null;
                graph_options.tooltip.formatter = function() {
                    return Highcharts.dateFormat('%d/%m/%Y %Hh%M', this.x) +'<br/>'
                        + "<strong>" + Highcharts.numberFormat(this.y, 2, ',') +" " + o.unit + "</strong>";
                    };
                return graph_options;
            },

            _24h: function(graph_options, o, from, to) {
                graph_options.title.text = Highcharts.dateFormat('%A %d %B %Y', to.getTime());
                graph_options.xAxis.min = Date.UTC(from.getFullYear(), from.getMonth(), from.getDate(),from.getHours(),0,0);
                graph_options.xAxis.max = Date.UTC(to.getFullYear(), to.getMonth(), to.getDate(),to.getHours(),0,0);
                graph_options.xAxis.dateTimeLabelFormats = {hour: '%H:%M'};
                graph_options.xAxis.tickInterval = null;
                graph_options.tooltip.formatter = function() {
                    return Highcharts.dateFormat('%d/%m/%Y %Hh%M', this.x) +'<br/>'
                        + "<strong>" + Highcharts.numberFormat(this.y, 2, ',') +" " + o.unit + "</strong>";
                    };
                return graph_options;
            },

            _7d: function(graph_options, o, from, to) {
                graph_options.title.text = Highcharts.dateFormat('%d/%m/%Y', from.getTime()) + " - " + Highcharts.dateFormat('%d/%m/%Y', to.getTime());
                graph_options.xAxis.min = Date.UTC(from.getFullYear(), from.getMonth(), from.getDate(), from.getHours(),0,0);
                graph_options.xAxis.max = Date.UTC(to.getFullYear(), to.getMonth(), to.getDate(), to.getHours()+1,0,0);
                graph_options.xAxis.dateTimeLabelFormats = {day: '%A %e'};
                graph_options.xAxis.tickInterval = 24 * 3600 * 1000; // a day
                graph_options.tooltip.formatter = function() {
                    return Highcharts.dateFormat('%d/%m/%Y %Hh', this.x) +'<br/>'
                        + "<strong>" + Highcharts.numberFormat(this.y, 2, ',') +" " + o.unit + "</strong>";
                    };
                return graph_options;
            },

            _month: function(graph_options, o, from, to) {
                graph_options.title.text = Highcharts.dateFormat('%B %Y', to.getTime())
                graph_options.xAxis.min = Date.UTC(from.getFullYear(), from.getMonth(), 1);
                graph_options.xAxis.max = Date.UTC(to.getFullYear(), to.getMonth(), 31, 23,59,59);
                graph_options.xAxis.dateTimeLabelFormats = {day: '%e. %b'};
                graph_options.xAxis.tickInterval = null;
                graph_options.tooltip.formatter = function() {
                    return Highcharts.dateFormat('%d/%m/%Y', this.x) +'<br/>'
                        + "<strong>" + Highcharts.numberFormat(this.y, 2, ',') +" " + o.unit + "</strong>";
                    };
                return graph_options;
            },

            _year: function(graph_options, o, from, to) {
                graph_options.title.text = Highcharts.dateFormat('%Y', to.getTime())
                graph_options.xAxis.min = Date.UTC(from.getFullYear(), 0, 1);
                graph_options.xAxis.max = Date.UTC(to.getFullYear(), 11, 31, 23,59,59);
                graph_options.xAxis.dateTimeLabelFormats = {month: '%b %y'};
                graph_options.xAxis.tickInterval = null;
                graph_options.tooltip.formatter = function() {
                    return Highcharts.dateFormat('%d/%m/%Y', this.x) +'<br/>'
                        + "<strong>" + Highcharts.numberFormat(this.y, 2, ',') +" " + o.unit + "</strong>";
                    };
                return graph_options;
            }
        },

        // Used to pre-process data before displaying
        _process_data: {
            _8h: function(values) {
                var d = [];
                $.each(values, function(index, stat) {
                    d.push({x:(Date.UTC(stat[0], stat[1]-1, stat[3], stat[4], stat[5], 0)/ 1000), y:stat[6]});
                });
                return d;
            },

            _24h: function(values) {
                var d = [];
                $.each(values, function(index, stat) {
                    d.push({x:(Date.UTC(stat[0], stat[1]-1, stat[3], stat[4], stat[5], 0)/ 1000), y:stat[6]});
                });
                return d;
            },
            _7d: function(values) {
                var d = [];
                $.each(values, function(index, stat) {
                    d.push({x:(Date.UTC(stat[0], stat[1]-1, stat[3], stat[4], 0, 0/ 1000)), y:stat[5]});
                });
                return d;
            },
            _month: function(values) {
                var d = [];
                $.each(values, function(index, stat) {
                    d.push({x:Date.UTC(stat[0], stat[1]-1, stat[3], 0, 0, 0), y:stat[4]});
                });
                return d;
            },
            _year: function(values) {
                var d = [];
                $.each(values, function(index, stat) {
                    d.push({x:Date.UTC(stat[0], stat[1]-1, stat[3], 0, 0, 0), y:stat[4]});
                });
                return d;
            }
        }
});
chart.engine = new ChartRickshaw();
