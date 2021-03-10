
$("button[value='change-status']").click(function() {
    const rem_id = this.id;
    const action = this.name;
    $.ajax ({
    url : '/reminder/ajax-change-status',
    data: {
            'rem_id': rem_id,
            'action': action,
        },
    success: function (data) {
            location.reload();
        }
    });
});


$(function () {
    $(".close").click(function () {
        $(".modal").modal("hide");
    });
});


$(function () {

    // Update reminder
    $(".update-rem").each(function () {
        $(this).modalForm({formURL: $(this).data("form-url")});
    });

    // Create reminder "
    $("#create-rem").modalForm({
        formURL: '/reminder/create/',
        modalID: '#create-modal'
    });

});