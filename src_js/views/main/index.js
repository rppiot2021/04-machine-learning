import * as plotly from 'plotly.js/dist/plotly.js';
import 'main/index.scss';


export function vt() {
    return plot();
}

export function plot() {
    const layout = {
        title: 'Air quality',
        xaxis: {
            title: 'Hour',
            showgrid: true,
            range: [0, 72]
        },
        yaxis: {
            title: 'CO concentration',
            showline: false,
            range: [600, 2100]
        }
    };
    const config = {
        displayModeBar: true,
        responsive: true,
        staticPlot: true
    };

    const reading_trace = {
        x: r.get('remote', 'timeseries', 'reading').keys(),
        y: r.get('remote', 'timeseries', 'reading'),
        line: { shape: 'spline' },
        type: 'scatter',
        name: 'Reading'
    };
    const forecast_trace = {
        x: r.get('remote', 'timeseries', 'forecast').map((_, k) => k + 47),
        y: r.get('remote', 'timeseries', 'forecast'),
        line: { shape: 'spline' },
        type: 'scatter',
        name: 'Forecast'
    };
    const data = [reading_trace, forecast_trace];
    return ['div.plot', {
        plotData: data,
        props: {
            style: 'height: 100%'
        },
        hook: {
            insert: vnode => plotly.newPlot(vnode.elm, data, layout, config),
            update: (oldVnode, vnode) => {
                if (u.equals(oldVnode.data.plotData, vnode.data.plotData)) return;
                plotly.react(vnode.elm, data, layout, config);
            },
            destroy: vnode => plotly.purge(vnode.elm)
        }
    }
    ];
}
