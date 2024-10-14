let questionIndex = 1;

$('#question_1').addClass('show');

const showQuestion = ()=>{
    const newEl = $(`#question_${questionIndex}`)[0];
    new bootstrap.Collapse(newEl);
};

function selectQuestion(index){
    if (index == questionIndex) return;
    const currEl = $(`#question_${questionIndex}`)[0];
    questionIndex = index;
    currEl.addEventListener('hidden.bs.collapse', showQuestion);
    new bootstrap.Collapse(currEl);
}

function nextQuestion(){
    selectQuestion(questionIndex+1);
}

function prevQuestion(){
    selectQuestion(questionIndex-1);
}

