var ip_address = document.getElementById('id_ip_address');
var quantity = document.getElementById('id_quantity');
var errorlist = document.getElementsByClassName('errorlist')[0];
var reset = document.getElementById('reset');
var submit = document.getElementById('submit');

function resetFields() {
    ip_address.setAttribute('value', '');
    quantity.setAttribute('value', '');
    ip_address.focus();
    if (errorlist) errorlist.style.display = 'none';
}

function verifyValues() {
    var ip = ip_address.value;
    var qty = quantity.value;
    var opt = document.querySelector('input[name=option]:checked').value;
    var oct = parseInt(ip.split('.')[0]);
    if (oct === 0) {
        alert('Class A - 0 is reserved as a part of the default address.');
        ip_address.focus();
        return false;
    }
    else if (oct >= 1 && oct <= 126) {
        if ((opt === 'subnets' && qty > 8388608) || (opt === 'hosts' && qty > 8388606)) {
            alert('Invalid quantity.');
            quantity.focus();
            return false;
        }
    }
    else if (oct === 127) {
        alert('Class A - 127 is reserved for internal loopback testing.');
        ip_address.focus();
        return false;
    }
    else if (oct >= 128 && oct <= 191) {
        if ((opt === 'subnets' && qty > 32768) || (opt === 'hosts' && qty > 32766)) {
            alert('Invalid quantity.');
            quantity.focus();
            return false;
        }
    }
    else if (oct >= 192 && oct <= 223) {
        if ((opt === 'subnets' && qty > 128) || (opt === 'hosts' && qty > 126)) {
            alert('Invalid quantity.');
            quantity.focus();
            return false;
        }
    }
    else if (oct >= 224 && oct <= 239) {
        alert('Class D - Used for multicast. Multicast IP addresses have their first octets in the range 224 to 239.');
        ip_address.focus();
        return false;
    }
    else if (oct >= 240 && oct <= 255) {
        alert('Class E - Reserved for future use and includes the range of addresses with a first octet from 240 to 255.');
        ip_address.focus();
        return false;
    }
    return true;
}

reset.onclick = resetFields;
submit.onclick = verifyValues;