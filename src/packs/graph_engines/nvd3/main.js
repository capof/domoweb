var ChartNVD3 = ChartCore.extend({

        setup: function(options) {
            this._super(options);
            var self = this, o = this.options;
            $("#dialog-graph").append("<svg style='height: 400px;'></svg>");
            this.chart = nv.models.lineChart();

            this.chart.yAxis
                .axisLabel(o.name + ' (' + o.unit + ')')
                .tickFormat(d3.format('.01f'));

        },
        
        show: function(params) {
            this._super(params);
            var self = this, o = this.options;
            this._init_graph['_'+params.type](self.chart, o, this.from, this.to);
            return this.getdata(params.type) // Get the data from RINOR
                .done(function(values, min, max, avg){
                    self.chart.yDomain([0,max]);

                    d3.select('#dialog-graph svg')
                        .datum(function() { return [
                            {
                                values: self._process_data['_'+params.type](values),
                                key: o.name,
                                color: '#ff7f0e'
                            },
                        ]})
                        .transition().duration(500)
                        .call(self.chart);
//                    nv.addGraph(self.chart);
                });
        },

        _init_graph: {
            _8h: function(graph_options, o, from, to) {
            },

            _24h: function(chart, o, from, to) {
                chart.xAxis
                    .axisLabel('Hour (h:mm)')
                    .ticks(d3.time.hours, 1)
                    .tickFormat(function(d) { return d3.time.format('%H:%M')(new Date(d)); });
            },

            _7d: function(chart, o, from, to) {
                chart.xAxis
                    .axisLabel('Day')
                    .tickFormat(function(d) { return d3.time.format('%A %d')(new Date(d)); });
            },

            _month: function(graph_options, o, from, to) {
            },

            _year: function(graph_options, o, from, to) {
            }
        },
        
        // Used to pre-process data before displaying
        _process_data: {
            _8h: function(values) {
                return values.map(function(d) { return {x:Date.UTC(d[0], d[1]-1, d[3], d[4], d[5], 0), y:d[6]} });
            },
            _24h: function(values) {
                return values.map(function(d) { return {x:Date.UTC(d[0], d[1]-1, d[3], d[4], d[5], 0), y:d[6]} });
            },
            _7d: function(values) {
                return values.map(function(d) { return {x:Date.UTC(d[0], d[1]-1, d[3], d[4], 0, 0), y:d[5]} });
            },
            _month: function(values) {
                return values.map(function(d) { return {x:Date.UTC(d[0], d[1]-1, d[3], 0, 0, 0), y:d[4]} });
            },
            _year: function(values) {
                return values.map(function(d) { return {x:Date.UTC(d[0], d[1]-1, d[3], 0, 0, 0), y:d[4]} });
            }
        }
});
chart.engine = new ChartNVD3();
