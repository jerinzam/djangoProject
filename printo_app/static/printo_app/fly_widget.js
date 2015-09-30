FlyWidget = {
    getValue: function(choice) {
        var value = choice.data('value');
        console.log("creating a new choice")

        if (value == 'create') {
            choice.html(this.input.val())

            $.ajax(this.autocomplete.url, {
                async: false,
                type: 'post',
                data: {
                    'name': this.input.val(),
                },
                success: function(text, jqXHR, textStatus) {
                    value = text;
                }
            });

            choice.data('value', value);
        }

        return value;
    }
}

$(document).bind('yourlabsWidgetReady', function() {
    // Instanciate decks with RemoteAutocompleteWidget as override for all widgets with
    // autocomplete 'remote'.
    console.log("here")
    $('body').on('initialize', '.autocomplete-light-widget[data-widget-bootstrap=fly-widget]', function() {
        $(this).yourlabsWidget(FlyWidget);
    });
});