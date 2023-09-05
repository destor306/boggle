const $guessinput = $("input[name='word']")
const $sizeinput = $("input[name='size']")

let $msg = $(".msg"); // Select the <p> element with the class "msg"
let $score = $(".scores"); // select the <p> element with the class "score"
let $time = $(".time"); // select the <p> element with the class "time"
let $high_score = $(".hi_scores");
let $start_btn = $(".start_btn")
let time_intval;

class boggleGame{
    constructor(board, time){
        this.board = board;
        this.time = time;
        this.score = 0;
        this.board_id = $("#board_id");
        this.time_intval ;
        this.words= new Set();
        // when submit is triggered, send guess value to submit_form
        $("form").on("submit",  this.submit_guess_form.bind(this));
        $("#board-btn").on("click", this.submit_size_form.bind(this));
        $start_btn.on("click", this.play_game.bind(this));
    }

    play_game(evt){
        evt.preventDefault();
        this.time_intval = setInterval(this.tictok.bind(this), 1000)
    }
    show_message(msg){
        $msg.text(msg);
    }

    update_scores(word){
        let score = parseInt($score.text());
        console.log(score)
        score = score+ word.length;
        $score.text(score);
    }
    /* Update Timer on screen */
    showTime(){
        $time.text(this.time);
    }

    /* tiktoking the time */
    tictok(){
        this.time -=1
        this.showTime();
        if (this.time === 0){
            clearInterval(this.time_intval);
            $("form").hide(); // disable guess 
            let score = parseInt($score.text());
            this.post_score(score);
            
        }
    }
    async submit_size_form(evt){
        
        let size = parseInt($sizeinput.val());
        console.log(size);
        $sizeinput.val("");
        this.board_id.empty();
        try{
            const res = await axios.post('/make-board', {size: size})
            const new_board = res.data.board;
            
            for (let row of new_board){
                const $row = $("<tr>");
                for(let col of row){
                    const $cell = $("<td>").text(col);
                    $row.append($cell);
                }
                this.board_id.append($row);
            }
            this.board_id.show();
        }
        catch(e){
            console.log(e);
        }
    }

    async submit_guess_form(evt){
        evt.preventDefault();
        let guess = $guessinput.val();
        $guessinput.val("");
        try {
            const res = await axios.get('/check-word', { params: { word: guess } });
            const word_res = res.data.result;
            
           // console.log($msg.val())
            if (word_res === "not-word") {
                this.show_message(`${guess} is not a word`);
            } else if (word_res === "not-on-board") {
                this.show_message(`${guess} is not on board`);
            } else if (word_res === "ok") 
            {
                this.show_message(`Added: ${guess}`);
                this.update_scores(guess);
            }
        } catch (error) {
            console.error(error);
            // Handle the error
        }
    }
    async  post_score(score){
        try{
            const res = await axios.post('/post-score', {score: score})
            console.log(res.data.highest);
            $high_score.text(res.data.highest);        
        }
        catch(e){
            console.log(e);
        }
    }
    
}




