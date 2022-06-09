var test = function (questions, people) {
    var w = document,
        container = document.getElementById('test-container');
    
    var c = function (n, h) {
        var e = w.createElement(n);
        if (h)
            e.innerHTML = h;
        return e;
    };
    HTMLElement.prototype.add = function (e) {
        this.appendChild(e);
    }
    var data = [];
    for (var i = 0; i < people.length; i++) {
        var s = "", p = people[i];
        for (var j in p.answers) {
            var a = p.answers[j];
            s += j+"/";
        }
        data.push(s);
    }
    var form = c('form');
    // Question part
    for (var i = 0; i < questions.length; i++) {
        var q = questions[i],
            e = c('div', "<h3>"+q.value+"</h3>");
        var ul = c('ul');
        for (var a in q.alternatives) {
            var li = w.createElement('div');
            li.className = "form-group";
            var d = data[i]; 
            li.innerHTML = '<label class="radio"><input type="radio"'+
                ' name="question-'+i+'" value="'+d+'"/> '+q.alternatives[a]+'</label>';
            ul.appendChild(li);
        }
        e.appendChild(ul);
        form.appendChild(e);
    }
    var b = c('button', 'Svar');
    b.className = "btn btn-nabla-blue-dark btn-lg";
    form.add(b);
    container.add(form);

    form.addEventListener("submit", function (e) {
        var ans = new FormData(this);
        var result = [];
        for (var j = 0; j < questions.length; j++) {
            var value = ans.get('question-'+j);
            if (value) {
                var d = value.split("/");
                for (var i = 0; i < d.length; i++) {
                    result[i] += parseInt(d[i]);
                }
            }
        }
        var winner = 0;
        for (var i = 0; i < result.length; i++) {
            if (result[i] > result[winner]) {
                winner = i;
            }
        }

        alert("Du ble:"+people[winner].name+"\n"+people[winner].text);
        
        e.preventDefault();
    });
    

};
