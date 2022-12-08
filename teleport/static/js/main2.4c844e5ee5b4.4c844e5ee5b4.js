$(document).ready(() => {

	var a = 'active';

	// functions
	let // domain
        domainDeleteAjax = async (data, CSRFToken) =>
			await $.ajax({
				method: 'post',
				url: '/domains/delete/',
				headers: {'X-CSRFToken': CSRFToken},
				data
			}),

        // folder
        folderCreateAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: '/folders/create/',
                headers: {'X-CSRFToken': CSRFToken},
                data
            }),
		folderDeleteAjax = async (data, CSRFToken) =>
			await $.ajax({
				method: 'post',
				url: '/folders/delete/',
				headers: {'X-CSRFToken': CSRFToken},
				data,
			}),

        // page
        pageListAjax = async (data) =>
            await $.ajax({
                method: 'get',
                url: '/subscribe-pages/list/',
                data
            }),
		pageDeleteAjax = async (data, CSRFToken) =>
			await $.ajax({
				method: 'post',
				url: '/subscribe-page/delete/',
				headers: {'X-CSRFToken': CSRFToken},
				data,
			}),

        // partner
        channelCreateAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: '/partner/channel/create/',
                headers: {'X-CSRFToken': CSRFToken},
                data
            }),
        channelDeleteAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: '/partner/channel/delete/',
                headers: {'X-CSRFToken': CSRFToken},
                data
            }),
        channelEditAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: '/partner/channel/edit/',
                headers: {'X-CSRFToken': CSRFToken},
                data
            }),
        payoutCreateAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: '/partner/payout/create/',
                headers: {'X-CSRFToken': CSRFToken},
                data,
                processData: false,
                contentType: false,
            }),

        // modal
		modalAction = (modalSelector, action) => {
			let modal = $(modalSelector),
				body = $('body');

			switch (action) {
				case 'show':
					modal.addClass('active');
					body.css('overflow', 'hidden');
					break;
				case 'hide':
					modal.removeClass('active');
					body.css('overflow', 'scroll');
					break;
			}
		};

	// Hover nav

	if ($('.header_nav').length) {
		$('.header_nav').hoverSlippery({
			border: true,
			underline: true,
			speed: 430,
			borderColor: 'var(--blue)',
			borderWidth: '2px'
		})
	};


	// Nav scroll active

	if ($('.header_nav').length) {
		var lastId,
			h = $('.header').outerHeight(),
			topMenu = $('.header_nav .nav'),
			topMenuHeight = topMenu.outerHeight(),
			menuItems = topMenu.find('a'),
			scrollItems = menuItems.map(function(){
				var item = $($(this).attr('href'));
				if (item.length) {
					return item;
				}
			});

			menuItems.click(function(e){
				var 	href = $(this).attr('href'),
					offsetTop = href === '#' ? 0 : $(href).offset().top-topMenuHeight - h;
				$('html, body').stop().animate({
					scrollTop: offsetTop
				}, 1000);
				e.preventDefault();
			});

		$(window).scroll(function(){
			var fromTop = $(this).scrollTop()+topMenuHeight + h + 1;
			var cur = scrollItems.map(function(){
				if ($(this).offset().top < fromTop)
				return this;
			});
			cur = cur[cur.length-1];
			var id = cur && cur.length ? cur[0].id : "";

			if (lastId !== id) {
				lastId = id;
				menuItems.parent().removeClass(a).end().filter("[href='#"+id+"']").parent().addClass(a);

				var aHref = menuItems.parent().end().filter("[href='#"+id+"']"),
					par = aHref.parent(),
					width = par.width() / 3 * 2,
					left = aHref.position().left + par.width() / 3 / 2;

				$('.slippery').attr('heir__left', left).attr('heir__width', width).stop().animate({
					left: left,
					width: width
				}, 300);
			}
		});
	}



	// Header fixed

	fixed_nav();
	$(window).scroll(function () {
		fixed_nav()
	});

	function fixed_nav() {
		var e = $('.header'),
			h = $('.header').outerHeight() + 40,
			a = $(window).scrollTop(),
			r = $('.main').attr('data-inner');
			m = $('.main').height() - r;

		if (a >= m) {
			e.addClass('fixed');
		} else {
			e.removeClass('fixed');
		}

		if (a >= h) {
			e.addClass('invisible');
		} else {
			e.removeClass('invisible');
		}
	}



	// Slider

    if ($('.example_items.twoo__slide').length) {
        $('.example_items.twoo__slide').slick({
            arrows: true,
            dots: false,
            infinite: false,
            slidesToShow: 2,
            responsive: [
                {
                    breakpoint: 1100,
                    settings: {
                        slidesToShow: 1
                    }
                }
            ]
        });
    };

    if ($('.example_items.one__slid').length) {
        $('.example_items.one__slid').slick({
            arrows: true,
            dots: false,
            infinite: false,
            slidesToShow: 1,
            slidesToScroll: 1
        });
    };

    if ($('.content_slider').length) {
        var w = $('.content_inner').width() / 200,
            nth = Math.floor(w) - 1,
            e = $('.content_slid:eq(' + nth + ')');

        if (nth >= 1) {
            e.addClass('last');
        }

        $('.content_slider').slick({
            arrows: true,
            dots: false,
            infinite: false,
            slidesToShow: w
        });
    };

    $('.content_slider').on('beforeChange', function (event, slick, currentSlide, nextSlide) {
        if (Math.abs(nextSlide - currentSlide) == 1) {
            direction = (nextSlide - currentSlide > 0) ? 1 : 0;
        }
        else {
            direction = (nextSlide - currentSlide > 0) ? 0 : 1;
        }

        if (direction == 1) {
            $('.content_slid').removeClass('last');
            $('.content_slid.slick-active:last').next().addClass('last');
        } else {
            $('.content_slid').removeClass('last');
            $('.content_slid.slick-active:last').prev().addClass('last');
        }
    });



	// Dropdown

	$(document).on('click', '.droprown_item',function () {
		var e = $(this),
			info = e.find('.droprown_item_info');

		if (e.hasClass(a)) {
			close_faq();

			e.removeClass(a);
			info.slideUp();
		} else {
			close_faq();

			e.addClass(a);
			info.slideDown();
		}

		function close_faq() {
			$('.droprown_item').removeClass(a);
			$('.droprown_item .droprown_item_info').slideUp();
		}
	});


	// Animation to scroll

	let animItems = document.querySelectorAll('.anim');

	if (animItems.length > 0) {
		window.addEventListener('scroll', animOnScroll);
		function animOnScroll() {
			for (let index = 0; index < animItems.length; index++) {
				const animItem = animItems[index];
				const animItemHeight = animItem.offsetHeight;
				const animItemOffset = offset(animItem).top;
				const animStart = 4;

				let animItemPoint = window.innerHeight - animItemHeight + 100;
				if (animItemHeight > window.innerHeight) {
					animItemPoint = window.innerHeight - window.innerHeight / animStart;
				}
				if (animItem.classList.contains('anim_wis')) {
					animItemPoint = animItemOffset - window.innerHeight + 100;

					if (pageYOffset > animItemPoint) {
						animItem.classList.add('anim_act');
						setTimeout(function() {
							if (animItem.classList.contains('anim__hover')) {
								animItem.classList.add('anim_act__hover')
							}
						}, 2000);
					}
				} else {
					if ((pageYOffset > animItemOffset - animItemPoint) && pageYOffset < (animItemOffset + animItemHeight)) {
						animItem.classList.add('anim_act');
						setTimeout(function() {
							if (animItem.classList.contains('anim__hover')) {
								animItem.classList.add('anim_act__hover')
							}
						}, 2000);
					}
				}
			}
		}

		function offset(el) {
			const rect = el.getBoundingClientRect(),
				scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
				scrollTop = window.pageXOffset || document.documentElement.scrollTop;
			return {top: rect.top + scrollTop, left: rect.left + scrollLeft}
		}

		setTimeout(() => {
			animOnScroll();
		}, 300);

	};



	// Cabinet theme
    let theme = $('.theme');
    if (theme.hasClass('white')) {
        $('.nav__theme p').text('Темная тема');
    }

    $(document).on('click', '.nav__theme', function () {
        $('.lever, .theme').toggleClass('white');

        if (theme.hasClass('white')) {
            $('.nav__theme p').text('Темная тема');
        } else {
            $('.nav__theme p').text('Светлая тема');
        }
    });



	// Select


    var i = $('.select_info, .select__info');

    i.on('click',function () {
        var i = $(this),
            p = i.parent(),
            o = p.find('.select_wrapper, .select__wrapper').find('.select_opt, .lang_opt');

        if (p.hasClass(a)) {
            $('.select_info').parent().removeClass(a);

            p.removeClass(a);
        } else {
            $('.select_info').parent().removeClass(a);

            p.addClass(a);
        }

        p.mousedown('click',function () {
            event.stopPropagation();
        })

        o.on('click',function () {
            var e = $(this);
                t = e.html();

            p.removeClass(a);
            i.html(t);
            o.removeClass(a);
            e.addClass(a);

            if (i.hasClass('select__payment')) {
                var data = e.data('payment'),
                    input = $('.input__payment input'),
                    paymentTypeInput = $('input[name=payment_type]');

                $('.input__payment').slideDown();

                paymentTypeInput.val(data);

                if (data === 'qiwi') {
                    input.inputmask('phone');
                }

                if (data === 'card') {
                    input.inputmask('#### #### #### ####');
                }

                if (data === 'yoomoney') {
                    input.inputmask('###################');
                }
            }
        })

        $('html').mousedown('click',function (event) {
            if (p.hasClass(a)) {
                p.removeClass(a);
            }
        });
    });



	// Modal


    let modal = $('.modal'),
        modalSelector;

    $(document).on('click', '.dtn__modal', function () {
        let dataModal = $(this).data('modal');
        modalSelector = '.modal_' + dataModal;

        modalAction(modalSelector, 'show');

		if (dataModal === 'folder') {
        	let folderID = $(this).data('element-id'),
				folderIDInput = $('#folderRenameForm input[name="id"]');
        	folderIDInput.val(folderID)
		}

    });

    $('.modal_wrapper').mousedown(function () {
        let select = $('.select');
        event.stopPropagation();

        if (select.hasClass(a)) {
            select.removeClass(a);
        }
    });

    $('html, .modal_close, .btn__close').mousedown(function (event) {
        if (modal.hasClass('active')) {
            if (modal.hasClass('modal_ok')) {
                $(location).attr('href', '/subscribe-pages');
            }

            modalAction(modalSelector, 'hide');
            $('html').removeClass('hidden');
        }
    });

    // Partner

    let channelCreateForm = $('#channelCreate');
    if (channelCreateForm.length) {
        $(channelCreateForm).submit(async function (e) {
            let form = $(this),
                channelName = channelCreateForm.find('input[name=name]'),
                CSRFToken = channelCreateForm.find('input[name=csrfmiddlewaretoken]'),
                channelTable = $('#channelTable table'),
				response,
                channel;

            e.preventDefault();

            response = await channelCreateAjax({name: channelName.val()}, CSRFToken.val());
            if (response.status === 'SUCCESS') {
                channel = response.data;
                channelTable.append(`
                    <tr class="delete__e">
                        <td>${ channel.name }</td>
                        <td>https://instateleport.ru/?r=${ channel.url }</td>
                        <td class="icon">
                            <svg width="24" height="24" viewbox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path class="stroke" d="M10.1968 12.906C10.5859 13.4262 11.0823 13.8566 11.6523 14.1681C12.2224 14.4795 12.8528 14.6647 13.5007 14.7111C14.1486 14.7575 14.799 14.664 15.4076 14.437C16.0162 14.21 16.5689 13.8547 17.0282 13.3953L19.7462 10.6772C20.5714 9.82282 21.028 8.67851 21.0177 7.49073C21.0074 6.30296 20.531 5.16675 19.691 4.32684C18.8511 3.48692 17.7149 3.01049 16.5271 3.00017C15.3394 2.98985 14.1951 3.44646 13.3407 4.27165L11.7823 5.82095" stroke="#94B3E2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path class="stroke" d="M13.8211 11.094C13.432 10.5738 12.9356 10.1434 12.3655 9.83198C11.7955 9.52053 11.1651 9.33532 10.5172 9.28892C9.86923 9.24251 9.21889 9.336 8.61027 9.56304C8.00164 9.79007 7.44896 10.1453 6.98971 10.6048L4.27165 13.3228C3.44646 14.1772 2.98985 15.3215 3.00017 16.5093C3.01049 17.6971 3.48692 18.8333 4.32684 19.6732C5.16675 20.5131 6.30296 20.9895 7.49073 20.9999C8.67851 21.0102 9.82282 20.5536 10.6772 19.7284L12.2265 18.1791" stroke="#94B3E2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                            <!--<svg width="24" height="24" viewbox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">-->
                                <!--<path class="fill stroke" d="M18.9331 3.72457C17.9654 2.75848 16.3983 2.75848 15.4306 3.72457L14.5538 4.60621L5.22087 13.9351L5.20103 13.9551C5.19623 13.9599 5.19623 13.965 5.19111 13.965C5.1812 13.9799 5.16632 13.9946 5.15656 14.0095C5.15656 14.0144 5.15144 14.0144 5.15144 14.0194C5.14153 14.0343 5.13672 14.0442 5.12665 14.0591C5.12185 14.064 5.12185 14.0688 5.11689 14.074C5.11193 14.0888 5.10697 14.0988 5.10186 14.1136C5.10186 14.1184 5.09705 14.1184 5.09705 14.1236L3.02635 20.351C2.96561 20.5283 3.01179 20.7246 3.1452 20.8562C3.23895 20.9487 3.3654 21.0005 3.49696 21C3.55073 20.9991 3.60403 20.9907 3.65548 20.9752L9.87751 18.8993C9.88231 18.8993 9.88231 18.8993 9.88742 18.8945C9.90308 18.8899 9.91811 18.8832 9.9319 18.8745C9.93577 18.8741 9.93918 18.8724 9.94197 18.8697C9.95669 18.8598 9.97653 18.8498 9.9914 18.8398C10.0061 18.8301 10.0212 18.8152 10.036 18.8053C10.041 18.8002 10.0458 18.8002 10.0458 18.7954C10.0509 18.7904 10.0608 18.7856 10.0658 18.7755L20.2755 8.56484C21.2415 7.59703 21.2415 6.02979 20.2755 5.06214L18.9331 3.72457ZM9.71899 17.735L6.27117 14.287L14.9006 5.65677L18.3484 9.10476L9.71899 17.735ZM5.78553 15.2036L8.79761 18.2158L4.27469 19.7218L5.78553 15.2036ZM19.5771 7.87118L19.0519 8.40134L15.604 4.95304L16.1342 4.42304C16.7143 3.84344 17.6544 3.84344 18.2345 4.42304L19.5819 5.77052C20.1576 6.35322 20.1554 7.29127 19.5771 7.87118Z" fill="#94B3E2" stroke="#94B3E2" stroke-width="0.5"/>-->
                            <!--</svg>-->
                            <svg class="dtn__modal delete__btn" data-modal="delete_channel" width="24" height="24" viewbox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path class="fill stroke" d="M17.8496 8.0876H6.1502C6.02362 8.07684 5.8982 8.11867 5.80336 8.20319C5.71012 8.29277 5.66692 8.42244 5.68777 8.55003L6.89006 19.024C7.03106 20.1788 8.01575 21.0441 9.17906 21.0355H15.0056C16.2017 21.0526 17.2092 20.1458 17.3178 18.9546L18.312 8.50378C18.3181 8.39168 18.2761 8.28228 18.1964 8.20319C18.1016 8.11867 17.9762 8.07684 17.8496 8.0876ZM16.393 18.9084C16.3203 19.6125 15.7129 20.1388 15.0057 20.1107H9.1791C8.48455 20.1389 7.88754 19.6228 7.81492 18.9315L6.65887 9.01245H17.3409L16.393 18.9084Z" fill="#94B3E2" stroke="#94B3E2" stroke-width="0.5"/>
                                <path class="fill stroke" d="M19.5376 5.08118H14.7745V4.34126C14.8002 3.62662 14.2417 3.02651 13.5271 3.00085C13.5036 3 13.4801 2.99978 13.4567 3.00023H10.5433C9.82835 2.98699 9.23807 3.55586 9.22483 4.27085C9.22439 4.29431 9.22461 4.31781 9.22545 4.34126V5.08113H4.46243C4.20703 5.08113 4 5.28816 4 5.54356C4 5.79896 4.20703 6.00599 4.46243 6.00599H19.5376C19.793 6.00599 20 5.79896 20 5.54356C20 5.28816 19.7929 5.08118 19.5376 5.08118ZM13.8497 4.34126V5.08113H10.1503V4.34126C10.1242 4.13862 10.2674 3.95323 10.47 3.92716C10.4943 3.92402 10.5189 3.92336 10.5433 3.92508H13.4566C13.6604 3.91066 13.8373 4.06413 13.8518 4.26798C13.8535 4.29241 13.8528 4.31697 13.8497 4.34126Z" fill="#94B3E2" stroke="#94B3E2" stroke-width="0.5"/>
                            </svg>
                        </td>
                    </tr>
                `);
                channelName.val('');
                modalAction('.modal_channel', 'hide')
            }
        })
    }

    $('#modalPayout form').on('submit', async function (e) {
        let data = new FormData($(this)[0]),
            paymentAddress = data.get('payment_address'),
            paymentAddressInput = $('input[name=payment_address]'),
            CSRFToken = $('input[name=csrfmiddlewaretoken]').val();

        e.preventDefault();

        if (paymentAddress.indexOf('_') !== -1) {
            paymentAddressInput.addClass('error');
            paymentAddressInput.next('.input_err').text('Введите валидный номер');
            return
        }

        let response = await payoutCreateAjax(data, CSRFToken);
        console.log(response);

        if (response.status === 'SUCCESS') {
            let payout = response.data;

            $('#modalPayout').removeClass('active');
            $('.slide_big_block_number').find('span').text(response.data.balance + ' ');

            if (response.data.balance >= 500) {
                $('.available_amount').find('span').text('Доступно для вывода: ' + response.data.balance + ' ₽')
            } else {
                $('.available_amount').find('span').text('Доступно для вывода: 0 ₽')
            }

            $('#payoutCreated').addClass('active');
            setTimeout(() => {
                $('#payoutCreated').removeClass('active')
            }, 3000)

            $('#payoutTable').append(`
                <tr>
                    <td>${ payout.created_date }</td>
                    <td>${ payout.amount } ₽</td>
                    <td>
                        ${ payout.payment_type }
                        <br/>{{ payout.payment_address }}
                    </td>
                    <td class="orange">В обработке</td>
                </tr>
            `)


        } else if (response.status === 'FAIL') {
            if (response.reason === 'FORM_ERROR') {
                for (let error in response.errors) {
                    if (error === 'payment_type') {
                        $(`#modalPayout .modal_select_info`).addClass('error').next('.input_err').text(response.errors[error])
                    } else {
                        $(`#modalPayout input[name=${error}]`).addClass('error').next('.input_err').text(response.errors[error]);
                    }
                }
            }
        }
    });


	// Calendar

    if ($('input[name="daterange"]').length) {
        var date = new Date();
            date.setDate(date.getDate() - 7);

            moment.lang('zh-cn', {
                week : {
                    dow : 1 // Monday is the first day of the week
                }
            });

            var date = moment().weekday(0); // date now is the first day of the week, (i.e., Monday)

        $('input[name="daterange"]').daterangepicker({
            opens: 'right',
            startDate: date,
            // showDropdowns: true,
            minYear: 2008,
            showCustomRangeLabel: false,
            cancelButtonClasses: 'btn-outline',
            applyButtonClasses: 'btn-red',
            // maxYear: parseInt(moment().add(1, 'years').format('YYYY')),
             ranges: {
                'День': [moment(), moment()],
                'Неделя': [moment().subtract(6, 'days'), moment()],
                'Месяц': [moment().startOf('month'), moment().endOf('month')],
                'Последние 6 месяцев': [moment().subtract(6, 'month'), moment()],
                'Прошедший год': [moment().startOf('years'), moment().endOf('years')],
            }
        });
    }



	// Messages
	let messages = $('.message');
	if (messages.length) {
		setTimeout(() => messages.addClass('active'), 500);
		setTimeout(() => messages.removeClass('active'), 3000)
	}


	// Navigation slid

	$('.content_nav_li').on('click', function () {
		var e = $(this);

		if (!e.hasClass(a)) {
			var id = e.attr('id');

			$('.content__li').slideUp();
			$('.content_li-' + id).slideDown();
			$('.content_nav_li').removeClass(a);
			e.addClass(a);
		}
	})



	// Input type="password"

	$('.input__password span.icon').on('click', function () {
		var input = $(this).parent().find('input');

		if (input.attr('type') === 'password') {
			input.attr('type', 'text');
		} else {
			input.attr('type', 'password');
		}
	});









	// Проверка фона

	$('.images__wrapper .images img').each(function() {
		if (this.src.length > 0) {
			$('.images__wrapper').addClass('active');
		}
	});

	// Замена на выбраное изображениe

	function readURL_ava(t, a, b) {
		let e;
		t.files && t.files[0] && ((e = new FileReader).onload = function(e) {
			a.addClass('active'),
			b.attr('src', e.target.result),
			b.attr('style', '')
		}, e.readAsDataURL(t.files[0]))
	}

	$('.images__wrapper .input__hidden').change(function() {
		var a = $(this).parents('.images__wrapper'),
			b = a.find('.images').find('img')

		readURL_ava(this, a, b);
	})

	// удаление фона

	$('.images__close').on('click', function () {
		var img = $(this).parent().find('.images img'),
			input = $(this).parent().find('input');

		$(img).attr('src', '');
		input.removeClass('error').val('');
		$('.images__wrapper').removeClass('active');
	})



	// Step

	$('.next__step, .prev__step').on('click', function () {
		var step = $(this).parents('.content_form_step').attr('id'),
			stepClass = '.' + step,
			stepId = '#' + step,
			input = $(stepId).find('.required__field input'),
			b = 1,
			posTop = 0;

		if ($('input[name=typePage]:checked').attr('id') === 'typePage-1') {
			$(stepId).find('.required__field').parent().find('input').each(function () {
				var val = $(this).val();

				if (val.length === 0) {
					b = 0;
					posTop = $(this).offset().top - 100;
					$(this).addClass('error');

					return false;
				}
			})

			if (b == 1) {
				if ($(this).hasClass('next__step')) {
					$('.content_step_li').removeClass('open');
					$(stepId).slideUp(1000);
					$('#step-5').slideDown(1000);
					$(stepClass).addClass('past').next().addClass('active open');
				}
			}

			if ($(this).hasClass('prev__step')) {
				$('.content_step_li').removeClass('open');
				$(stepId).slideUp(1000)
				$('#step-1').slideDown(1000);
				$(stepClass).removeClass(a).prev().removeClass('past').addClass('open');
			}
		} else {
			$(stepId).find('.required__field').parent().find('input').each(function () {
				var val = $(this).val();

				if (val.length === 0) {
					b = 0;
					posTop = $(this).offset().top - 100;
					$(this).addClass('error');

					return false;
				}
			})

			if (b == 1) {
				if ($(this).hasClass('next__step')) {
					$('.content_step_li').removeClass('open');
					$(stepId).slideUp(1000).next().slideDown(1000);
					$(stepClass).addClass('past').next().addClass('active open');
				}
			}

			if ($(this).hasClass('prev__step')) {
				$('.content_step_li').removeClass('open');
				$(stepId).slideUp(1000).prev().slideDown(1000);
				$(stepClass).removeClass(a).prev().removeClass('past').addClass('open');
			}
		}

		$('html, body').animate({
			scrollTop: posTop
		}, 1000);
	});

	$('.dooble .content_step_li').on('click', function () {
		var e = $(this);

		if (!$(this).hasClass('open')) {
			var step = $(this).attr('data-id'),
				stepId = '#' + step,
				stepActive = $('.content_step_li.open').attr('data-id'),
				stepActiveId = '#' + stepActive,
				b = 1,
				posTop = 0;

			if (e.hasClass('past')) {
				$('.content_step_li').removeClass('open');
				$('.content_form_step').slideUp(1000);
				$(stepId).slideDown(1000);

				e.prevAll().addClass('active past');
				e.addClass('active open').removeClass('past');
				e.nextAll().removeClass('active past');
			} else {
				$(stepActiveId).find('.required__field').parent().find('input').each(function () {
					var val = $(this).val();

					if (val.length === 0) {
						b = 0;
						posTop = $(this).offset().top - 100;
						$(this).addClass('error');

						return false;
					}
				})

				if (b == 1) {
					if (!e.hasClass(a)) {
						$('.content_step_li').removeClass('open');
						$('.content_form_step').slideUp(1000);
						$(stepId).slideDown(1000);

						e.prevAll().addClass('active past');
						e.addClass('active open');
						e.nextAll().removeClass('active past');
					}
				}
			}

		}

		$('html, body').animate({
			scrollTop: posTop
		}, 1000);
	});

	$('input[name=typePage]').on('click', function () {
		var e = $(this);

		if (e.attr('checked') != 'checked') {
			$('input[name=typePage]').attr('checked', false)
			e.attr('checked', true);

			if (e.attr('id') === 'typePage-1') {
				$('.content_step_li.step-2').nextAll().hide();
				$('.content_step_li.step-2 .content_step_top span').hide();
			} else {
				$('.content_step_li.step-2').nextAll().show();
				$('.content_step_li.step-2 .content_step_top span').show();
			}
		}
	})



	// Lever

	$('.lever__wrapper').on('click', function () {
		var e = $(this),
			inner = '.' + e.attr('id');
		console.log(2);

		e.toggleClass(a);
		$(inner).slideToggle()
	});



	// Copied

	$(document).on('click', '.copy__href', function () {
		let e = $(this),
			f = $('<input>'),
            op,
            id_;

		if (e.hasClass('modal_ok_btn')) {
			op = '.modal_ok .page_link';
		} else if (e.hasClass('partner_copy')) {
		    op = '.partner_link';
        } else {
		    id_ = e.attr('id').match(/\d+$/) - 0;
			op = '#page_open-' + id_;
		}

		$('body').append(f);
		f.val($(op).attr('href')).select();
		document.execCommand('copy');
		f.remove();

		$('.copy__href').addClass('active');
		setTimeout(() => {
			$('.copy__href').removeClass('active');
		}, 1000);
	});


	$(document).on('click', '.copy__href_modal', function () {
		$('.copy__href').addClass('active');
		setTimeout(() => {
			$('.copy__href').removeClass('active');
		}, 1000);
	})



	// Media

	media();
	$(window).resize(media);

	function media() {
		var w = $(window).width(),
			h = $(window).height();

		if (w <= 1200) {
			$('.main').attr('data-inner', 120);
		} else {
			$('.main').attr('data-inner', 172);
		}

		if (w <= 1100 || h <= 800) {
			$('.prev_wrapper').addClass('small');

			$('.prev_window').removeClass('scale');
			$('.prev_button').removeClass(a);

			$('.prev_wrapper').animate( {
				width: 455,
				height: 440
			}, 20)
		} else {
			$('.prev_wrapper').removeClass('small');

			if ($('#prev-scale').hasClass(a)) {
				$('.prev_wrapper').animate( {
					height: 637
				}, 20)
			} else {
				$('.prev_wrapper').animate( {
					height: 538
				}, 20)
			}
		}

		if (w <= 600) {
			$('#lang-desktop > *').detach().prependTo('#lang-mobile');
			$('#user-desktop > *').detach().prependTo('#user-mobile');
			$('.statistik_chart_li canvas').attr('width', 320).attr('height', 488);
		} else {
			$('#lang-mobile > *').detach().prependTo('#lang-desktop');
			$('#user-mobile > *').detach().prependTo('#user-desktop');
			$('.statistik_chart_li canvas').attr('width', 1028).attr('height', 618)
		}

		if (w <= 480 || h <= 600) {
			$('.prev_wrapper').animate( {
				width: 280,
				height: 300
			}, 20)
		}

	};


	// function animateTo() {
	// 	$('.advantage_item').animate({
	// 		'left': '100%',
	// 		'transform': 'translate3d(-100%, 0, 0)'
	// 	}, 4000, 'linear');
	// }

	// function animateFrom() {
	// 	$('.advantage_item').animate({
	// 		'left': '0',
	// 		'transform': 'translate3d(0, 0, 0)'
	// 	}, 4000, 'linear', function () {
	// 		animateTo();
	// 	});
	// }

    var w = $(window).width();

    if (w < 1000) {
        var ww = $('.advantage_items').width();
            aw = $('.advantage_item').outerWidth();

        function animateEven() {
            $('.advantage_item:even').animate({
                left: ww - aw,
            }, 4000, 'linear');
            $('.advantage_item:even').animate({
                left: 0,
            }, 4000, 'linear', function () {
                animateEven();
            });
        }

        function animateOdd() {
            $('.advantage_item:odd').animate({
                left: 0,
            }, 4000, 'linear');
            $('.advantage_item:odd').animate({
                left: ww - aw,
            }, 4000, 'linear', function () {
                animateOdd();
            });
        }

        animateOdd();
        animateEven();
    }



	// Index Burger

	$('.header_bar_burger, .header_bar_wrapper .header_nav_li a').on('click', function () {
		$('.header_bar_burger').toggleClass(a);
		$('.header').toggleClass('bar__inactive');
		$('html').toggleClass('hidden');

		// setTimeout(function() {
			$('.header_bar_wrapper').slideToggle();
		// }, 10);
	});



	// Bar

	$('.content_burger').on('click', function () {
		$(this).toggleClass(a);
		$('.bar').toggleClass(a);
		$('html').toggleClass('hidden');
	});

	$('.bar_viel').mousedown('click', function () {
		$('.bar, .content_burger').removeClass(a);
		$('html').removeClass('hidden');
	})











	// preview

	function prevStop() {
		$('.prev_button').addClass('stop');
		setTimeout(function() {
			$('.prev_button').removeClass('stop');
		}, 800);
	}


	$('.prev_media_button').on('click', function () {
		$(this).toggleClass('active');
		$('.prev_wrapper').slideToggle(830);

		// if ($(this).hasClass('active')) {
		// 	var toogle = 'show';
		// } else {
		// 	var toogle = 'hide';
		// }

		// $('.prev_wrapper').animate( {
	 //        width: toogle,
	 //        marginLeft: toogle,
	 //        marginRight: toogle
	 //    }, 830)

	});

	$('#prev-scale').on('click', function () {
		var e = $(this);

		if (!e.hasClass('stop')) {
			prevStop();
			e.toggleClass(a)

			if (e.hasClass(a)) {
				var w = 1026,
					h = 637;
			} else {
				var w = 455,
					h = 538;
			}

			$('.prev_wrapper').animate( {
				width: w,
				height: h
			}, 0, 'linear');

			$('.prev_window').toggleClass('scale');
		}

		$('.prev_wrapper').addClass('trs');

		setTimeout(function() {
			$('.prev_wrapper').removeClass('trs');
		}, 830);
	});

	$('.prev__device').on('click', function () {
		var e = $(this);
			id = e.attr('data-id');

		if (!e.hasClass('stop') && !e.hasClass(a)) {
			prevStop();

			$('.prev__device').removeClass(a);
			e.addClass(a);

			if (id === 'desktop') {
				var w = 1440,
					h = 772;

				$('.prev_window').removeClass('mobile');
			} else {
				var w = 375,
					h = 667;

				$('.prev_window').addClass('mobile');
			}

			$('.prev_window').animate( {
				width: w,
				'min-width': w,
				height: h,
				'min-height': h
			}, 830, 'linear');
		}

	})



	// No error

	$('input').on('keydown', function () {
		let input = $(this);

		if (input.hasClass('error')) {
			input.removeClass('error');
		}
	});




	// Scroll to

	function scroll_to(e) {
		if ($(e).length != 0) {
			$('html, body').animate({
				scrollTop: $(e).offset().top - 88
			}, 1000);
		}
	}





	// Emoji

    // if ($('.emoj').length) {
    //     $('.emoj').emojiPicker({
    //         onShow: function () {
    //             $('head').append('<link rel="stylesheet" type="text/css" href="styles/jquery.emojipicker.a.css">');
    //         }
    //     });
    // }

    // Create
    // $(document).on('click', '#createFolderModal .create__btn', async function () {
    //     let folderName = $('#createFolderModal input[name=name]').val(),
		// 	folderList= $('#folderList'),
    //         CSRFToken = $('input[name=csrfmiddlewaretoken]').val(),
    //         response = await folderCreateAjax({name: folderName}, CSRFToken),
		// 	folder;
    //
    //     if (response.status === 'SUCCESS') {
    //         // прописать добавление папки
		// 	folder = response.folder;
    //
		// 	folderList.append(
		// 		`
		// 		<div class="content_slid delete__e">
		// 			<a href="/subscribe-pages/${folder.name}" class="folder" data-element-id="${folder.id}">
		// 				<div class="folder_top flex__start">
		// 					<div class="folder_file">${ folder.subscribe_pages_count }</div>
		// 					<div class="folder_more">
		// 						<div class="more">
		// 							<div class="more_dots">
		// 								<span></span>
		// 								<span></span>
		// 								<span></span>
		// 							</div>
		// 							<div class="more_wrapper">
		// 								<div class="more_scroll">
		// 									<div class="more_opt icon icon-pencil dtn__modal" data-modal="folder" data-element-id="${folder.id}">Редактировать папку</div>
		// 									<div class="more_opt icon icon-del dtn__modal delete__btn" data-modal="delete_folder" data-element-id="${folder.id}">Удалить папку</div>
		// 								</div>
		// 							</div>
		// 						</div>
		// 					</div>
		// 				</div>
		// 				<div class="folder_icon icon icon-file"></div>
		// 				<div class="folder_name">${folder.name}</div>
		// 			</a>
		// 		</div>
		// 		`
		// 	)
    //         modalAction('new_folder', 'hide')
    //     } else if (response.status === 'ERROR') {
    //         for (let error in response.errors) {
    //             $(`#createFolderModal  input[name=${error}]`).addClass('error').next('.input_err').text(response.errors[error])
    //         }
    //     }
    // });

    // Folder
	$(document).on('click', '.folder', async function (e) {
		let folder = $(this);
		console.log(this)
		// e.preventDefault()
		if (folder.hasClass('selected')) {
			e.preventDefault()
		}

        // if (!folder.hasClass('selected')) {
		 //    let folderID = folder.data('element-id'),
        //         selectedFolder = $('.folder.selected'),
        //         pages = $('#pages');
        //
		 //    selectedFolder.removeClass('selected');
		 //    pages.empty();
		 //    folder.addClass('selected');
        //
        //     let folderPages = await pageListAjax({folderID});
        //     console.log(folderPages);
        //     pageListPaste(pages, folderPages['pageList'])
        //
        // }
    });

	$(document).on('click', '#moveFolderButton', async function (e) {

		// let folderID =
    });

	// Delete

	let forDelete;

	$(document).on('click', '.delete__btn', function () {
		forDelete = $(this).parents('.delete__e');
		let typeOfDelete = $(this).data('modal'),
			modalSelector = '.modal_' + typeOfDelete,
			elementID = $(this).data('element-id'),
			CSRFToken = $('input[name=csrfmiddlewaretoken]').val();
        console.log(typeOfDelete)

		$('.delete').on('click', async function () {
			switch (typeOfDelete) {
				case 'delete_domain':
					await domainDeleteAjax(
						{
							'domainID': elementID
						}, CSRFToken
					);
					break;
				case 'delete_folder':
					await folderDeleteAjax(
						{
							'folderID': elementID
						}, CSRFToken
					);
					break;
				case 'delete_page':
					await pageDeleteAjax(
						{
							'pageID': elementID
						}, CSRFToken
					);
					break;
                case 'delete_channel':
                    await channelDeleteAjax(
                        {
                            'channelID': elementID
                        }, CSRFToken
                    );
                    break;
			}
			forDelete.remove();

			modalAction(modalSelector, 'hide')
		})
	});
});