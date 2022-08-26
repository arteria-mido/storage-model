let rawData = {};
let TIMESTEP = 88;

window.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById("upload").addEventListener("change", loadFile);
})

function loadFile(e) {
    let file = e.target.files[0];
    let reader = new FileReader();
    reader.readAsText(file);
    reader.onload = drawChart;
}

function drawChart(e) {
    let filePath = e.target.result;
    let json = JSON.parse(filePath);
    rawData = json;

    rawData.timestamps = addTimestamps(rawData['actual load cap'].length);

    /* increases timestep for all three arrays */
    // let timestamps = increaseTimeStep(rawData.timestamps);
    // let hwd = increaseTimeStep(rawData['hot water demand']);
    // let alc = increaseTimeStep(rawData['actual load cap']);

    /* drawing chart with timesteps */
    // hotWaterDemand_series = zip(timestamps, hwd.map(d => roundFloat(d, 2)));
    // actualLoadCap_series = zip(timestamps, alc.map(d => roundFloat(d, 2)));

    hotWaterDemand_series = zip(rawData.timestamps, rawData['hot water demand'].map(d => roundFloat(d, 2)));
    actualLoadCap_series = zip(rawData.timestamps, rawData['actual load cap'].map(d => roundFloat(d, 2)));

    let chartOptions = {
        chart: { type: 'spline', zoomType: 'x'},
        title: { text: 'Hot water demand and actual load capacity'},
        xAxis: {
            crosshair: true,
            title: { text: 'Time [hourly]' },
            type: 'datetime'
        },
        yAxis: { title: { text: 'Unit [kW]'}},
        tooltip: { shared: true },
        credits: { enabled: false },
        plotOptions: {
            series: { marker: { enabled: false }},
            // dataLabels : {
            //     enabled : true,
            //     formatter: function() {
            //         return (this.isFirst || this.isLast) ? this.value : '';
            //     }
            //   },
        },

        series: [
            { name: 'Warmwasserbedarf', color: 'orange', data: hotWaterDemand_series},
            { name: 'Actual load capacity', color: 'lightgreen',data: actualLoadCap_series}
        ]
    };

    Highcharts.chart('chart_container', chartOptions);
}

function addTimestamps(arrayLength) {
    let timestampsArray = [];
    let startDate = new Date("January 1, 2022 00:00:00");
    timestampsArray[0] = startDate.getTime();
    
    for (let i = 1; i < arrayLength; i++) {
        timestampsArray[i] = timestampsArray[i - 1] + 3600*1000;
    }
    console.log('first element: ', timestampsArray[0]);
    console.log('second element: ', timestampsArray[1])
    return timestampsArray;
}

function roundFloat(float, digit) {
    return Number(parseFloat(float).toFixed(digit));
}

function zip(array1, array2) {
    let zippedArray = array1.map((element, index) => {
        return [element, array2[index]];
    });
    return zippedArray;
}

function increaseTimeStep(array) {
    let filteredArr = [];
    for (let i = 0; i < array.length; i++) {
        if (i % TIMESTEP == 0) { filteredArr.push(array[i]) }
    }
    return filteredArr;
}

// function normalizedDataTable() {
//     timeCol = increaseTimeStep(rawData.timestamps);
//     hotWaterCol = increaseTimeStep(rawData['hot water demand']);
// }