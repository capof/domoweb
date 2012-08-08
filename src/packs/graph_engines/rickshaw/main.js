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
