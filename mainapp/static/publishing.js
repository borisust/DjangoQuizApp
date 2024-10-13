// password field control
function blockPasswordField(bool){
    $('#id_password')[0].disabled = bool;
    $('#div_id_password')[0].hidden = bool;
}
$('#id_access_0').click(()=>blockPasswordField(true));
$('#id_access_1').click(()=>blockPasswordField(false));
$('#id_access_2').click(()=>blockPasswordField(true));

if ($('#id_access_1').is(':checked') == false){
    blockPasswordField(true);
}



