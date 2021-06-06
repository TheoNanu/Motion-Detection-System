function Box(boxName,id1, minValue, maxValue)
{
	var box = document.getElementById(boxName);
	
	box.oninput = function()
	{
		if(this.value <= maxValue && this.value >= minValue)
		{
			ws.send(id1+this.value);
		}
	
	}
}
function tieBox(boxName, sliderName, id1, minValue, maxValue)
{
	var slider = document.getElementById(sliderName);
	var box = document.getElementById(boxName);
	box.value = slider.value;
	
	slider.oninput = function() 
	{
		box.value = this.value;
		if(this.value <= maxValue && this.value >= minValue)
		{
			ws.send(id1+this.value);
		}
	}
	box.oninput = function()
	{
		slider.value = this.value;
		if(this.value <= maxValue && this.value >= minValue)
		{
			ws.send(id1+this.value);
		}
	
	}
}