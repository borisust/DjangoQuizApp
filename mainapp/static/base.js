
function showError(text){
    $('#error_message').html(text);
    const toastEl = document.getElementById('toast_error');
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}
