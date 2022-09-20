
$("#dt-table tr").click(function(){
    $(this).addClass('selected').siblings().removeClass('selected');    
    var value_id=$(this).find('td:first').html();
    $('input[name="submit_number"]').val(value_id);

    // alert(value);   
  });