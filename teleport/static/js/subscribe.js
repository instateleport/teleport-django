var subscribe_status

async function subscribeCheck(login, CSRFToken){
    const formData = new FormData()
    formData.append("csrfmiddlewaretoken", CSRFToken)
    formData.append("login", login)
    const domain = location.protocol + '//' + location.host;
    const res = await fetch(`${domain}/page/${page_slug}/subscribe/check-subscribe/`, {method: "POST", body: formData})

    return  {status: await res.text()}
}

$('#login_input').on('input paste', function(){
    $("#login_input").val($(this).val().replace("@", "").trim().toLowerCase())
})

let getInputValue = (name) => $(`input[name=${name}]`).val(),
    texts = {
        presubscribe_text: getInputValue('presubscribe_text'),
        precheck_subscribe_text: getInputValue('precheck_subscribe_text'),
        preSearchText: getInputValue('presearch_text'),
        search_text: getInputValue('search_text'),
        search_time_text: getInputValue('search_time_text'),
        success_text: getInputValue('success_text'),
        error_text: getInputValue('error_text')
    },
    subBack = () => {
        $('#form-block2').hide();
        $('#form-block1').show();

        $('#preCheckSubscribePanel').hide();
        $('#preSubscribePanel').show();
        $('.subscript_title').text(texts['presubscribe_text'])
    },
    subNext = () => {
        $('#form-block1').hide();
        $('#form-block2').show();

        $('#preSubscribePanel').hide();
        $('#preCheckSubscribePanel').show();
        $('.subscript_title').text(texts['precheck_subscribe_text'])
    };

    page_slug = $('input[name=page_slug]').val(),
    page_options = JSON.parse(localStorage.getItem(`page_${page_slug}_subscribe_status`)),
    subscribe_status;

$("#go-subscribe").on("click", function (event) {
    let e = $(this),
        instagram_link = e.attr('instagram');

    event.preventDefault();
    subNext();
    localStorage.setItem(
        `page_${page_slug}_subscribe_status`,
        JSON.stringify({subscribe_status: 'check'})
    );
    setTimeout(() => {
        window.location.href = instagram_link
    }, 3000);	//Время через которое будет переход на инстаграм
    setTimeout(() => {
        $('#modal-return-back').removeClass('open');
    }, 4000);

    $('#modal-return-back').addClass('open');
});

$(document).on('click', '.already-subscribe', function () {
    localStorage.setItem(
        `page_${page_slug}_subscribe_status`,
        JSON.stringify({subscribe_status: 'check'})
    );
    subNext()
});


$('input[name=instagram_username]').hover(function () {
    $('input[name=instagram_username]').removeClass('error')
});

$('#subscribed-check').click(async function (e) {
    e.preventDefault();
    const login_input = $('input[name=instagram_username]'),
        login = login_input.val();

    if (login){
        const CSRFToken = $('input[name=csrfmiddlewaretoken]').val(),

            searching_panel = $('#modal-loading'),
            searching_panel__text = searching_panel.find('.modal-content'),
            searching_panel__loading = searching_panel.find('.modal-icon'),

            success_panel = $('#modal-acc-found'),

            error_panel = $('#modal-not-sub');

        searching_panel__text.html(texts['search_text']);
        searching_panel.addClass('open');


        let subscribeCheckResponse = await subscribeCheck(login, CSRFToken);

        if (subscribeCheckResponse.status === 'SUCCESS') {
            searching_panel.removeClass('open');
            success_panel.addClass('open');

            setTimeout(() => {
                success_panel.removeClass('open');
                const domain = location.protocol + '//' + location.host;
                window.location.href = `${domain}/page/${page_slug}/success`
            }, 2000)
        } else if (subscribeCheckResponse.status === 'FAIL') {
            searching_panel.removeClass('open');
            login_input.addClass('error');

            error_panel.addClass('open');

            setTimeout(() => {
                error_panel.removeClass('open');
                // setTimeout(() => {
                
                // }, 500)
            }, 2000)
            
        }
    } else {
        alert('Поле логина пропущено')
    }
});

subBack();

if (page_options) {
    subscribe_status = page_options.subscribe_status;
}
if (subscribe_status === 'subscribe') {
    subBack()
} else if (subscribe_status === 'check') {
    localStorage.setItem(
        `page_${page_slug}_subscribe_status`,
        JSON.stringify(
            {
                subscribe_status: 'check',
            }
        )
    );
    subNext()
} else {
    localStorage.setItem(
        `page_${page_slug}_subscribe_status`,
        JSON.stringify(
            {
                subscribe_status: 'subscribe',
            }
        ),
    );
    subBack()
}
