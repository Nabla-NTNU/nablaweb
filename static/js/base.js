
if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    var update = function () {
        weeks = Math.floor((timer) / (3600*24*7), 10);
        days = Math.floor((timer % (3600*24*7)) / (3600*24), 10);
        hours = Math.floor((timer % (3600*24)) / 3600, 10);
        minutes = Math.floor((timer % 3600) / 60, 10);
        seconds = Math.floor(timer % 60, 10);

        hours = hours < 10 ? "0" + hours : hours;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        var clock = hours + ":" +minutes + ":" + seconds;

        if (days != 0) {
            clock = days + " dager " + clock;
        }

        if (weeks != 0) {
          clock = weeks + " uker " + clock;
        }


        display.text(clock);

        if (--timer < 0) {
            timer = 0;
        }
    };
    update();
    setInterval(update, 1000);
}

