function setAddressFields(provinsi, kota, kecamatan, kelurahan) {
    if (provinsi) {
        // Set the provinsi field
        $('#id_provinsi').val(provinsi).trigger('change.select2');

        // Load and set the kota field
        $.ajax({
            type: 'GET',
            url: '/applicant/load-cities/',
            data: {'province_id': provinsi.split('_')[0]},
            success: function (data) {
                $('#id_kota').empty();
                $.each(data, function (index, item) {
                    $('#id_kota').append(`<option value="${item[0]}">${item[1]}</option>`);
                });
                $("#id_kota").val(kota);
            }
        });

        // Load and set the kecamatan field
        $.ajax({
            type: 'GET',
            url: '/applicant/load-districts/',
            data: {'city_id': kota.split('_')[0]},
            success: function (data) {
                $('#id_kecamatan').empty();
                $.each(data, function (index, item) {
                    $('#id_kecamatan').append(`<option value="${item[0]}">${item[1]}</option>`);
                });
                $("#id_kecamatan").val(kecamatan);
            }
        });

        // Load and set the kelurahan field
        $.ajax({
            type: 'GET',
            url: '/applicant/load-subdistricts/',
            data: {'district_id': kecamatan.split('_')[0]},
            success: function (data) {
                $('#id_kelurahan').empty();
                $.each(data, function (index, item) {
                    $('#id_kelurahan').append(`<option value="${item[0]}">${item[1]}</option>`);
                });
                $("#id_kelurahan").val(kelurahan).trigger('change');
            }
        });
    }
}

$(document).ready(function () {
    $('#id_provinsi, #id_kota, #id_kecamatan, #id_kelurahan').select2();

    $("#id_provinsi").change(function () {
        $.ajax({
            type: 'GET',
            url: '/applicant/load-cities/',
            data: {
                'province_id': $(this).val().split('_')[0]
            },
            success: function (data) {
                $('#id_kota').empty();
                $.each(data, function (index, item) {
                    $('#id_kota').append(`<option value="${item[0]}">${item[1]}</option>`);
                });
            }
        });
    });

    $("#id_kota").change(function () {
        $.ajax({
            type: 'GET',
            url: '/applicant/load-districts/',
            data: {
                'city_id': $(this).val().split('_')[0]
            },
            success: function (data) {
                $('#id_kecamatan').empty();
                $.each(data, function (index, item) {
                    $('#id_kecamatan').append(`<option value="${item[0]}">${item[1]}</option>`);
                });
            }
        });
    });

    $("#id_kecamatan").change(function () {
        $.ajax({
            type: 'GET',
            url: '/applicant/load-subdistricts/',
            data: {
                'district_id': $(this).val().split('_')[0]
            },
            success: function (data) {
                $('#id_kelurahan').empty();
                $.each(data, function (index, item) {
                    $('#id_kelurahan').append(`<option value="${item[0]}">${item[1]}</option>`);
                });
            }
        });
    });
});