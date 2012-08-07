var ChartRickshaw = ChartCore.extend({
        setup: function(options) {
            this._super(options);
            var self = this, o = this.options;
            this.series = []
            this.graph_options = {
                element: document.querySelector("#dialog-graph"),
                renderer: 'area',
                stroke: true,
                series: this.series,
            };
        },
        
        show: function(params) {
            this._super(params);
            var self = this, o = this.options;
            return this.getdata(params.type) // Get the data from RINOR
                .done(function(values, min, max, avg){
                    var data = self._process_data['_'+params.type](values);
                    self.series.length = 0;
                    self.series.push({
                        name: o.title,
                        color: 'lightblue',
                        data: data
                        });
                    if (self.graph) {
                        self.graph.update();
                    } else {
                        self.graph = new Rickshaw.Graph(self.graph_options);
            
                        var hoverDetail = new Rickshaw.Graph.HoverDetail({
                            graph: self.graph,
                            xFormatter: function(x) { var d = new Date(x*1000); return d.toString("H:m"); },
                            yFormatter: function(y) { return y + " " + o.unit; }
                        });
                        
                        var xAxis = new Rickshaw.Graph.Axis.Time({
                            graph: self.graph,
                        });
              
                        var yAxis = new Rickshaw.Graph.Axis.Y({
                            graph: self.graph,
                        });
                        self.graph.render();
                    }
                });
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
                var self = this;

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
                    d.push({x:(Date.UTC(stat[0], stat[1]-1, stat[3], stat[4], 0, 0)/ 1000), y:stat[5]});
                });
                return d;
            },
            _month: function(values) {
                var d = [];
                $.each(values, function(index, stat) {
                    d.push({x:(Date.UTC(stat[0], stat[1]-1, stat[3], 0, 0, 0)/ 1000), y:stat[4]});
                });
                return d;
            },
            _year: function(values) {
                var d = [];
                $.each(values, function(index, stat) {
                    d.push({x:(Date.UTC(stat[0], stat[1]-1, stat[3], 0, 0, 0)/ 1000), y:stat[4]});
                });
                return d;
            }
        }
});
chart.engine = new ChartRickshaw();
