var a = 'active';

    // Prew
    $(document).ready(function () {
        if ($('.prev').length) {
            prev_page(false, false, $('#typePage-2'))
        }
    });

    function prev_page(e, id_, typePage2) {
        let timer = false,
            img = false;

        if (!id_) {
            id_ = $('.prev_page.active').text();
        }

        if (e && !$(e).hasClass(a)) {
            $('.prev_page').removeClass(a);
            $(e).addClass(a);
        }

        if (!typePage2) {
            typePage2 = $('#typePage-2')
        }

        if (typePage2.is(':checked')) {
            let window_page = '#window-' + id_;

            $('.prev_pages').show();

            if ($('#step-3 .lever__subscriber').hasClass(a) || $('#step-1 .lever__subscriber').hasClass(a)) {
                if (id_ === 2 || id_ === '2') {
                    window_page = window_page + '_1';
                }
            }

            if ($('#step-2 .lever__timer').hasClass(a)) {
                timer = true;
            }

            img = $('#step-2 .images img').attr('src');

            page_open(window_page, timer, img);
        } else {
            $('.prev_pages').hide();

            let window_page = '#window-2';

            if ($('#step-5 .lever__subscriber').hasClass(a) || $('#step-1 .lever__subscriber').hasClass(a)) {
                window_page = window_page + '_1';
            }

            if ($('#step-5 .lever__timer').hasClass(a)) {
                timer = true;
            }

            img = $('#step-5 .images img').attr('src');

            page_open(window_page, timer, img);
        }

        $('.prev_window .knot__ava img').attr('src', $('.content_form_ava .ava img').attr('src'));
    }

    function page_open(e, timer, img) {
        if (timer) {
            $(e).find('.timer').show();
        } else {
            $(e).find('.timer').hide();
        }

        if (img) {
            $('.prev_window .knot__img img').attr('src', img);
        } else {
            $('.prev_window .knot__img img').attr('src', '');
        }

        if (!$(e).hasClass(a)) {
            $('.prev_window').hide(600).removeClass(a);
            $(e).show(600).addClass(a);
        }
    }

    function prev_color(e) {
        let e_ = $(e);

        // $('.prev_window .wrapper:after, .modal-block').css({
        //     'background-color': 'linear-gradient(225deg,' + e_.data('bgcolor-1') + ',' + e_.data('bgcolor-2') + ')',
        //     'color': e_.data('text-color')
        // });
        $('.prev_window .wrapper').css({
            '--background': 'linear-gradient(225deg,' + e_.data('bgcolor-1') + ',' + e_.data('bgcolor-2') + ')',
            '--color': e_.data('text-color')
        });

        $('.btn.transparent-btn').css({
            'color': e_.data('text-color')
        });

        $('.prev_window .content-icon').css({
            'background-color': e_.data('panel_icon_bg_color') + '!important;'
        });

        $('.user-content, .timer .timer-block').css({
            'background-color': e_.data('panel'),
            'color': e_.data('panel_text_color')
        });
        $('#login_input, #login_input_2').css({
            'background-color': e_.data('input_bg_color'),
            'color': e_.data('input_text_color')
        })
    }

    $(document).ready(function () {
        if ($('.input__color input:checked').length >= 1) {
            prev_color($('.input__color input:checked'));
        }
    });

    $(document).on('click', '.input__color input', function () {
        prev_color(this);
    });

    function set_value_all_input(input) {
        let input_ = $(input),
            value = input_.val(),
            text = input_.text();

        if (input_.attr('name') === 'popup_text') {
            for (let inp of $(`textarea[name=${input_.attr('name')}]`)) {
                $(inp).val(value)
                $(inp).text(text)
            }
        } else {
            for (let inp of $(`input[name=${input_.attr('name')}]`)) {
                $(inp).val(value)
            }
        }
    }

    function prev_input(input) {
        let e = '.insert__' + $(input).attr('data-id'),
            text = $(input).val().replace(/\r\n|\r|\n/g,'<br />'),
            input_ = '.input__read input[data-id="' + $(input).attr('data-id') + '"]';

        $(input_).val(text);

        if ($(e).hasClass('timer')) {
            $('input[name="timer-time"]').val(text);
            $('.timer-block .sec').text(text);

            if (text >= 3599) {
                $('input[data-id=timer]').val(3599);
            }

            let minutes = Math.floor(text % 3600 / 60),
                seconds = Math.floor(text % 3600 % 60);

            if (minutes <= 9) {
                minutes = '0' + minutes;
            }

            if (seconds <= 9) {
                seconds = '0' + seconds;
            }

            $('.time span.time__minutes').text(minutes);
            $('.time span.time__seconds').text(seconds);

        } else if ($(input_).attr('data-id') === 'hit_url') {
            $('.insert__hit_button').attr('href', text);

        } else {
            $(e).html(text);
        }
    }

    $(document).ready(function () {
        if ($('.prev').length) {
            let input,
                textarea;

            if ($('#typePage-2').is(':checked')) {
                input = $('#step-1, #step-2, #step-3, #step-4').find('.input__read input');
                textarea = $('#step-1, #step-2, #step-3, #step-4').find('.input__read textarea')
            } else {
                input = $('#step-5 .input__read input');
                textarea = $('#step-5 .input__read textarea');

                input.push($('input#id_instagram_username'))
            }

            for (let i = input.length - 1; i >= 0; i--) {
                prev_input(input[i]);
            }

            for (let i = textarea.length - 1; i >= 0; i--) {
                prev_input(textarea[i]);
            }
        }
    });

$(document).ready(() => {
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
        deleteInstagramFolderAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: '/folders/delete/',
                headers: {'X-CSRFToken': CSRFToken},
                data,
            }),
        deleteVKFolderAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: '/vk-folders/delete/',
                headers: {'X-CSRFToken': CSRFToken},
                data,
            }),
        deleteTGFolderAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: '/tg-folders/delete/',
                headers: {'X-CSRFToken': CSRFToken},
                data,
            }),

        // slug check
        checkSlugUpdateAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: 'slug-check/',
                headers: {'X-CSRFToken': CSRFToken},
                data,
            }),

        appendToTGFolderAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: '/tg-folder/append/',
                headers: {'X-CSRFToken': CSRFToken},
                data,
            }),

        appendToVKFolderAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: '/vk-folder/append/',
                headers: {'X-CSRFToken': CSRFToken},
                data,
            }),

        appendToInstagramFolderAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: '/folder/append/',
                headers: {'X-CSRFToken': CSRFToken},
                data,
            }),

        // change theme
        changeThemeAjax = async (data) =>
            await $.ajax({
                method: 'get',
                url: '/change-theme/',
                data,
            }),

        checkSlugCreateAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: '/subscribe-page/create/slug-check/',
                headers: {'X-CSRFToken': CSRFToken},
                data,
            }),


        // page
        pageListAjax = async () =>
            await $.ajax({
                method: 'get',
                url: '/subscribe-pages/list/',
                data
            }),

        deleteTGPageAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: '/tg-subscribe-page/delete/',
                headers: {'X-CSRFToken': CSRFToken},
                data,
            }),

        deleteVKPageAjax = async (data, CSRFToken) =>
            await $.ajax({
                method: 'post',
                url: '/vk-subscribe-page/delete/',
                headers: {'X-CSRFToken': CSRFToken},
                data,
            }),

        deleteInstagramPageAjax = async (data, CSRFToken) =>
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

        // statistic
        searchAjax = async (data) =>
            await $.ajax({
                method: 'get',
                url: 'search-subscribers/',
                data
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

    var a = 'active';
    // Hover nav

    if ($('.header_nav').length) {
        $('.header_nav').hoverSlippery({
            border: true,
            underline: true,
            speed: 430,
            borderColor: 'var(--blue)',
            borderWidth: '2px'
        })
    }

    // Sign up

    if ($('.sign_form').length) {
        let phone_input = $('input[name=phone]');
        if (phone_input.length) {
            phone_input.inputmask('phone');
        }
    }


// Nav scroll active

    if ($('.header_nav').length) {
        let lastId,
            h = $('.header').outerHeight(),
            topMenu = $('.header_nav .nav'),
            topMenuHeight = topMenu.outerHeight(),
            menuItems = topMenu.find('a'),
            scrollItems = menuItems.map(function () {
                let item = $($(this).attr('href'));

                if (item.length) {
                    return item;
                }
            });

        menuItems.click(function (e) {
            let href = $(this).attr('href'),
                offsetTop = href === '#' ? 0 : $(href).offset().top - topMenuHeight - h;
            $('html, body').stop().animate({
                scrollTop: offsetTop
            }, 1000);
            e.preventDefault();
        });

        $(window).scroll(function () {
            let fromTop = $(this).scrollTop() + topMenuHeight + h + 1,
                cur = scrollItems.map(function () {
                    if ($(this).offset().top < fromTop)
                        return this;
                });
            cur = cur[cur.length - 1];
            let id = cur && cur.length ? cur[0].id : "";

            if (lastId !== id) {
                lastId = id;
                menuItems.parent().removeClass(a).end().filter("[href='#" + id + "']").parent().addClass(a);

                let aHref = menuItems.parent().end().filter("[href='#" + id + "']"),
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

    $(document).ready(fixed_nav());
    $(window).scroll(function () {
        fixed_nav()
    });

    function fixed_nav() {
        let e = $('.header'),
            h = $('.header').outerHeight() + 40,
            a = $(window).scrollTop(),
            r = $('.main').attr('data-inner'),
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

    $(document).ready(function () {
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

        if ($('.pages_items').length) {
            $('.pages_items').slick({
                slidesToShow: 2,
                slidesToScroll: 1,
                prevArrow: '<button type="button" class="slick-prev slick-arrow"><svg width="54" height="13" viewBox="0 0 54 13" fill="none"><path d="M0.736141 7.07406C0.409252 6.74717 0.409252 6.21718 0.736141 5.89029L6.06312 0.563311C6.39001 0.236421 6.92001 0.236421 7.24689 0.563311C7.57379 0.890201 7.57379 1.42019 7.24689 1.74708L2.5118 6.48218L7.24689 11.2173C7.57379 11.5442 7.57379 12.0742 7.24689 12.401C6.92001 12.7279 6.39001 12.7279 6.06312 12.401L0.736141 7.07406ZM53.709 7.31923H1.32803V5.64512H53.709V7.31923Z" fill="#0057FF"/></svg></button>',
                nextArrow: '<button type="button" class="slick-next slick-arrow"><svg width="54" height="13" viewBox="0 0 54 13" fill="none"><path d="M53.2521 7.07406C53.579 6.74717 53.579 6.21718 53.2521 5.89029L47.9252 0.563311C47.5983 0.236421 47.0683 0.236421 46.7414 0.563311C46.4145 0.890201 46.4145 1.42019 46.7414 1.74708L51.4765 6.48218L46.7414 11.2173C46.4145 11.5442 46.4145 12.0742 46.7414 12.401C47.0683 12.7279 47.5983 12.7279 47.9252 12.401L53.2521 7.07406ZM0.279297 7.31923H52.6603V5.64512H0.279297V7.31923Z" fill="#0057FF"/></svg></button>',
                responsive: [{
                  breakpoint: 600,
                  settings: {
                    slidesToShow: 1
                  }
                }]
            });
        };

        if ($('.results_items').length) {
            $('.results_items').slick({
                prevArrow: '<button type="button" class="slick-prev slick-arrow"><svg width="54" height="13" viewBox="0 0 54 13" fill="none"><path d="M0.736141 7.07406C0.409252 6.74717 0.409252 6.21718 0.736141 5.89029L6.06312 0.563311C6.39001 0.236421 6.92001 0.236421 7.24689 0.563311C7.57379 0.890201 7.57379 1.42019 7.24689 1.74708L2.5118 6.48218L7.24689 11.2173C7.57379 11.5442 7.57379 12.0742 7.24689 12.401C6.92001 12.7279 6.39001 12.7279 6.06312 12.401L0.736141 7.07406ZM53.709 7.31923H1.32803V5.64512H53.709V7.31923Z" fill="#0057FF"/></svg></button>',
                nextArrow: '<button type="button" class="slick-next slick-arrow"><svg width="54" height="13" viewBox="0 0 54 13" fill="none"><path d="M53.2521 7.07406C53.579 6.74717 53.579 6.21718 53.2521 5.89029L47.9252 0.563311C47.5983 0.236421 47.0683 0.236421 46.7414 0.563311C46.4145 0.890201 46.4145 1.42019 46.7414 1.74708L51.4765 6.48218L46.7414 11.2173C46.4145 11.5442 46.4145 12.0742 46.7414 12.401C47.0683 12.7279 47.5983 12.7279 47.9252 12.401L53.2521 7.07406ZM0.279297 7.31923H52.6603V5.64512H0.279297V7.31923Z" fill="#0057FF"/></svg></button>',
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
            let direction;
            if (Math.abs(nextSlide - currentSlide) === 1) {
                direction = (nextSlide - currentSlide > 0) ? 1 : 0;
            }
            else {
                direction = (nextSlide - currentSlide > 0) ? 0 : 1;
            }

            if (direction === 1) {
                $('.content_slid').removeClass('last');
                $('.content_slid.slick-active:last').next().addClass('last');
            } else {
                $('.content_slid').removeClass('last');
                $('.content_slid.slick-active:last').prev().addClass('last');
            }
        });
    });


// Dropdown

    $(document).on('click', '.droprown_item', function () {
        let e = $(this),
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

    const animItems = document.querySelectorAll('.anim');

    if (animItems.length > 0) {
        window.addEventListener('scroll', animOnScroll);

        function animOnScroll() {
            for (let index = 0; index < animItems.length; index++) {
                const animItem = animItems[index],
                      animItemHeight = animItem.offsetHeight,
                      animItemOffset = offset(animItem).top,
                      animStart = 4;

                let animItemPoint = window.innerHeight - animItemHeight + 100;

                if (animItemHeight > window.innerHeight) {
                    animItemPoint = window.innerHeight - window.innerHeight / animStart;
                }
                if (animItem.classList.contains('anim_wis')) {
                    animItemPoint = animItemOffset - window.innerHeight + 100;

                    if (pageYOffset > animItemPoint) {
                        animItem.classList.add('anim_act');
                        setTimeout(function () {
                            if (animItem.classList.contains('anim__hover')) {
                                animItem.classList.add('anim_act__hover')
                            }
                        }, 2000);
                    }
                } else {
                    if ((pageYOffset > animItemOffset - animItemPoint) && pageYOffset < (animItemOffset + animItemHeight)) {
                        animItem.classList.add('anim_act');
                        setTimeout(function () {
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
                scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
                scrollTop = window.pageXOffset || document.documentElement.scrollTop;

            return {top: rect.top + scrollTop, left: rect.left + scrollLeft}
        }

        setTimeout(() => {
            animOnScroll();
        }, 300);

    };


// Cabinet theme

    if (!$('body').hasClass('white')) {
        $('.nav__theme p').text('Тёмная тема');
    };

    $(document).on('click', '.nav__theme', async function () {
        console.log('it was i, Dio')
        if (!$('body').hasClass('white')) {
            $('.nav__theme p').text('Светлая тема');
            await changeThemeAjax({'white': true})
        } else {
            $('.nav__theme p').text('Темная тема');
            await changeThemeAjax({'dark': true})
        }
        $('.lever, .theme').toggleClass('white')
    });

// Select

    $(document).ready(function () {
        let i = $('.select_info, .select__info');

        i.on('click', function () {
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

            p.mousedown('click', function () {
                event.stopPropagation();
            })

            o.on('click', function () {
                var e = $(this);
                t = e.html();

                p.removeClass(a);
                i.html(t);
                o.removeClass(a);
                e.addClass(a);

                if (i.hasClass('select__payment')) {
                    var data = e.data('payment'),
                        input = $('.input__payment input'),
                        paymentTypeInput = $('input[name=payment_type]');;

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

            $('html').mousedown('click', function (event) {
                if (p.hasClass(a)) {
                    p.removeClass(a);
                }
            });
        });
    });


// Modal

    let m = $('.modal'),
        modalSelector;

    $(document).on('click', '.dtn__modal', function () {
        let dataModal = $(this).data('modal');
        modalSelector = '.modal_' + dataModal;

        if (dataModal === 'carry') {
            let pageID = $(this).data('id');
            $('#page_slug').val(pageID)
        } else if (dataModal === 'folder') {
        	let folderID = $(this).data('element-id'),
				folderIDInput = $('#folderRenameForm input[name="id"]');
        	folderIDInput.val(folderID)
		}

        modalAction(modalSelector, 'show');

    });

    $('.modal_wrapper').mousedown(function () {
        event.stopPropagation();

        if ($('.select').hasClass(a)) {
            $('.select').removeClass(a);
        }
    });

    $('html, .modal_close, .btn__close').mousedown(function (event) {
        if (m.hasClass('active')) {
            if (m.hasClass('modal_ok')) {
                $(location).attr('href', '/subscribe-pages');
            }

            modalAction(modalSelector, 'hide');
            $('html').removeClass('hidden');
        }
    });


// Calendar
    if ($('input[name=daterange]').length) {

        $(function () {
            let date = new Date(),
                daterangeInput = $('input[name=daterange]');
            date.setDate(date.getDate() - 7);

            moment.lang('zh-cn', {
                week: {
                    dow: 1 // Monday is the first day of the week
                }
            });

            daterangeInput.daterangepicker({
                    opens: 'right',
                    startDate: date,
                    // showDropdowns: true,
                    minYear: 2008,
                    showCustomRangeLabel: false,
                    cancelButtonClasses: 'btn-outline',
                    applyButtonClasses: 'btn-red',
                    // maxYear: parseInt(moment().add(1, 'years').format('YYYY')),
                    ranges: {
                        'Вчера': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                        'Сегодня': [moment(), moment()],
                        'Последние 7 дней': [moment().subtract(6, 'days'), moment()],
                        'Последний месяц': [moment().startOf('month'), moment().endOf('month')],
                        'Последние 6 месяцев': [moment().subtract(6, 'month'), moment()],
                        'Прошедший год': [moment().startOf('years'), moment().endOf('years')],
                    }
                },

                function (start, end, label) {
                    $('#start_date').attr('value', start.format('YYYY-MM-DD'));
                    $('#end_date').attr('value', end.format('YYYY-MM-DD'));
                });
        });
    }

$(document).on('click', '.statistic_button .button', function () {
    $('#start_date').attr('value')
});
// $(document).ready(function () {
//         let daterangeInput = $('input[name=daterange]');
//         console.log(daterangeInput)
//         if (daterangeInput.length) {
//             let date = new Date();
//
//             date.setDate(date.getDate() - 7);
//
//             moment.lang('zh-cn', {
//                 week: {
//                     dow: 1 // Monday is the first day of the week
//                 }
//             });
//
//             date = moment().weekday(0); // date now is the first day of the week, (i.e., Monday)
//
//             daterangeInput.daterangepicker({
//                     opens: 'right',
//                     startDate: date,
//                     // showDropdowns: true,
//                     minYear: 2008,
//                     showCustomRangeLabel: false,
//                     cancelButtonClasses: 'btn-outline',
//                     applyButtonClasses: 'btn-red',
//                     // maxYear: parseInt(moment().add(1, 'years').format('YYYY')),
//                     ranges: {
//                         'Вчера': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
//                         'Сегодня': [moment(), moment()],
//                         'Последние 7 дней': [moment().subtract(6, 'days'), moment()],
//                         'Последний месяц': [moment().startOf('month'), moment().endOf('month')],
//                         'Последние 6 месяцев': [moment().subtract(6, 'month'), moment()],
//                         'Прошедший год': [moment().startOf('years'), moment().endOf('years')],
//                     }
//                 },
//                 function (start, end, label) {
//                     console.log(start, end)
//                     $('#start_date').attr('value', start.format('YYYY-MM-DD'));
//                     $('#end_date').attr('value', end.format('YYYY-MM-DD'))
//                 }
//             );
//
//         }
//             function(start, end, label) {
//                 var years = moment().diff(start, 'years');
//                 // alert("You are " + years + " years old!");
//               });
//     });


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
        let input = $(this).parent().find('input');
        console.log($(this))
        console.log(input)

        if (input.attr('type') === 'password') {
            input.attr('type', 'text');
        } else {
            input.attr('type', 'password');
        }
    });


// Проверка фона

    $('.images__wrapper .images img').each(function () {
        if (this.src.length > 0) {
            $('.images__wrapper').addClass('active');
        }
    });

// Замена на выбраное изображениe

    function readURL_ava(t, a, b, c) {
        let e;
        console.log(a);
        t.files && t.files[0] && (
            (e = new FileReader).onload = function (e) {
                if (t.files[0].size > 310000) {
                    for (let error_msg of $('.content_form_photo_btn').parent().find('.photo_error')) {
                        $(error_msg).text('Размер фото не должен превышать 300кб');
                    };
                } else {

                    for (let img of b) {
                        $(img).attr('src', e.target.result);
                    }
                    $('.images__wrapper').addClass('active');


                    c.attr('src', e.target.result);
                    b.attr('style', '');
                }
            },
                e.readAsDataURL(t.files[0]))
    }

    $('.images__wrapper .input__hidden').change(function () {
        for (let error_msg of $('.content_form_photo_btn').parent().find('.photo_error')) {
            $(error_msg).text('');
        };
        imagess(this)
    })

    function imagess(e) {
        console.log($(e));
        let a = $(e).parents('.images__wrapper'),
            b,
            prev_img;

        if ($(e).attr('name') === 'page_photo') {
            b = $('.photo.images img')
        } else if ($(e).attr('name') === 'instagram_avatar') {
            b = $('.ava.images img')
        }

        if ($(e).attr('id') === 'ava') {
            prev_img = $('.prev_window .knot__ava img');
        } else {
            prev_img = $('.prev_window .knot__img img');
        }

        readURL_ava(e, a, b, prev_img);
    }

// удаление фона

    $('.images__close').on('click', function () {
        let img = $(this).parent().find('.images img'),
            input = $(this).parent().find('input');

        $(img).attr('src', '');
        $('.prev_window .knot__img img').attr('src', '');
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
                if (stepClass === '.step-5') {
                    stepClass = '.step-2';
                }
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
        console.log('heya')

        if (!$(this).hasClass('open')) {
            var step = $(this).attr('data-id'),
                stepId = '#' + step,
                stepActive = $('.content_step_li.open').attr('data-id'),
                stepActiveId = '#' + stepActive,
                b = 1,
                posTop = 0;

            if ($('input[name=typePage]:checked').attr('id') === 'typePage-1' && step === 'step-2') {
                stepId = '#step-5';
            }
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
            $('input[name=typePage]').attr('checked', false);
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

    $('.lever__wrapper:not(.readonly)').on('click', function () {
        var e = $(this),
            inner = '.' + e.attr('id');

        e.toggleClass(a);
        $(inner).slideToggle();

        if (e.hasClass('lever__timer')) {
            prev_page(false, false, $('#typePage-2'));

            if (e.hasClass('active')) {
                $('input[name=is_timer_active]').val(true)
            } else {
                $('input[name=is_timer_active]').val(false)
            }

        } else if (e.hasClass('lever__subscriber')) {
            prev_page(false, false, $('#typePage-2'));

            if (e.hasClass('active')) {
                $("#id_show_subscribers").val(true)
            } else {
                $("#id_show_subscribers").val(false)
            }
        } else if (e.hasClass('lever__type_group_id')) {
            if (e.hasClass('active')) {
                $("#id_type_group_id").val('slug')
            } else {
                $("#id_type_group_id").val('id')
            }
        }
    });


    $(document).on('click', '.show__hint_in_modal', () => {
        $('.show__hint_in_modal').addClass('active')

        setTimeout(() => {
			$('.show__hint_in_modal').removeClass('active');
		}, 1000);
    })
    
	$(document).on('click', '.copy__href', function () {
		let e = $(this),
			f = $('<input>'),
            op,
            id_;

		if (e.hasClass('modal_ok_btn')) {
			op = '.modal_ok .page_link';
		} else if (e.hasClass('partner_copy')) {
		    op = `#channel-${e.data('channel-id')}`;
        } else if (e.hasClass('domain_copy')) {
		    op = '.icon'
        } else {
		    id_ = e.attr('id').match(/\d+$/) - 0;
			op = '#page_open-' + id_;
		}

		let link = $(op).attr('href'),
            domain = 'https://instateleport.ru/',
            input = $('<input autofocus="false" class="input_copied"/>');

        if (!e.hasClass('domain_copy')) {
            if (link.indexOf('https://') === -1) {
              link = domain + link;
            }
        }

        if(!$(this).find('.input_copied').length) {
          input = input.val(link);
          input.css({
            'position': 'absolute',
            'left': '-9999px',
              'font-size': '18px'
          });
          $(this).append(input);
        }

        input = $(this).find('.input_copied');
        $(input[0]).val(link);
        input[0].select();
        input[0].setSelectionRange(0, 99999);
        document.execCommand('copy');
        input.remove();

        $('.copy__href').addClass('active');

		setTimeout(() => {
			$('.copy__href').removeClass('active');
		}, 1000);
	});



// Media

    $(document).ready(media);
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

            $('.prev_windows').removeClass('scale');
            $('#prev-scale').removeClass(a);

            $('.prev_wrapper').animate({
                width: 455,
                height: 440
            }, 20)
        } else {
            $('.prev_wrapper').removeClass('small');

            if ($('#prev-scale').hasClass(a)) {
                $('.prev_wrapper').animate({
                    height: 637
                }, 20)
            } else {
                $('.prev_wrapper').animate({
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
            $('.prev_wrapper').animate({
                width: 280,
                height: 300
            }, 20)
        }

    };

    // Statistic

    // if ($('.statistik').length) {
    //     let searchInput = $('.search input'),
    //         subscriberTable = $('.statistik_table_wrapper table');
    //
    //     searchInput.on('change', async function () {
    //         let response;
    //         subscriberTable.find('tbody').empty();
    //
    //         response = await searchAjax(
    //             {
    //                 instagram_username: searchInput.val()
    //             }
    //         );
    //
    //         for (let subscriber of response.subscribers) {
    //             let subscribed;
    //
    //             if (subscriber.subscribed) {
    //                 subscribed = '<td class="green">Подписался</td>'
    //             } else {
    //                 subscribed = '<td class="orange">Не подписался</td>'
    //             }
    //
    //             subscriberTable.append(`<tr>
    //                     <td>${ subscriber.date }</td>
    //                     <td>${ subscriber.username }</td>
    //                     ${subscribed}
    //                 </tr>
    //             `)
    //         }
    //
    //         console.log(response)
    //     })
    // }


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

    $(document).ready(function () {
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
    })


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
        setTimeout(function () {
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

            $('.prev_wrapper').animate({
                width: w,
                height: h
            }, 0, 'linear');

            $('.prev_windows').toggleClass('scale');
        }

        $('.prev_wrapper').addClass('trs');

        setTimeout(function () {
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

                $('.prev_window, .prev_windows').removeClass('mobile');
            } else {
                var w = 375,
                    h = 667;

                $('.prev_window, .prev_windows').addClass('mobile');
            }

            $('.prev_windows').animate({
                width: w,
                'min-width': w,
                height: h,
                'min-height': h
            }, 830, 'linear');
        }

    });


// No error

    $('input').on('keydown', function () {
        if ($(this).hasClass('error')) {
            $(this).removeClass('error');
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

    // $(document).ready(function () {
    //     if ($('.emoj').length) {
    //         $('.emoj').emojiPicker({
    //             onShow: function () {
    //                 $('head').append('<link rel="stylesheet" type="text/css" href="styles/jquery.emojipicker.a.css">');
    //             }
    //         });
    //     }
    // });


    // Delete

    let forDelete;

	$(document).on('click', '.delete__btn', function () {
		forDelete = $(this).parents('.delete__e');
		let typeOfDelete = $(this).data('modal'),
			modalSelector = '.modal_' + typeOfDelete,
			elementID = $(this).data('element-id'),
			CSRFToken = $('input[name=csrfmiddlewaretoken]').val();
        console.log(elementID)
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
					await deleteInstagramFolderAjax(
						{
							'folderID': elementID
						}, CSRFToken
					);
					window.location = ''
					break;
                case 'tg_delete_folder':
                    await deleteTGFolderAjax(
                        {
							'folderID': elementID
						}, CSRFToken
                    )
                    window.location = ''
					break;
				case 'vk_delete_folder':
					await deleteVKFolderAjax(
						{
							'folderID': elementID
						}, CSRFToken, true
					);
					window.location = ''
					break;
				case 'delete_page':
					await deleteInstagramPageAjax(
						{
							'pageID': elementID
						}, CSRFToken
					);
					break;
				case 'vk_delete_page':
					await deleteVKPageAjax(
						{
							'pageID': elementID
						}, CSRFToken
					);
					break;
                case 'tg_delete_page':
                    await deleteTGPageAjax(
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

// Scrollbar size

    let block = $('<div>').css({'height': '50px', 'width': '50px'}),
        indicator = $('<div>').css({'height': '200px'});

    $('body').append(block.append(indicator));
    let w1 = $('div', block).innerWidth();
    block.css('overflow-y', 'scroll');
    let w2 = $('div', block).innerWidth();
    $(block).remove();

    let scrollbar = w1 - w2;

    $(':root').css('--scroll', w1 - w2 + 'px');



    // bg_color
    $(document).on('click', '.input_color__hidden', function () {
        let color_id = $(this).attr('data-id'),
            input = $('#id_bg_color');
        input.val(color_id)
    });

// domain
    $(document).on('click', '.select_opt', function () {
        let data = $(this).attr('data-domain-id'),
            input = $('#id_domain');
        input.val(data)
    });

// slug
    $(document).on('change', '#id_slug', async function () {
        let csrfToken = $('input[name=csrfmiddlewaretoken]').val(),
            response = await checkSlugUpdateAjax({'slug': $(this).val()}, csrfToken);

        if (response['is_unique'] === false) {
            $(this).addClass('sheet_input error');
            $(this).next('.input_err').text(response['error'])
        }
    });


    $(document).on('change', '#id_slug_create', async function () {
        let csrfToken = $('input[name=csrfmiddlewaretoken]').val(),
            response = await checkSlugCreateAjax({'slug': $(this).val()}, csrfToken);

        if (response['is_unique'] === false) {
            $(this).addClass('sheet_input error');
            $(this).next('.input_err').text(response['error'])
        }
    });

// Тип страницы
    $(document).on('click', '#typePage-1', function () {
        $('#id_single_page').val(true);
        
	if (!$('#id_title').val()) {
	        $('#id_title').val('Заголовок');
	}
	if (!$('#id_description').val()) {
	        $('#id_description').val('Описание')
	}
    });
    $(document).on('click', '#typePage-2', function () {
        $('#id_single_page').val(false);
        if (!$('#id_title').val()) {
        	$('#id_title').val(null);
	}
        if (!$('#id_description')) {
	        $('#id_description').val(null);
	}
    });

// Если тип страницы - 'одностраничный' --- для DetailView
    $(document).ready(function () {
        let e = $('#id_single_page').val();

        if (e === 'True' || e === true) {
            $('#typePage-1').attr('checked', true);
            $('.content_step_li.step-2').nextAll().hide();
            $('.content_step_li.step-2 .content_step_top span').hide();
        }
    });


// Move page to folder
    $(document).on('click', '.select_opt', function () {
        let folder_id = $(this).attr('data-id');
        $('#folder_id').val(folder_id)
    });

    $(document).on('click', '#moveFolderButton', async function () {
        let csrfToken = $('input[name=csrfmiddlewaretoken]').val(),
            slg = $('#page_slug').val(),
            folder_id = $('#folder_id').val(),
            type = $(this).data('type')

        let response = null
        console.log(type)
        switch (type) {
            case 'vk':
                response = await appendToVKFolderAjax(
                    {
                        'slug': slg,
                        'group_id': folder_id
                    },
                    csrfToken,
                );
                break;
            case 'tg':
                response = await appendToTGFolderAjax(
                    {
                        'slug': slg,
                        'group_id': folder_id
                    },
                    csrfToken,
                );
                break;
            case 'ig':
                    response = await appendToInstagramFolderAjax(
                        {
                            'slug': slg,
                            'group_id': folder_id
                        },
                        csrfToken,
                    );
                    break;
        }
        console.log(response)

        if (response['status'] === 'SUCCESS') {
            window.location = response['url']
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

    // вывод
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

            $('#payoutTable').prepend(`
                <tr>
                    <td>${ payout.created_date }</td>
                    <td>${ payout.amount } ₽</td>
                    <td>
                        ${ payout.payment_type }
                        <br/>${ payout.payment_address }
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

// // Partner delete
//     $(document).on('click', '.partner_delete', async function () {
//         let csrf_token = $('input[name=csrfmiddlewaretoken]').val(),
//             channel_id = $('#channelId').val(),
//             response = await channelDeleteAjax({'channelID': channel_id}, csrf_token);
//     });
//
//     $(document).on('click', '.delete_svg', function () {
//         let channel_id = $(this).attr('data-element-id');
//         $('#channelId').val(channel_id)
//     });

// // Theme
//     $(document).on('click', '.nav__theme' function () {
//         if ($('.theme').hasClass('white')) {
//             await changeThemeAjax({'dark': true})
//         } else {
//             await changeThemeAjax({'white': true})
//         }
//     });

    if ($('#subscribePageForm').length) {
        $(document).on('change keyup input focus', '.input input, .input textarea', function () {
            set_value_all_input(this);
        });

        $(document).on('change keyup input focus', '.input__read input, .input__read textarea', function () {
            prev_input(this);
        });

        $(document).on('click', '.prev_window #form-block1 .button, .prev_window #form-block1_2 .button', function () {
            $('#form-block1, #form-block1_2').slideUp();
            $('#form-block2, #form-block2_2').slideDown();

            $('.user-content__sub').hide();
            $('.user-content__ex').css('display', 'flex');
        });

        $(document).on('click', '.prev_window #form-block2 .already-subscribe.button, .prev_window #form-block2_2 .already-subscribe.button', function () {
            $('#form-block1, #form-block1_2').slideDown();
            $('#form-block2, #form-block2_2').slideUp();

            $('.user-content__sub').css('display', 'flex');
            $('.user-content__ex').hide();
        });
    }



    if ($('.message').length) {
        $('.message').addClass('active');
        setTimeout(function () {
            $('.message').removeClass('active')
        }, 5000)
    };

    // reg
    if ($('#signUpForm').length) {
        $('#signUpForm').on('submit', function (e) {
            let username = $('input[name=username]').val(),
                email = $('input[name=email]').val();

            carrotquest.track('$registered', {'$email': email, '$name': username});
            carrotquest.identify([
                {op: "update_or_create", key: "$email", value: email},
                {op: "update_or_create", key: "$name", value: username}
            ]);

            carrotquest.track('$authorized', {'$name': username});
            carrotquest.identify([
                {op: "update_or_create", key: "$name", value: username}
            ])
        })
    }

    // auth
    if ($('#authForm').length) {
        $('#authForm').on('submit', function (e) {
            let username = $('input[name=username]').val();

            carrotquest.track('$authorized', {'$name': username});
            carrotquest.identify([
                {op: "update_or_create", key: "$name", value: username}
            ])
        })
    }
});
