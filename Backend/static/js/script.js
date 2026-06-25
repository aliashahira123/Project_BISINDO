function update(){
    fetch('/sentence')
    .then(r=>r.json())
    .then(d=>{
        document.getElementById("sentence").innerText = d.sentence;
    });
}

function reset(){
    fetch('/reset').then(()=>{
        document.getElementById("sentence").innerText = "";
    });
}

function space(){
    fetch('/space');
}

setInterval(update, 400);