konuli_dynamicallyLoadScript = (url) => {
    var script = document.createElement("script");  // create a script DOM node
    script.src = url;  // set its src to the provided URL
    script.onload = konuli_init;

    document.head.appendChild(script);  // add it to the end of the head section of the page (could change 'head' to 'body' to add it to the end of the body section instead)
}

konuli_init = () => {
    // Move board to left a bit to make room for our solver
    const board = $(".board-6:last");
    board.css("left", "30%");

    // Introduce the new div
    const konuliDiv = `
<div style="position:absolute; display:grid; left:55%; width:290px;color:white;">
  <h3>Sanuli-Konuli<button onclick="javascript:konuli_game_round();">R</button></h3>
  <div id="konuli-words" style="overflow-y:scroll; height:420px;position: relative;width: 150px;"></div>
</div>
`.trim()
    board.after(konuliDiv);

    // Kick the game on
    konuli_game_round();
}

konuli_game_round = () => {
    const state = konuli_determine_state();
    if (Array.isArray(state)) {
        const [row_idx, greens, grays, yellows] = state;
        if (row_idx === 0) {
            konuli_get_initial_word();
        } else {
            if (!greens && !yellows) {
                // Oh! Initial has nothing.
                konuli_get_initial_word(grays);
            } else {
                konuli_match_word(greens, grays, yellows);
            }
        }
    }
}

konuli_determine_state = () => {
    const msg = konuli_get_message();

    if (msg) {
        if (msg.startsWith("Löysit sanan!") || msg.startsWith("Löysit päivän sanulin")) {
            $("#konuli-words").empty();
            console.log("Konuli: Sanuli solved!");

            return null;
        } else if (msg.startsWith("Ei sanulistalla.")) {
            console.log("Konuli: Bad word.")

            return false;
        }

        console.log(`Konuli: XXX Unknown message "${msg}"!`)

        return null;
    }

    // Ok. Seems good to go.
    // Find current row number.
    const current_tiles = $(".tile.current");
    if (!current_tiles) {
        console.log("Konuli internal error: Confusion! Current row missing.")

        return null;
    }

    // Determine current row and collect game status.
    const current_row = current_tiles[0].parentNode;
    const board = $(".board-6:last");
    let row_idx = null;
    let row_div = true;
    let prev_row_div = null;
    let row_matched = false;
    for (row_idx = 0; row_div; ++row_idx) {
        row_div = board[0].childNodes[row_idx];
        if (row_div && row_div === current_row) {
            row_matched = true;
            console.log(`Konuli current row: ${row_idx}`)

            break;
        }
        prev_row_div = $(row_div);
    }
    if (!row_matched) {
        console.log("Konuli internal error: Confusion! Current row cannot be matched.")

        return null;
    }

    // Beginning of game?
    if (row_idx === 0) {
        console.log("Konuli debug: Game begin.")

        return [row_idx, null, null, null];
    }

    // Get all grays in the board
    const gray_tiles = board.find(".absent");
    let grays = '';
    gray_tiles.each((idx, elem) => {
        grays += elem.textContent;
    });
    console.log(`Konuli debug: grays: "${grays}"`)

    // Get greens from previous row
    const prev_row_tiles = prev_row_div.find(".tile");
    let greens = '';
    prev_row_tiles.each((idx, elem) => {
        if ($(elem).hasClass("correct")) {
            greens += elem.textContent;
        } else {
            greens += ".";
        }
    });
    console.log(`Konuli debug: greens: "${greens}"`)

    // Get yellows from previous row
    let yellows = '';
    prev_row_tiles.each((idx, elem) => {
        if ($(elem).hasClass("present")) {
            yellows += elem.textContent;
        } else {
            yellows += ".";
        }
    });
    console.log(`Konuli debug: yellows: "${yellows}"`)

    return [row_idx, greens, grays, yellows];
}

konuli_get_message = () => {
    const message = $(".message");
    if (!message.length) {
        return '';
    }

    return message[0].innerHTML;
}

konuli_get_initial_word = () => {
    // Docs: https://api.jquery.com/jQuery.ajax/
    $.ajax({
        url: `${s_url}/api/v1/words/${s_lang}-${s_wl}`,
        headers: {
            "Authorization": `Token ${s_key}`
        },
        context: document.body
    }).done((resp) => {
        konuli_show_initial_word(resp);
    });
}

konuli_show_initial_word = (resp) => {
    const word_list = $("#konuli-words");
    const word_html = `
${resp['word']} <button onclick="javascript:return konuli_add_word('${resp['word']}');">Lisää</button>
`;
    word_list.empty();
    word_list.html(word_html);
}

konuli_match_word = (greens, grays, yellows) => {
    // Docs: https://api.jquery.com/jQuery.ajax/
    $.ajax({
        url: `${s_url}/api/v1/words/${s_lang}-${s_wl}`,
        headers: {
            "Authorization": `Token ${s_key}`
        },
        context: document.body,
        type: "POST",
        data: {
            "match_mask": greens,
            "excluded_letters": grays,
            "known_letters": yellows
        }
    }).done((resp) => {
        konuli_show_matching_words(resp);
    });
}

konuli_show_matching_words = (resp) => {
    const word_list = $("#konuli-words");
    const chosen_word = resp['word'];
    let word_html = `
${chosen_word} <button onclick="javascript:return konuli_add_word('${chosen_word}');">Lisää</button><br/>
`;
    for (let idx in resp['prime_words']) {
        const word = resp['prime_words'][idx];
        if (word !== chosen_word) {
            word_html += `
${word} <button onclick="javascript:return konuli_add_word('${word}');">Lisää</button><br/>
`;
        }
    }
    word_list.empty();
    word_list.html(word_html);
}

konuli_add_word = (word) => {
    console.log(`Konuli adding word "${word}".`)
    const keypresses = word.split() + String.fromCharCode(13);

    for (let key_idx in keypresses) {
        const key = keypresses[key_idx];
        let event_params;
        // NOTE: Need to dispatch browser native event!
        if (key === String.fromCharCode(13)) {
            //console.log(`Konuli send: Enter`)
            event_params = {'key': 'Enter', 'keyCode': 13};
        } else {
            //console.log(`Konuli send: ${key}`)
            event_params = {'key': key.toUpperCase()};
        }

        konuli_delay(() => {
            window.dispatchEvent(new KeyboardEvent('keydown', event_params));
        }, 10)();
    }

    konuli_delay(() => {
        konuli_game_round();
    }, 200)();

    return false;
}

konuli_delay = (fn, ms) => {
    // Code from: https://stackoverflow.com/a/1909508/1548275
    let timer = 0;
    return (...args) => {
        clearTimeout(timer)
        timer = setTimeout(fn.bind(this, ...args), ms || 0)
    }
}

konuli_dynamicallyLoadScript(`${s_url}/js/jquery-3.6.0.js`);
