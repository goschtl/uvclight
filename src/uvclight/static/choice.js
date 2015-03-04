  $(document).ready(function() {
   
    $.each($('select.alternative-choice'), function() {
        input_value = $(this).next().children().val();
        if (input_value == '')
          {
            $(this).next().hide();
            $(this).append(
                '<option class="alt-opt" id="alternative-choice-opt" value=""> Sonstiges </option>')
          }
        else
          {
            $(this).next().show();
            $(this).append(
                '<option class="alt-opt" id="alternative-choice-opt" selected="selected" value=""> Sonstiges </option>')
          }
    }
   
    )


    $('select.alternative-choice').change(function(e) {
        if ($(this).find("option:selected").attr('class') == 'alt-opt') {
            $(this).next().show('slow')
            //$('input.alternative-input').show('slow');
        }
        else {
            $(this).next().children().val('');
            $(this).next().hide();
            //$('input.alternative-input').val('')
            //$('input.alternative-input').hide();
        }
    });

  });

