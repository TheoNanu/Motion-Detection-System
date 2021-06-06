function chartBuildPhase1(canvasId, label, dataChart)
{
	var ctx = document.getElementById(canvasId);
	var chartName = new Chart(ctx, {
		  type: 'line',
		  options:{
		    tooltips: {enabled: false},
			hover: {mode: null},
			legend:
			{
				labels:{
				fontColor: "#202020",
				fontSize: 14,
				fontFamily: 'Helvetica Neue',
				}
			},
			  scales: 
			  {
				  xAxes: 
				[{
					ticks: 
					{
						display: false
					},
					gridLines: 
					{
						display:false
					}
				}],
				  yAxes: 
				[{
					gridLines: 
					{
						display:true
					}   
				}]
			}
		},
		  data: {
			labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
			datasets: [
			  { label: label,
				data: dataChart,
				borderColor: '1C4E80',
                backgroundColor: '#0091D5',
				cubicInterpolationMode:'monotone',
				lineTension:'0'
			  } 
			]
		  }
		});
		return chartName;
}

function chartBuildPhase2(canvasId, label, dataChart)
{
	var ctx = document.getElementById(canvasId);
	var chartName = new Chart(ctx, {
		  type: 'line',
		  options: 
{
		    tooltips: {enabled: false},
			hover: {mode: null},
			legend:
			{
				labels:{
				fontColor: "#202020",
				fontSize: 14,
				fontFamily: 'Helvetica Neue',
				}
			},
			  scales: 
			  {
				  xAxes: 
				[{
					ticks: 
					{
						display: false,
						min:0,
						max:100,
						stepSize:20
					},
					gridLines: 
					{
						display:false
					}
				}],
				  yAxes: 
				[{
					gridLines: 
					{
						display:true
					}   
				}]
			}
		},
		  data: {
			labels: [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2],
			datasets: [
			  { label: label,
				data: dataChart,
				borderColor: '1C4E80',
                backgroundColor: '#A5D8DD',
				cubicInterpolationMode:'monotone',
				lineTension:'0'
			  } 
			]
		  }
		});
		return chartName;
}

function chartBuildPhase3(canvasId, label, dataChart)
{
	var ctx = document.getElementById(canvasId);
	var chartName = new Chart(ctx, {
		  type: 'line',
		  options: 
{
		    tooltips: {enabled: false},
			hover: {mode: null},
			legend:
			{
				labels:{
				fontColor: "#202020",
				fontSize: 14,
				fontFamily: 'Helvetica Neue',
				}
			},
			  scales: 
			  {
				  xAxes: 
				[{
					ticks: 
					{
						display: false
					},
					gridLines: 
					{
						display:false
					}
				}],
				  yAxes: 
				[{
					gridLines: 
					{
						display:true
					}   
				}]
			}
		},
		  data: {
			labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
			datasets: [
			  { label: label,
				data: dataChart,
				borderColor: '1C4E80',
                backgroundColor: '#EA6A47',
				cubicInterpolationMode:'monotone',
				lineTension:'0'
			  } 
			]
		  }
		});
		return chartName;
}

function chartBuildPower(canvasId, label, dataChart)
{
	var ctx = document.getElementById(canvasId);
	var chartName = new Chart(ctx, {
		  type: 'line',
		  options: 
{
		    tooltips: {enabled: false},
			hover: {mode: null},
			legend:
			{
				labels:{
				fontColor: "#202020",
				fontSize: 14,
				fontFamily: 'Helvetica Neue',
				}
			},
			  scales: 
			  {
				  xAxes: 
				[{
					ticks: 
					{
						display: false
					},
					gridLines: 
					{
						display:false
					}
				}],
				  yAxes: 
				[{
					gridLines: 
					{
						display:true
					}   
				}]
			}
		},
		  data: {
			labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
			datasets: [
			  { label: label,
				data: dataChart,
				borderColor: '1C4E80',
                backgroundColor: '#7E909A',
				cubicInterpolationMode:'monotone',
				lineTension:'0'
			  } 
			]
		  }
		});
		return chartName;
}
