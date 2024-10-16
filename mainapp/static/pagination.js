let queries = {};
let currPageNums = {};

function getCurrPageNum(content){
    if (!currPageNums.hasOwnProperty(content)){
        currPageNums[content] = 1;
    }
    return currPageNums[content];
}

function search(content){
    queries[content] = $(`#${content}_search`).val();
    getPage(content, 1);
}

function reset(content){
    queries[content] = "";
    $(`#${content}_search`).val("")
    getPage(content, 1);
}

function getPage(content, pageNum){
    let spinner = $(`#${content}_spinner`)[0];
    spinner.hidden = false;
    if (!queries.hasOwnProperty(content)){
        queries[content] = "";
    }
    $.ajax({
        url: window.location.href,
        type: "GET",
        data: {
            'content': content,
            'page': pageNum,
            'query': queries[content]
        },
        success: (data)=> {
            document.getElementById(`${content}_container`).innerHTML = data;
            currPageNums[content] = pageNum;
        },
        error: (xhr, status, error) => {
            showError(error);
        }
    }).always(()=>{
        spinner.hidden = true;
    });
}

