const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;


function deleteQuiz(id){
    const modal = new bootstrap.Modal(document.getElementById('modal_confirm_delete'));
    $('#btn_confirm_delete')[0].onclick = ()=>{
        $.ajax({
            url: `/quizzes/${id}/deletett`,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrf
            },
            success: function(response){
                if (response.success){
                    modal.hide();
                    getPage('saved_quizzes', getCurrPageNum('saved_quizzes'));
                }else{
                    showError('Something went wrong...');
                }
            },
            error: function(xhr, status, error){
                showError(error);
            }
        });
    };
    modal.show();
}

