$(document).on('submit', '.update-plan-form', function (e) {
    e.preventDefault();

    var form = $(this);

    $.ajax({
        url: form.attr('action'),
        type: 'POST',
        data: form.serialize(),
        success: function (response) {

            $('.success-msg').remove();

            $('.premium-plan-header').append(
                '<div class="success-msg" style="margin-top:15px;color:#16a34a;font-weight:600;">' +
                response.message +
                '</div>'
            );

            setTimeout(function () {
                $('.success-msg').fadeOut(300, function () {
                    $(this).remove();
                });
            }, 3000);

        },
        error: function () {
            alert('Something went wrong.');
        }
    });
});