const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;


function deleteQuiz(id){
    let btnConfirm = document.getElementById('btn_confirm_delete');
    btnConfirm.replaceWith(btnConfirm.cloneNode(true));
    $('#btn_confirm_delete').click(()=>{
        $.ajax({
            url: `/quizzes/${id}/delete`,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrf
            },
            success: function(response){
                if (response.success){
                    document.getElementById(`quiz_${id}`).remove();
                }else{
                    showError('Something went wrong...');
                }
            },
            error: function(xhr, status, error){
                showError(error);
            }
        });
    });
    const toastEl = document.getElementById('toast_confirm_delete');
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

