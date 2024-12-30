$(document).ready(function(){
    const games=JSON.parse(document.getElementById('arena_game').textContent)
    const player=JSON.parse(document.getElementById('player').textContent)
    const fight_n=JSON.parse(document.getElementById('fight_n').textContent)
    const bet_s=JSON.parse(document.getElementById('betstatus').textContent)
    
    
    // var socket= new WebSocket('ws://'+window.location.host+'/ws/arena/'+games);    
    $(document).on('click','.bet',function(){
        amount = $(this).val()
        $('#mybet').val(amount)
    })
    
    $('.clearbet').click(function(){
        $('#mybet').val(0)
    })
    
    
    // socket.onmessage =function(e){ 
    
    
    $('.notif').html('')
    // result=JSON.parse(e.data)
    // if(result.winner == 'MERON'){
    //     $('.meron_box').addClass('meron-win')
    //     $('.wala_box').removeClass('wala-win')
    //     $('.draw_box').removeClass('draw-win')
    //     $('#meron-win').attr('hidden',false)
    //     $('#wala-win').attr('hidden',true)
    
    // }else if(result.winner == 'WALA'){
    //     $('.meron_box').removeClass('meron-win')
    //     $('.draw_box').removeClass('draw-win')
    //     $('.wala_box').addClass('wala-win')
    //     $('#meron-win').attr('hidden',true)
    //     $('#wala-win').attr('hidden',false)
    
    // }else if(result.winner == 'DRAW'){
    //     $('.draw_box').addClass('draw-win')
    //     $('.meron_box').removeClass('meron-win')
    //     $('.wala_box').removeClass('wala-win')
    //     $('#meron-win').attr('hidden',true)
    //     $('#wala-win').attr('hidden',true)
    //     $('#draw-win').attr('hidden',false)
    
    // }else{
    //     $('.meron_box').removeClass('meron-win')
    //     $('.wala_box').removeClass('wala-win')
    //     $('.draw_box').removeClass('draw-win')
    //     $('#draw-win').attr('hidden',true)
    //     $('#meron-win').attr('hidden',true)
    //     $('#wala-win').attr('hidden',true)
    // }
    
    // $('#fid').val(result.fightid)
    // $('#wbalance').val(result.mywallet)
    // $('.wbalance').text(result.mywallet)
    
    // if(result.bet_status == 'OPEN'){
    //     $('.betsub').removeClass('disabled')
    //     $('.betlong').removeClass('disabled')
    //     notif='<span class="badge bg-success fw-bolder fs-4 " >OPEN</span>'
    // }else if(result.bet_status == 'LAST CALL'){
    //     $('.betsub').removeClass('disabled')
    //     $('.betlong').removeClass('disabled')
    //     notif='<span class="badge bg-warning text-danger fw-bolder fs-4  blink callnotif" >LAST CALL</span>'
    // }else if(result.bet_status == 'CLOSED'){
    //     $('.betsub').addClass('disabled')
    //     $('.betlong').addClass('disabled')
    //     notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
    // }else if(result.bet_status == 'CLOSING'){
    //     $('.betsub').addClass('disabled')
    //     $('.betlong').addClass('disabled')
    //     notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
    // }else if(result.bet_status == 'DECLARED'){
    //     $('.betsub').addClass('disabled')
    //     $('.betlong').addClass('disabled')
    //     notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
    // }else if(result.bet_status == 'DONE'){
    //     notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
    //     $('.betsub').addClass('disabled')
    //     $('.betlong').addClass('disabled')
    //     $('.meron_box').removeClass('meron-win')
    //     $('.wala_box').removeClass('wala-win')
    //     $('.draw_box').removeClass('draw-win')
    // }
    
    // $('.notif').append(notif)
    // $('.fnum').text('Fight #: '+result.fightnum)
    // $('.meronpayout').text(result.meronpayout.toFixed(2))
    // $('.walapayout').text(result.walapayout.toFixed(2))
    // $('.merontowin').text(result.merontowin.toFixed(2))
    // $('.walatowin').text(result.walatowin.toFixed(2))
    // $('#wbalance').val(result.mywallet)
    // $('.wbalance').text(result.mywallet.toLocaleString('en'))
    
    
    // meron = $('.meron-val').val()
    // $('.meron_bet').text(result.dmeron)
    // $('.meron-val').val(result.dmeron)
    // $('.meron_bet').each(function () {
    //     $(this).prop('Counter',meron).animate({
    //         Counter: $(this).text()
    //     }, {
    //         duration: 1000,
    //         easing: 'swing',
    //         step: function (now) {
    //             $(this).text(Math.ceil(now).toLocaleString('en'));
    //         }
    //     })
    // });
    
    // wala = $('.wala-val').val()
    // $('.wala_bet').text(result.dwala)
    // $('.wala-val').val(result.dwala)
    // $('.wala_bet').each(function () {
    //     $(this).prop('Counter',wala).animate({
    //         Counter: $(this).text()
    //     }, {
    //         duration: 1000,
    //         easing: 'swing',
    //         step: function (now) {
    //             $(this).text(Math.ceil(now).toLocaleString('en'));
    //         }
    //     })
    // });
    
    // draw = $('.draw-val').val()
    // $('.mydrawbet').text(result.mydrawbet)
    // $('.draw-val').val(result.mydrawbet)
    // $('.mydrawbet').each(function () {
    //     $(this).prop('Counter',draw).animate({
    //         Counter: $(this).text()
    //     }, {
    //         duration: 2000,
    //         easing: 'swing',
    //         step: function (now) {
    //             $(this).text(Math.ceil(now).toLocaleString('en'));
    //         }
    //     })
    // });
    
    // long = $('.long-val').val()
    // $('.mylongbet').text(result.mylongbet)
    // $('.long-val').val(result.mylongbet)
    // $('.mylongbet').each(function () {
    //     $(this).prop('Counter',long).animate({
    //         Counter: $(this).text()
    //     }, {
    //         duration: 2000,
    //         easing: 'swing',
    //         step: function (now) {
    //             $(this).text(Math.ceil(now).toLocaleString('en'));
    //         }
    //     })
    // });
    
    // $('.mymeronbet').text(result.myMeronBet.toLocaleString('en'))
    // $('.mywalabet').text(result.myWalaBet.toLocaleString('en'))
    // $('.mydrawbet').text(result.mydrawbet.toLocaleString('en'))
    // $('.mylongbet').text(result.mylongbet.toLocaleString('en'))
    // // mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
    // renderTablehistory();
    // renderTablereg();
    // mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
    // }
    
    
    
    
    
    // socket.onopen = function(e){
    
    
    $(document).on('click','.betsub',function(){
        amount=$('#mybet').val()
        betamount=parseFloat(amount)
        fid=$('#fid').val()
        betin=$(this).attr('id')
        wallet=$('#wbalance').val()
        
        if (betamount>=20) {
            if(betamount > wallet){
                Swal.fire({
                    title: "Insufficient Points Balance!",
                    icon: "error"
                });
            }else{
                if(betamount == 0){
                    Swal.fire({
                        title: "No Amount Entered!",
                        icon: "error"
                    });
                }else{
                    Swal.fire({
                        title: "BET "+betin +" : " +betamount+" ?",
                        text: "You're to place a Bet",
                        icon: "warning",
                        showCancelButton: true,
                        confirmButtonColor: "#3085d6",
                        cancelButtonColor: "#d33",
                        confirmButtonText: "Proceed!"
                    }).then((result) => {
                        if (result.isConfirmed) {
                            $('#mybet').val(0)
                            st=$('#betst').val()
                            if(st == 'CLOSE'){
                                Swal.fire({
                                    title: "Betting are Closed!",
                                    icon: "error"
                                });
                            }else{
                                $.ajax({
                                    method:'POST',
                                    url:'../../updatewallet',
                                    data:{amount:amount,ttype:'minus',fid:fid,betin:betin},
                                    success:function(res){
                                        if(res.response == 'success'){
                                            toastr["success"]("Bet successfully!");  
                                        }else if(res.response == 'insufficient'){
                                            Swal.fire({
                                                title: "Insufficient Points Balance!",
                                                icon: "error"
                                            });
                                        }else if(res.response == 'drawlimit'){
                                            Swal.fire({
                                                title: "Draw bet slots has been reach!",
                                                icon: "error"
                                            });
                                        }else{
                                            toastr["error"]("Invalid input!");  
                                        }
                                        fetchData()
                                        // socket.send(JSON.stringify({
                                        // 'amount': betamount,
                                        // 'betin':betin,
                                        // 'player':player,
                                        // 'fight_no':fid,                
                                        // }))
                                    }
                                })
                            }
                        }
                    });
                }    
            }
        }else{
            toastr["error"]("Invalid input!");  
        }
    })
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    $(document).on('click','.betlong',function(){
        amount=$('#mybet').val()
        betamount=parseFloat(amount)
        fid=$('#fid').val()
        betin=$(this).attr('id')
        wallet=$('#wbalance').val()
        if(betin == 'LONGEST'){
            $('#mybet').val(100)
            if (betamount==100) {
                if(betamount > wallet){
                    Swal.fire({
                        title: "Insufficient Points Balance!",
                        icon: "error"
                    });
                }else{
                    if(betamount == 0){
                        Swal.fire({
                            title: "No Amount Entered!",
                            icon: "error"
                        });
                    }else{
                        Swal.fire({
                            title: "BET "+betin +" : " +betamount+" ?",
                            text: "You're to place a Bet",
                            icon: "warning",
                            showCancelButton: true,
                            confirmButtonColor: "#3085d6",
                            cancelButtonColor: "#d33",
                            confirmButtonText: "Proceed!"
                        }).then((result) => {
                            if (result.isConfirmed) {
                                $('#mybet').val(0)
                                st=$('#betst').val()
                                if(st == 'CLOSE'){
                                    Swal.fire({
                                        title: "Betting are Closed!",
                                        icon: "error"
                                    });
                                }else{
                                    $.ajax({
                                        method:'POST',
                                        url:'../../updatewallet',
                                        data:{amount:amount,ttype:'minus',fid:fid,betin:betin},
                                        success:function(res){
                                            fetchData()
                                            if(res.response == 'success'){
                                                Swal.fire({
                                                    title: "Bet successfully!",
                                                    icon: "success"
                                                });
                                            }if(res.response == 'insufficient'){
                                                Swal.fire({
                                                    title: "Insufficient Points Balance!",
                                                    icon: "error"
                                                });
                                            }
                                            // socket.send(JSON.stringify({
                                            // 'amount': betamount,
                                            // 'betin':betin,
                                            // 'player':player,
                                            // 'fight_no':fid,                
                                            // }))
                                        }
                                    })
                                }
                            }
                        });
                    }    
                }
            }else{
                $('#mybet').val(0)
                Swal.fire({
                    title: "Invalid Amount!!",
                    icon: "error"
                });
            }
        }else{
            $('#mybet').val(0)
            Swal.fire({
                title: "Invalid!",
                icon: "error"
            });
        }
    })
    
    
    
    
    // }
    // /////////////////////////////
    
    
    
    
    
    // fight history
    function tablehistory(rows, columns, fightData) {
        const table = document.createElement('table');
        let fightIndex = 0;
        for (let j = 0; j < columns; j++) {
            for (let i = 0; i < rows; i++) {
                const tr = table.rows[i] || table.insertRow();
                const td = tr.insertCell();
                
                if (fightIndex < fightData.length) {
                    const fightNumber = fightData[fightIndex].f_number;
                    const winner = fightData[fightIndex].f_winner;
                    const span = document.createElement('span');
                    span.classList.add('badges');
                    span.textContent = fightNumber;
                    if (winner === 'MERON') {
                        span.classList.add('badge_meron');
                    } else if (winner === 'WALA') {
                        span.classList.add('badge_wala');
                    } else if (winner === 'DRAW') {
                        span.classList.add('badge_draw');
                    } else if (winner === 'CANCELLED') {
                        span.classList.add('badge_cancel');
                    } else{
                        span.classList.add('badge_default');
                    }
                    td.appendChild(span);
                    fightIndex++;
                } else {
                    td.textContent = '';
                }
            }
        }
        return table;
    }
    
    async function fetchFightline() {
        try {
            const gameId = document.getElementById('gameid').value;
            const response = await fetch(`/get-fight-data/${gameId}/`);
            if (!response.ok) {
                throw new Error('Network response was not ok' + response.statusText);
            }
            const fightData = await response.json();
            return fightData;
        } catch (error) {
            alert('Failed to load fight data. Please try again later.');
            return [];
        }
    }
    async function renderTablehistory() {
        const fightData = await fetchFightline();
        if (fightData.length > 0) {
            const container = document.getElementById('tablehistory');
            container.innerHTML = '';
            const table = tablehistory(5, 300, fightData);
            container.appendChild(table);
        } else {
            console.log('No fight data available');
        }
    }
    renderTablehistory();
    // fight history
    
    
    
    // reglahan
    function generateRowIndices(rows, columns) {
        const rowIndices = [];
        for (let i = 0; i < rows; i++) {
            const row = [];
            for (let j = 0; j < columns; j++) {
                row.push(i + 1 + j * rows);
            }
            rowIndices.push(row);
        }
        return rowIndices;
    }
    
    function createStyledTable(rows, columns, fightData) {
        const table = document.createElement('table');
        
        for (let i = 0; i < rows; i++) {
            const tr = table.insertRow();
            for (let j = 0; j < columns; j++) {
                tr.insertCell();
            }
        }
        
        function placeFightsInRow(rowIndices, rowIndex) {
            rowIndices.forEach((tblrowsValue, colIndex) => {
                const fight = fightData.find(fight => fight.f_tblrows === tblrowsValue);
                if (fight) {
                    const td = table.rows[rowIndex].cells[colIndex];
                    const span = document.createElement('span');
                    span.classList.add('badges');
                    span.textContent = fight.f_number;
                    
                    if (fight.f_winner === 'MERON') {
                        span.classList.add('badge_meron');
                    } else if (fight.f_winner === 'WALA') {
                        span.classList.add('badge_wala');
                    } else if (fight.f_winner === 'DRAW') {
                        span.classList.add('badge_draw');
                    } else if (fight.f_winner === 'CANCELLED') {
                        span.classList.add('badge_cancel');
                    } else{
                        span.classList.add('badge_default');
                    }
                    td.appendChild(span);
                }
            });
        }
        
        const rowIndices = generateRowIndices(rows, columns);
        
        rowIndices.forEach((rowIndexSet, rowIndex) => {
            placeFightsInRow(rowIndexSet, rowIndex);
        });
        return table;
    }
    
    async function fetchFightData() {
        try {
            const gameId = document.getElementById('gameid').value;
            const response = await fetch(`/get-fight-data/${gameId}/`);
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            const fightData = await response.json();
            return fightData;
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
            alert('Failed to load fight data. Please try again later.');
            return [];
        }
    }
    
    async function renderTablereg() {
        const fightData = await fetchFightData();
        if (fightData.length > 0) {
            const container = document.getElementById('fighrowtable');
            container.innerHTML = '';
            const rows = 5;
            const columns = 300;
            const table = createStyledTable(rows, columns, fightData);
            container.appendChild(table);
        } else {
            console.log('No fight data available');
        }
    }
    renderTablereg();
    // reglahan
    
    
    
    
    
    
    
    
    
    
    
    
    function fetchData() {
        const gameId = document.getElementById('gameid').value;
        if (gameId) {
            $.ajax({
                url: `/betdata/${gameId}/`, 
                type: 'GET',
                success: function(data) {
                    if(data.betstat == 'OPEN'){
                        $('.betsub').removeClass('disabled')
                        $('.betlong').removeClass('disabled')
                        notif='<span class="badge bg-success fw-bolder fs-4 " >OPEN</span>'
                    }else if(data.betstat == 'LAST CALL'){
                        $('.betsub').removeClass('disabled')
                        $('.betlong').removeClass('disabled')
                        notif='<span class="badge bg-warning text-danger fw-bolder fs-4  blink callnotif" >LAST CALL</span>'
                    }else if(data.betstat == 'CLOSED'){
                        $('.betsub').addClass('disabled')
                        $('.betlong').addClass('disabled')
                        notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
                    }else if(data.betstat == 'CLOSING'){
                        $('.betsub').addClass('disabled')
                        $('.betlong').addClass('disabled')
                        notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
                    }else if(data.betstat == 'DECLARED'){
                        $('.betsub').addClass('disabled')
                        $('.betlong').addClass('disabled')
                        notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
                    }else if(data.betstat == 'DONE'){
                        notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
                        $('.betsub').addClass('disabled')
                        $('.betlong').addClass('disabled')
                        $('.meron_box').removeClass('meron-win')
                        $('.wala_box').removeClass('wala-win')
                        $('.draw_box').removeClass('draw-win')
                    }
                    
                    if(data.fwin == 'MERON'){
                        $('.meron_box').addClass('meron-win')
                        $('.wala_box').removeClass('wala-win')
                        $('.draw_box').removeClass('draw-win')
                        $('#meron-win').attr('hidden',false)
                        $('#wala-win').attr('hidden',true)
                        $('#draw-win').attr('hidden',true)
                        $('#cancel-win').attr('hidden',true)
                    }else if(data.fwin == 'WALA'){
                        $('.meron_box').removeClass('meron-win')
                        $('.draw_box').removeClass('draw-win')
                        $('.wala_box').addClass('wala-win')
                        $('#meron-win').attr('hidden',true)
                        $('#wala-win').attr('hidden',false)
                        $('#draw-win').attr('hidden',true)
                        $('#cancel-win').attr('hidden',true)
                    }else if(data.fwin == 'DRAW'){
                        $('.draw_box').addClass('draw-win')
                        $('.meron_box').removeClass('meron-win')
                        $('.wala_box').removeClass('wala-win')
                        $('#meron-win').attr('hidden',true)
                        $('#wala-win').attr('hidden',true)
                        $('#draw-win').attr('hidden',false)
                        $('#cancel-win').attr('hidden',true)
                    }else if(data.fwin == 'CANCELLED'){
                        $('.draw_box').addClass('draw-win')
                        $('.meron_box').removeClass('meron-win')
                        $('.wala_box').removeClass('wala-win')
                        $('#meron-win').attr('hidden',true)
                        $('#wala-win').attr('hidden',true)
                        $('#draw-win').attr('hidden',true)
                        $('#cancel-win').attr('hidden',false)
                    }else{
                        $('.meron_box').removeClass('meron-win')
                        $('.wala_box').removeClass('wala-win')
                        $('.draw_box').removeClass('draw-win')
                        $('#draw-win').attr('hidden',true)
                        $('#meron-win').attr('hidden',true)
                        $('#wala-win').attr('hidden',true)
                        $('#cancel-win').attr('hidden',true)
                    }
                    
                    $('.gamename').html(data.game_name);
                    $('#fid').val(data.fight_id);
                    $('#betst').val(data.betstat);
                    $('#gameid').val(data.game);
                    $('.notif').html(notif)
                    $('.fnum').text('Fight #: '+data.fnumber)
                    $('.nmeron').html(data.nmeron);
                    meron = $('.meron-val').val()
                    $('.meron_bet').text(data.dmeron)
                    $('.meron-val').val(data.dmeron)
                    $('.mymeronbet').text(data.mybetmeron.toLocaleString('en'))
                    $('.meronpayout').text(data.meronpayout.toFixed(2))
                    $('.merontowin').text(data.merontowin.toFixed(2))
                    $('.meron_bet').each(function () {
                        $(this).prop('Counter',meron).animate({
                            Counter: $(this).text()
                        }, {
                            duration: 1000,
                            easing: 'swing',
                            step: function (now) {
                                $(this).text(Math.ceil(now).toLocaleString('en'));
                            }
                        })
                    });
                    
                    $('.nwala').html(data.nwala);
                    wala = $('.wala-val').val()
                    $('.wala_bet').text(data.dwala)
                    $('.wala-val').val(data.dwala)
                    $('.walapayout').text(data.walapayout.toFixed(2))
                    $('.mywalabet').text(data.myWalaBet.toLocaleString('en'))
                    $('.walatowin').text(data.walatowin.toFixed(2))
                    $('.wala_bet').each(function () {
                        $(this).prop('Counter',wala).animate({
                            Counter: $(this).text()
                        }, {
                            duration: 1000,
                            easing: 'swing',
                            step: function (now) {
                                $(this).text(Math.ceil(now).toLocaleString('en'));
                            }
                        })
                    });
                    
                    draw = $('.draw-val').val()
                    $('.mydrawbet').text(data.mydrawbet)
                    $('.draw-val').val(data.mydrawbet)
                    $('.mydrawbet').each(function () {
                        $(this).prop('Counter',draw).animate({
                            Counter: $(this).text()
                        }, {
                            duration: 2000,
                            easing: 'swing',
                            step: function (now) {
                                $(this).text(Math.ceil(now).toLocaleString('en'));
                            }
                        })
                    });
                    
                    long = $('.long-val').val()
                    $('.mylongbet').text(data.mylongbet)
                    $('.long-val').val(data.mylongbet)
                    $('.mylongbet').each(function () {
                        $(this).prop('Counter',long).animate({
                            Counter: $(this).text()
                        }, {
                            duration: 2000,
                            easing: 'swing',
                            step: function (now) {
                                $(this).text(Math.ceil(now).toLocaleString('en'));
                            }
                        })
                    });
                    
                    $('#wbalance').val(data.mywallet)
                    $('.wbalance').text(data.mywallet.toLocaleString('en'))
                    
                    if(data.reglastat==1){
                        renderTablehistory();
                        renderTablereg();
                    }
                    
                    
                },
                error: function(error) {
                    console.log('Error fetching data:', error);
                }
            });
        } else {
            console.error('Game ID not found!');
        }
    }
    $(document).ready(fetchData);
    
    function refreshFunction() {
        fetchData()
    }
    setInterval(refreshFunction, 2000);
    
    
    
    
})