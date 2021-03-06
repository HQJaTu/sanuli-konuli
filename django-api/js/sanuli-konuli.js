let konuli_word_length = null;
let konuli_waiting_for_board = false;
let konuli_retries = null;

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
<div style="position:absolute;display:grid;left: 60%;width:290px;color:white;margin-left: -20px;">
  <h3>Sanuli-Konuli
    <div style="margin-top:50px;position: relative;display: inline-block;">
      <img src="${s_url}/js/refresh-svgrepo-com-32px.png" style="position: absolute;top: -25px;cursor: pointer;" onclick="javascript:konuli_game_round();">
    </div>
  </h3>
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
        konuli_retries = null;
        const [row_idx, greens, grays, yellows] = state;
        if (row_idx === 0 || (greens === null && yellows === null)) {
            konuli_get_initial_word(grays);
        } else {
            if (!greens && !yellows) {
                // Oh! Initial has nothing.
                konuli_get_initial_word(grays);
            } else {
                konuli_match_word(greens, grays, yellows);
            }
        }
    } else if (typeof state == "boolean") {
        if (konuli_waiting_for_board) {
            // If game is solved, poll once a second to see if user
            let delay = 1000;
            if (konuli_retries === null) {
                konuli_retries = 0;
            } else {
                ++konuli_retries;
                if (konuli_retries > 30) {
                    // 30 seconds have passed, relax a lot
                    delay = 60000; // minute
                }
            }
            //console.log(`Retry: ${konuli_retries} Konuli waiting for user to go for a new game`)
            konuli_delay(() => {
                konuli_game_round()
            }, delay)();
        }
    }
}

konuli_determine_state = () => {
    /*
    * Return values:
    * - null: error
    * - true: solved
    * - false: bad word
    * - array: [current row index 0-5, greens, grays, yellows]
    */
    const msg = konuli_get_message();

    if (msg) {
        if (msg.startsWith("L??ysit sanan!") || msg.startsWith("L??ysit p??iv??n sanulin")) {
            $("#konuli-words").empty();
            if (!konuli_waiting_for_board) {
                console.log("Konuli: Sanuli solved!");
            }
            konuli_waiting_for_board = true;

            return true;
        } else if (msg.startsWith("Ei sanulistalla.")) {
            console.log("Konuli: Bad word.")

            // Wait a second, then erase.
            konuli_delay(() => {
                konuli_clear_word()
            }, 1000)();

            return false;
        } else if (msg.startsWith("Sana oli ")) {
            if (!konuli_waiting_for_board) {
                console.log("Konuli: Game over - failed")
            }
            konuli_waiting_for_board = true;

            return false;
        }

        console.log(`Konuli: XXX Unknown message "${msg}"!`)

        return null;
    }

    // Ok. Seems good to go.
    // Find current row number.
    konuli_waiting_for_board = false;
    const current_tiles = $(".tile.current");
    if (!current_tiles) {
        console.log("Konuli internal error: Confusion! Current row missing.")

        return null;
    }

    // Determine current row and collect game status.
    const current_row = current_tiles[0].parentNode;
    konuli_word_length = current_row.childElementCount;
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
    let green_cnt = 0;
    prev_row_tiles.each((idx, elem) => {
        if ($(elem).hasClass("correct")) {
            greens += elem.textContent;
            ++green_cnt;
        } else {
            greens += ".";
        }
    });
    console.log(`Konuli debug: greens: "${greens}"`)

    // Get yellows from previous row
    let yellows = '';
    let yellow_cnt = 0;
    prev_row_tiles.each((idx, elem) => {
        if ($(elem).hasClass("present")) {
            yellows += elem.textContent;
            ++yellow_cnt;
        } else {
            yellows += ".";
        }
    });
    console.log(`Konuli debug: yellows: "${yellows}"`)

    if (!green_cnt && !yellow_cnt) {
        greens = null;
        yellows = null;
    }

    return [row_idx, greens, grays, yellows];
}

konuli_get_message = () => {
    const message = $(".message");
    if (!message.length) {
        return '';
    }

    return message[0].innerHTML;
}

konuli_get_initial_word = (grays) => {
    // Docs: https://api.jquery.com/jQuery.ajax/
    let url = `${s_url}/api/v1/words/${s_lang}-${konuli_word_length}`;
    if (grays !== null) {
        url += `?excluded=${grays}`
    }
    $.ajax({
        url: url,
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
${resp['word']} <button onclick="javascript:return konuli_add_word('${resp['word']}');">Lis????</button>
`;
    word_list.empty();
    word_list.html(word_html);
}

konuli_match_word = (greens, grays, yellows) => {
    // Docs: https://api.jquery.com/jQuery.ajax/
    $.ajax({
        url: `${s_url}/api/v1/words/${s_lang}-${konuli_word_length}`,
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
    if (!resp["found_matches"]) {
        let word_html = `
<p>Sanastossa ei sopivia sanoja!</p>
`;
        word_list.empty();
        word_list.html(word_html);

        return
    }

    const chosen_word = resp['word'];
    let word_html = `
${chosen_word} <button onclick="javascript:return konuli_add_word('${chosen_word}');">Lis????</button><br/>
`;
    for (let idx in resp['other_words']) {
        const word = resp['other_words'][idx];
        if (word !== chosen_word) {
            word_html += `
${word} <button onclick="javascript:return konuli_add_word('${word}');">Lis????</button><br/>
`;
        }
    }
    if (resp['prime_words'].length < 10) {
        for (let idx in resp['prime_words']) {
            const word = resp['prime_words'][idx];
            if (word !== chosen_word) {
                word_html += `
${word} <button onclick="javascript:return konuli_add_word('${word}');">Lis????</button><br/>
`;
            }
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

konuli_clear_word = () => {
    const event_params = {'key': 'Backspace', 'keyCode': 8};
    for (let idx = 0; idx < konuli_word_length; ++idx) {
        konuli_delay(() => {
            window.dispatchEvent(new KeyboardEvent('keydown', event_params));
        }, 10)();
    }
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
