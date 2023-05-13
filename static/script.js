$(document).ready(function() {
    $('#create-work-btn').click(function() {
        var newWorkId = $('#new-work-id').val().trim();
        if (newWorkId !== '') {
            var optionExists = $('#existing-work-select option[value="' + newWorkId + '"]').length > 0;
            if (!optionExists) {
                $('#existing-work-select').append('<option value="' + newWorkId + '">' + newWorkId + '</option>');
            }
            $('#existing-work-select').val(newWorkId);
        }
    });

    $('#choose-work-btn').click(function() {
        var selectedWorkId = $('#existing-work-select').val();
        if (selectedWorkId) {
            $('#selected-work-id').val(selectedWorkId);
        }
    });

    $('#upload-form').submit(function(event) {
        event.preventDefault();
        $('#result').empty();

        var form = $(this);
        var formData = new FormData(form[0]);

        $.ajax({
            url: form.attr('action'),
            type: form.attr('method'),
            data: formData,
            contentType: false,
            processData: false,
            beforeSend: function() {
                $('#loading-spinner').show();
            },
            success: function(response) {
                $('#loading-spinner').hide();
                $('#result').html(response);
            },
            error: function(xhr, status, error) {
                $('#loading-spinner').hide();
                console.log(error);
            }
        });
    });
});
