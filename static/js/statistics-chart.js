var statisticChart,
    CTRChart;

let statisticConfig = {
	type: 'line',
	data: {
            data: [],
        datasets: [
            {
                label: 'Просмотров',
                borderColor: '#36a2eb',
                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                fill: 'end'
            },
            {
                label: 'Подписок',
                borderColor: '#ff6384',
                backgroundColor: 'rgba(200, 78, 137, 0.1)',
                fill: 'start'
            }
        ]
    },
    options: {
        responsive: true,
        title: {
            display: true
        },
        tooltips: {
            mode: 'index',
            intersect: false,
            backgroundColor: 'rgb(60, 64, 112, 0.9)',
        },
        legend: {
            display: true,
        },
        scales: {
            yAxes: [{
                display: true,
                ticks: {
                    suggestedMin: 0,
                    beginAtZero: true,
                    stepSize: 1
                }
            }]
        }
	}
};

let CTRConfig = {
    type: 'line',
	data: {
        datasets: [
            {
                label: 'Конверсия',
                borderColor: '#36a2eb',
                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                fill: 'end'
            }
        ]
    },
    options: {
        responsive: true,
        title: {
            display: true
        },
        tooltips: {
            mode: 'index',
            intersect: false,
            backgroundColor: 'rgb(60, 64, 112, 0.9)',
        },
        legend: {
            display: true,
            onClick: ()=>{}
        },
        scales: {
            yAxes: [{
                display: true,
                ticks: {
                    suggestedMin: 0,
                    min: 0,
                    max: 100,
                    suggestedMax: 100,
                }
            }]
        }
	},
};

// Chart.defaults.global.fontFamily = "Nunito";
// Chart.defaults.global.defaultFontSize = 14;
// Chart.defaults.global.defaultFontColor = '#717171';
// Chart.defaults.global.elements.point.radius = 5;

$(document).ready(function() {
    $.ajax({
        method: 'get',
        url: 'get-statistic/',

        success: function(data) {
            let statisticLabels = [],
                statisticDatasets = [[], []],
                CTRLabels = [],
                CTRDatasets = [[]];

            console.log(data);

            for (let date in data) {
                if (['views', 'subscribers', 'ctr'].indexOf(date) === -1) {
                    statisticLabels.push(date);
                    CTRLabels.push(date);

                    statisticDatasets[0].push(data[date][0]);
                    statisticDatasets[1].push(data[date][1]);

                    CTRDatasets[0].push(data[date][2]);
                } else {
                    let views = $('#viewsValue'),
                        subscribers = $('#subscribersValue'),
                        ctr = $('#ctrValue');

                    if (date === 'views') views.text(data[date]);
                    else if (date === 'subscribers') subscribers.text(data[date]);
                    else if (date === 'ctr') ctr.text(data[date] + ' %')
                }
            }
            statisticConfig.data.labels = statisticLabels;
            statisticConfig.data.datasets[0].data = statisticDatasets[0];
            statisticConfig.data.datasets[1].data = statisticDatasets[1];

            CTRConfig.data.labels = CTRLabels;
            CTRConfig.data.datasets[0].data = CTRDatasets[0];

            let statisticChartCanvas = document.getElementById('statistik').getContext('2d'),
                CTRChartCanvas = document.getElementById('CTRChart').getContext('2d');

            statisticChart = new Chart(statisticChartCanvas, statisticConfig);
            CTRChart = new Chart(CTRChartCanvas, CTRConfig);
        }
    });
});
$(document).ready(function () {
    $(document).on('click', '.applyBtn, .ranges ul li', function () {
        let start_date = $('input[name=start_date]').val(),
            end_date = $('input[name=end_date]').val();
        console.log(start_date, end_date);

        if (!start_date || !end_date) {
            return
        }

        $.ajax({
            method: 'get',
            url: 'get-statistic/',
            data: {
                start_date: start_date,
                end_date: end_date
            },

            success: function(data) {
                let statisticLabels = [],
                    statisticDatasets = [[], []],
                    CTRLabels = [],
                    CTRDatasets = [[]];

                for (let date in data) {
                    if (['views', 'subscribers', 'ctr'].indexOf(date) === -1) {
                        statisticLabels.push(date);
                        CTRLabels.push(date);

                        statisticDatasets[0].push(data[date][0]);
                        statisticDatasets[1].push(data[date][1]);

                        CTRDatasets[0].push(data[date][2]);
                    } else {
                        let views = $('#viewsValue'),
                            subscribers = $('#subscribersValue'),
                            ctr = $('#ctrValue');
                        console.log(date)
                        console.log('hello')
                        console.log(data)
                        if (date === 'views') views.text(data[date]);
                        else if (date === 'subscribers') subscribers.text(data[date]);
                        else if (date === 'ctr') ctr.text(data[date] + ' %')
                    }
                }
                statisticConfig.data.labels = statisticLabels;
                statisticConfig.data.datasets[0].data = statisticDatasets[0];
                statisticConfig.data.datasets[1].data = statisticDatasets[1];

                CTRConfig.data.labels = CTRLabels;
                CTRConfig.data.datasets[0].data = CTRDatasets[0];

                let statisticChartCanvas = document.getElementById('statistik').getContext('2d'),
                    CTRChartCanvas = document.getElementById('CTRChart').getContext('2d');

                statisticChart.destroy();
                CTRChart.destroy();

                statisticChart = new Chart(statisticChartCanvas, statisticConfig);
                CTRChart = new Chart(CTRChartCanvas, CTRConfig);
            }
        });
    });
});

$(document).ready(function() {
	let w = $(window).width(),
        statisticChart = $('#statistik'),
        CTRChart = $('#CTRChart');

	if (w <= 600) {
	    statisticChart.attr('height', 300);
	    statisticChart.attr('width', 300);

	    CTRChart.attr('height', 300);
	    CTRChart.attr('width', 300);
	} else {
	    statisticChart.attr('height', 1);
	    statisticChart.attr('width', 2);

	    CTRChart.attr('height', 1);
	    CTRChart.attr('width', 2);
    }
});
