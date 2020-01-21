function resetFields() {
    $('#id_ip_address').attr('value', '');
    $('#id_quantity').attr('value', '');
    $('#id_ip_address').focus();
    $('.errorlist').hide();
}

function verifyValues() {
    if ($('#id_ip_address').val() !== '') {
        var ip = $('#id_ip_address').val();
    }
    var qty = $('#id_quantity').val();
    var opt;
    $('#id_option_0').is(':checked') ? opt = $('#id_option_0').val() : opt = $('#id_option_1').val();
    var oct = ip.split('.')[0];

    if (oct == 0) {
        alert('Class A - 0 is reserved as a part of the default address.');
        $('#id_ip_address').focus();
        return false;
    }
    else if (oct >= 1 && oct <= 126) {
        if ((opt === 'subnets' && qty > 8388608) || (opt === 'hosts' && qty > 8388606)) {
            alert('Invalid quantity.');
            $('#id_quantity').focus();
            return false;
        }
    }
    else if (oct == 127) {
        alert('Class A - 127 is reserved for internal loopback testing.');
        $('#id_ip_address').focus();
        return false;
    }
    else if (oct >= 128 && oct <= 191) {
        if ((opt === 'subnets' && qty > 32768) || (opt === 'hosts' && qty > 32766)) {
            alert('Invalid quantity.');
            $('#id_quantity').focus();
            return false;
        }
    }
    else if (oct >= 192 && oct <= 223) {
        if ((opt === 'subnets' && qty > 128) || (opt === 'hosts' && qty > 126)) {
            alert('Invalid quantity.');
            $('#id_quantity').focus();
            return false;
        }
    }
    else if (oct >= 224 && oct <= 239) {
        alert('Class D - Used for multicast. Multicast IP addresses have their first octets in the range 224 to 239.');
        $('#id_ip_address').focus();
        return false;
    }
    else if (oct >= 240 && oct <= 255) {
        alert('Class E - Reserved for future use and includes the range of addresses with a first octet from 240 to 255.');
        $('#id_ip_address').focus();
        return false;
    }
    return true;
}

$(document).ready(function () {
    $('#reset').click(resetFields);
    $('#submit').click(verifyValues);
});