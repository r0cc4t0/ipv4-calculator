from django import forms


class IndexForm(forms.Form):

    ip_address = forms.GenericIPAddressField(label='IP Address', label_suffix='', protocol='ipv4', widget=forms.TextInput(
        attrs={'placeholder': 'Enter an IP Address', 'autofocus': 'autofocus'}))

    quantity = forms.IntegerField(label='Quantity', label_suffix='', min_value=2, max_value=8388608,
                                  widget=forms.NumberInput(attrs={'placeholder': 'Enter a Quantity'}))

    option = forms.ChoiceField(label='Options', label_suffix='', choices=[('subnets', 'Subnets'), ('hosts', 'Hosts')],
                               initial='subnets', widget=forms.RadioSelect())
