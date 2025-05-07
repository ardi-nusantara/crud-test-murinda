$(document).ready(function () {
    $('#add-choice').click(function () {
        var form_idx = $('#id_choice_set-TOTAL_FORMS').val();
        $('#choice-formset').append($('#empty-form').html().replace(/__prefix__/g, form_idx));
        $('#id_choice_set-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });

    $(document).on('click', '.remove-choice', function () {
        $(this).closest('.choice-form').hide();
        checkDeleteCheckbox(this);
        updateFormIndexes();
    });

    function checkDeleteCheckbox(element) {
        let del_checkbox_idx = element.parentNode.children[2].children[0].id.split('-')[1]
        const del_checkbox = document.getElementById(`id_choice_set-${del_checkbox_idx}-DELETE`)
        del_checkbox.checked = true
    }

    function updateFormIndexes() {
        $('.choice-form').each(function (index) {
            $(this).find('.form-control').each(function () {
                var name = $(this).attr('name').replace(/-\d+-/, '-' + index + '-');
                $(this).attr('name', name);
                $(this).attr('id', 'id_' + name);
            });
        });
    }
});
