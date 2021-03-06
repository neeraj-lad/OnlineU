/**
    This library contains functions for converting markdown to HTML
**/

function randomValue(a, b) {
    /**
        Returns a random integer on the interval [a, b)
    **/
    a = a || 0;
    b = b || 100;

    return Math.floor(Math.random() * (b - a) + a);
};

function variableIndex(string) {
    /**
        Returns the first index of a variable in a string, if present
        Returns -1 otherwise
    **/
    var re = /{[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]}/;
    var result = re.exec(string);
    if (result) {
        return result.index;
    }
    return -1;
};

function isChoice(string) {
    /**
        Returns true if the string is a multiple choice option
    **/
    var re = /^[0-9]*\)/;
    var result = re.exec(string);
    return result;
};

function htmlify(source, target) {
    /**
        Get text from source
        Compile it to HTML
        Insert it into target
    **/

    target = target || source;

    var markdown = source.value;
    var html = "<form action=''>";
    var lines = markdown.split("\n");
    var variables = {}

    // Compile to html
    var line, hCount, index, varName, value, number;
    for (var i = 0; i < lines.length; i++) {
        line = lines[i];
        line = line.trim();

        // Check for headers
        hCount = 0;
        while (line[0] === "#") {
            hCount++;
            line = line.substr(1, line.length);
        }
        if (hCount > 0) {
            html = html + "<h" + hCount + ">";
            html = html + line;
            html = html + "</h" + hCount + ">";
            continue;
        }

        // Choice for multiple choice option
        if (isChoice(line)) {
            index = line.indexOf(")") + 1;
            number = line[index - 2];
            value = line.substr(index, line.length);
            html = html + "<input type='radio' name='answer' value='" + number + "'><p style='display:inline-block;'>" + value + "</p><br>"
            continue;
        }

        // Check for variables
        while (true) {
            index = variableIndex(line);
            
            if (index < 0) {
                break;
            }
            if (index > -1) {
                varName = line[index + 1];
                if (varName in variables) {
                    value = variables[varName];
                }
                else {
                    value = randomValue();
                    variables[varName] = value;
                }

                line = line.substr(0, index) + "<strong>" + value + "</strong>" + line.substr(index + 3, line.length);
            }
        }

        // Paragraph
        html = html + "<p>" + line + "</p>";

        // End form
        html = html + "</form>"

    }

    // Insert compiled HTML into target element
    target.innerHTML = html;
};

function link(source, target) {
    /**
        Automatically compile from source to target when the user types
    **/
    source.onkeyup = function() {
        htmlify(source, target);
    };
};