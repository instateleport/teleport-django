
// Bar

(function(d){


	let strip = $('.bar .strip'),
		sec = $('.bar .sec'),
		min = $('.bar .min'),
		sec_val,
		min_val,
		time;

	let page_slug = $('input[name=page_slug]').val(),
	    page_options = JSON.parse(localStorage.getItem(`page_${page_slug}_timer`)),
		timer_time;

	if (page_options) {
	    timer_time = page_options.timer_time;
	}

	if (timer_time) {
		sec_val = timer_time;
	} else {
		sec_val = $('input[name=timer_time]').attr('value');
	}
	min_val = Math.floor(sec_val / 60) + ' : ' + sec_val % 60;
	sec.html(sec_val);
	min.text(min_val);

	let display = d.querySelector('.bar .sec'),
		timeLeft = parseInt(display.innerHTML);

	setInterval(function(){
	if (--timeLeft >= 0) {

		if ((timeLeft % 60) < 10) {
			time = Math.floor(timeLeft / 60) + ' : ' + '0' + timeLeft % 60;
		} else {
			time = Math.floor(timeLeft / 60) + ' : ' + timeLeft % 60;
		}
		let	a = sec_val - timeLeft,
			b = sec_val - a,
			c = sec_val * .01,
			d = b / c + '%',
			e = 'calc(' + d + ' - 8px)';

		localStorage.setItem(`page_${page_slug}_timer`, JSON.stringify({timer_time: timeLeft}));
		min.text(time);
		strip.css('width', e);
	} else {
			// по истичению таймера
	}
  }, 1000)
})(document);

$(document).ready(function() {
	let w = $(window).width(),
		barText = $('input[name=barText]');

	if (w <= 600) {
		$('.bar .text').text(barText.val());
	}
});

$(function() {
	let e = $('.bar');

	$('.subscript_buttons .subscript_button').hover( function() {
		e.toggleClass('ml');
	});
	$('.subscript_input').hover( function() {
		e.toggleClass('mr');
	})
});