$(document).ready(function(){
    
    
    $(document).on('click','.g_duplicate',function(){
        gname=$(this).attr('game_n')
        gid=$(this).attr('id')
        Swal.fire({
            title: 'Duplicate '+gname+'?',
            text: 'COPY FIGTH EVENT?',
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Copy!"
        }).then((result) => {
            if (result.isConfirmed) {
              
                $.ajax({
                    method:'POST',
                    url:'duplicate_game',
                    data:{gname:gname,gid:gid},
                    success:function(res){

                        $('#id_g_name').val(res.data.gname)
                        $('#id_g_redname').val(res.data.meron)
                        $('#id_g_bluename').val(res.data.wala)
                        $('#id_g_desc').val(res.data.desc)
                        $('#id_g_plasada').val(res.data.plasada)
                        $('#id_g_category').val(res.data.cat)
                        $('#id_g_link').val(res.data.link)
                        $('.tg_image').val(res.data.img)
                        
                        $('#id_g_image').attr('required',false)


                        $('#addgames').modal('show')
                        console.log(res.data.gname)
                    }
                })
                
            }
        });

    })
    
    $(document).on('click','.reset_games',function(){
        gname=$(this).attr('game_n')
        gid=$(this).attr('id')
        Swal.fire({
            title: 'RESET '+gname+'?',
            text: 'RESET FIGTH EVENT?',
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "RESET!"
        }).then((result) => {
            if (result.isConfirmed) {
                
                $.ajax({
                    method:'POST',
                    url:'resetFightNo',
                    data:{gname:gname,gid:gid},
                    success:function(res){
                        
                        console.log(res)
                    }
                })
                
            }
        });
    })
    
    $(document).on('click','.nxtfight',function(){
        const page = document.getElementById('page').value;
        fight=$(this).attr('game')
        game=$(this).attr('id')
        multi=$('.bmulti').val()
        Swal.fire({
            title: 'Next Fight?',
            text: "Please confirm your Action!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Proceed!"
        }).then((result) => {
            if (result.isConfirmed) {                
                $.ajax({
                    method:'POST',
                    url:'../../nxtfight',
                    data:{fight:fight,game:game,multi,multi},
                    success:function(res){
                        get_fight(game)
                        if(page == "DECLA ARENA"){
                            fetchDeclaData()
                            renderTablehistory();
                            renderTablereg();
                        }
                    }
                })
            }
        });
    })
    
    
    
    
    
    
    $(document).on('click','.disburse_btn',function(){
        const page = document.getElementById('page').value;
        fight=$(this).attr('game')
        Swal.fire({
            title: 'Disburse Payment?',
            text: "Please confirm your Action!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Disburse!"
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    method:'POST',
                    url:'../../disburse',
                    data:{fight:fight},
                    success:function(res){
                        if(page == "DECLA ARENA"){
                            fetchDeclaData()
                            // renderTablehistory();
                            // renderTablereg();
                        }
                        // socket.send(JSON.stringify({
                        //     'bet_stat': 'DONE',
                        //     'amount': 0,
                        //     'betin':'',
                        //     'fight_no':'',
                        
                        // }))                        
                    }
                })
            }
        });
    })
    
    
    
    
    
    
    
    $(document).on('click','.revert_btn',function(){
        const page = document.getElementById('page').value;
        fight=$(this).attr('game')
        Swal.fire({
            title: 'Revert Declaration?',
            text: "Please confirm your Action!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Revert!"
        }).then((result) => {
            if (result.isConfirmed) {                
                $.ajax({
                    method:'POST',
                    url:'../../revert',
                    data:{fight:fight},
                    success:function(res){
                        if(page == "DECLA ARENA"){
                            fetchDeclaData()
                            renderTablehistory();
                            renderTablereg();
                        }
                        // socket.send(JSON.stringify({
                        //     'bet_stat': 'CLOSE',
                        //     'amount': 0,
                        //     'betin':'',
                        //     'fight_no':'',
                        // }))
                    }
                })
            }
        });
    })
    
    
    
    
    
    
    $(document).on('click','.betwin',function(res){
        const page = document.getElementById('page').value;
        winner=$(this).attr('id')
        fight=$(this).attr('game')
        gameid=$(this).attr('gameid')
        if(winner != 'DRAW'){
            msg=winner+' WINS?'
        }else{
            msg='DRAW FIGHT?'
        }
        Swal.fire({
            title: msg,
            text: "Please confirm your Actiona!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: winner+" WINS!"
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    method:'POST',
                    url:'../../setwinner',
                    data:{fight:fight,winner:winner,gameid:gameid},
                    success:function(res){
                        if(page == "DECLA ARENA"){
                            fetchDeclaData()
                            renderTablehistory();
                            renderTablereg();
                        }
                        // socket.send(JSON.stringify({
                        //     'bet_stat': 'DECLARED',
                        //     'amount': 0,
                        //     'betin':'',
                        //     'fight_no':'',
                        // }))
                    }
                })
            }
        });
    })
    
    
    
    
    
    
    
    
    $(document).on('click','.longbetwin',function(res){
        const page = document.getElementById('page').value;
        winner=$(this).attr('id')
        fight=$(this).attr('game')
        gameid=$(this).attr('gameid')
        
        msg='LONGEST FIGHT?'
        Swal.fire({
            title: msg,
            text: "Please confirm your action!",
            icon: "warning",
            input: 'number',
            inputPlaceholder: 'Enter fight number',
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "LONGEST FIGHT!",
            preConfirm: (fvalue) => {
                if (!fvalue) {
                    Swal.showValidationMessage('You need to enter fight number!'); 
                }
                return fvalue;
            }
            
        }).then((result) => {
            if (result.isConfirmed) {
                const fvalue = result.value;
                $.ajax({
                    method:'POST',
                    url:'../../setlongwin',
                    data:{fight:fight,winner:winner,gameid:gameid,fightnum:fvalue},
                    success:function(res){
                        if(res.data == 'ok'){
                            Swal.fire({
                                title: "Successfully disburse!",
                                icon: "success"
                            });
                        }else{
                            Swal.fire({
                                title: "No bets found in longest fight!",
                                icon: "error"
                            });
                        }
                        if(page == "DECLA ARENA"){
                            fetchDeclaData()
                            // renderTablehistory();
                            // renderTablereg();
                        }
                        // socket.send(JSON.stringify({
                        //     'bet_stat': 'DECLARED',
                        //     'amount': 0,
                        //     'betin':'',
                        //     'fight_no':'',
                        // }))
                    }
                })
            }
        });
    })
    
    
    
    
    
    
    
    $(document).on('click','.addfight',function(){
        gfid=$(this).attr('id')
        get_fight(gfid)
        $('#fightsetting').modal('toggle')
    })
    
    
    
    // Fight SUBMIT
    $(document).on('submit','#fsetting',function(e){
        const page = document.getElementById('page').value;
        e.preventDefault()
        data=$(this).serializeArray()
        gfid=$('#gid').val()
        fnum=$('.fight_no').val()
        fmulti=$('.fmulti').val()
        if( $('.sub_type').is(':checked') ){
            typ='UPDATE ONGOING FIGHT?'
        }
        else{
            typ='CREATE NEW FIGHT?'
        }
        
        Swal.fire({
            title: typ,
            text: "Please confirm your Action!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Proceed!"
        }).then((result) => {
            if (result.isConfirmed) {
                $(".upfight").show();
                if(fnum == 0 || fmulti == 0){
                    Swal.fire({
                        title: "Please Input a Valid Entry!",
                        icon: "error"
                    });
                }else{
                    
                    $.ajax({
                        method:'POST',
                        url:'../../addfight',
                        data:data,
                        success:function(res){
                            $(".upfight").hide();
                            get_fight(gfid)
                            if(page == "DECLA ARENA"){
                                fetchDeclaData()
                                renderTablehistory();
                                renderTablereg();
                            }
                            if(res.data == 'update'){
                                Swal.fire({
                                    title: "Update Successfully!",
                                    icon: "success"
                                });
                                $('#fightsetting').modal('hide')
                            }else if(res.data == 'insert' ){
                                Swal.fire({
                                    title: "Create New Fight Success!",
                                    icon: "success"
                                });
                                $('#fightsetting').modal('hide')
                            }else if(res.data == 'exist' ){
                                Swal.fire({
                                    title: "Fight Number Exist!",
                                    icon: "error"
                                });
                                
                            }else{
                                Swal.fire({
                                    title: "Error Command!",
                                    icon: "error"
                                });
                            }
                        }
                    })
                    
                }
            }
        });  
    })
    
    // Fight sub
    $('.sub_type').on('change',function(){
        if( $(this).is(':checked') ){
            $('.fsubmit').text('Update Current Fight?')
            $('.ftype').text('Update Existing Fight?')
        }
        else{
            $('.fsubmit').text('Create New Fight?')
            $('.ftype').text('Create New Fight?')
        } 
    })
    
    
    
    
    //  load_games()
    function load_games(){
        $.ajax({
            url:'load_games',
            type:'POST',
            success:function(res){
                st=''
                $('#games_tbl').html('')
                for(g in res){  
                    if(res[g].fields.g_status == 'CLOSED'){
                        st='<span class="badge text-bg-danger">CLOSED</span>'
                    }else if(res[g].fields.g_status == 'OPEN'){
                        st='<span class="badge text-bg-success">OPEN</span>'
                    }
                    
                    data='<tr>\
                <td>'+moment(res[g].fields.g_created).format('YYYY-MM-DD hh:m a')+'</td>\
                 <td class="text-white fw-bolder fs-4">'+res[g].fields.g_name+'</td>\
                 <td>'+res[g].fields.g_category+'</td>\
                 <td class="text-white fw-bolder fs-4">'+res[g].fields.g_plasada+'</td>\
                 <td>'+st+'</td>\
                 <td class="text-center"><button type="button" class="btn btn-outline-warning mb-2 me-2 g_update" id="'+res[g].pk+'"><i class="fa fa-edit"></i> Update</button>\
                 <a type="button" class="btn btn-outline-primary mb-2 me-2 g_preview" href="decla/arena/'+res[g].pk+'" %}" id="'+res[g].pk+'"><i class="fa fa-eye"></i> Preview</a>\
                 <button type="button" class="btn btn-outline-danger mb-2 me-2 del_games" id="'+res[g].pk+'" ><i class="icon_close_alt2"></i> Remove</button>\
                </tr>'
                    
                    $('#games_tbl').append(data)
                }
            }
        })
        
        
    }
    
    
    
    
    
    $(document).on('click','.del_games',function(){
        const page = document.getElementById('page').value;
        did=$(this).attr('id')
        
        Swal.fire({
            title: "REMOVE GAMES ?",
            text: "You're to close Delete Games!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Proceed!"
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    method:'POST',
                    url:'delgame',
                    data:{did:did},
                    success:function(res){
                        if(res.data == 'ok'){
                            $("#import_row_table").load('imprt_newgame');
                            if(page == "DECLA ARENA"){
                                fetchDeclaData()
                                renderTablehistory();
                                renderTablereg();
                            }
                        }
                    }
                })
            }
        });
        
    })
    
    
    
    
    // //////////////////// add games
    $('#addgame').on('submit',function(e){
        e.preventDefault()
        $('.msg').html('')
        $(".addgames").show();
        var newgamebtn = document.getElementById('newgamebtn');
        newgamebtn.disabled = true;
        $.ajax({
            url: "add_games",
            type: "POST",
            data: new FormData(this),
            cenctype: 'multipart/form-data',
            processData: false,
            contentType: false,   
            success: function(res){
                $(".addgames").hide();
                newgamebtn.disabled = false;
                if(res.data == 'ok'){
                    toastr["success"]("New Game Successfully Added!");
                        $("#import_row_table").load('imprt_newgame');
                        $('#addgame').trigger('reset')
                    }else if(res.data == 'copy'){
                        toastr["success"]("Duplicate Successfully!");
                        $("#import_row_table").load('imprt_newgame');
                        $('#addgame').trigger('reset')
                    }
                    else{
                        toastr["error"]("Please try again after a few seconds.");
                        console.log(res) 
                    }
                },
                error: function(){
                    alert(res.data)
                }
            });
        })
        
        
        
        // ///////////////// update game
        function get_fight(gfid){
            cgame=$('.gname').text()
            $.ajax({
                method:'POST',
                url:'../../gfight',
                data:{gfid:gfid},
                success:function(res){
                    $('.fight_no').val(res.data.fnum)
                    $('.fmulti').val(res.data.fmulti)
                    $('.bmulti').val(res.data.fmulti)
                    $('.f_game').val(res.data.game)
                    $('.fid').val(res.data.fight)
                    $('.fstat').val(res.data.fstat)
                    $('.f_winner').val(res.data.fwin)
                    $('.f_longest').val(res.data.flong)
                    $('.fnum_dis').text(res.data.fnum)
                    $('.fgame').val(cgame)
                    $('.notif').html('')
                    $('.controls').html('')
                    fetchDeclaData()
                    // socket.send(JSON.stringify({
                    //     'bet_stat': 'OPEN',
                    //     'amount': 0,
                    //     'betin':'',
                    //     'fight_no':res.data.fnum,
                    // }))
                }
            })
        }
        
        
        
        
        $('#updategame').on('submit',function(e){
            $(".upgames").show();
            e.preventDefault()
            $('.msg').html('')
            $.ajax({
                url: "update_games",
                type: "POST",
                data: new FormData(this),
                cenctype: 'multipart/form-data',
                processData: false,
                contentType: false,   
                success: function(res){
                    $(".upgames").hide();
                    Swal.fire({
                        title: "Update Successfull",
                        icon: "success"
                    });
                    $('#updategames').modal('hide')
                    $("#import_row_table").load('imprt_newgame');
                },
                error: function(){
                    alert(res.data)
                }
            });
        })
        
        
        
        
        
        // /////////////// UPDATE
        $(document).on('click','.g_update',function(){
            gid=$(this).attr('id')
            
            $.ajax({
                method:'POST',
                url:'getgame',
                data:{gid:gid},
                success:function(res){
                    for(r in res){
                        $('.g_id').val(gid)
                        $('.g_name').val(res[r].gname)
                        $('.g_redname').val(res[r].meron)
                        $('.g_bluename').val(res[r].wala)
                        $('.g_plasada').val(res[r].plasada)
                        $('.g_desc').val(res[r].desc)
                        $('.g_category').val(res[r].category)
                        $('.g_link').val(res[r].link)
                        $('.gimage').val(res[r].image)
                        $('.g_status').val(res[r].status)
                        // ('.g_image').val(res[r].image)
                        $('.img_preview').attr('src','uploads/'+res[r].image)
                    }   
                    $('#updategames').modal('show')
                }
            })
        })
        
        
        
        
        // /////////// control btn
        $(document).on('click','.callbtn',function(){
            gfid=$('#gid').val()
            typ=$(this).attr('typ')
            fid=$(this).attr('game')
            bmulti=$('.bmulti').val()
            $('.callbtn').prop('disabled', true);
            if(bmulti == 0){
                Swal.fire({
                    title: "Bet Multiplier Required!",
                    icon: "error"
                });
            }else{
                Swal.fire({
                    title: ""+typ+" BET ?",
                    text: "You're about to update Fight!",
                    icon: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#3085d6",
                    cancelButtonColor: "#d33",
                    confirmButtonText: "Proceed!"
                }).then((result) => {
                    if (result.isConfirmed) {
                        $.ajax({
                            method:'POST',
                            url:'../../fight_stat',
                            data:{fid:fid,typ:typ,game:gfid},
                            success:function(res){
                                $('.callbtn').prop('disabled', false);
                                if(res.data == 1){
                                    get_fight(gfid)
                                    fetchDeclaData()
                                }
                            }
                        })
                    }
                });
            }
        })
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        //////////// WEBSOCKET
        // const ongame=JSON.parse(document.getElementById('arena_game').textContent)
        // var socket= new WebSocket('ws://'+window.location.host+'/ws/arena/'+ongame);
        // socket.onmessage =function(e){    
        //     result=JSON.parse(e.data)
        // $('.notif').html('')
        // $('.controls').html('')
        
        // if(result.winner == 'MERON'){
        //     $('.meron_box').addClass('meron-win')
        //     $('.wala_box').removeClass('wala-win')
        //     $('.draw_box').removeClass('draw-win')
        //     $('#meron-win').attr('hidden',false)
        //     $('#wala-win').attr('hidden',true)
        //     $('#draw-win').attr('hidden',true)
        // }else if(result.winner == 'WALA'){
        //     $('.meron_box').removeClass('meron-win')
        //     $('.draw_box').removeClass('draw-win')
        //     $('.wala_box').addClass('wala-win')
        //     $('#meron-win').attr('hidden',true)
        //     $('#wala-win').attr('hidden',false)
        //     $('#draw-win').attr('hidden',true)
        // }else if(result.winner == 'DRAW'){
        //     $('.draw_box').addClass('draw-win')
        //     $('.meron_box').removeClass('meron-win')
        //     $('.wala_box').removeClass('wala-win')
        //     $('#meron-win').attr('hidden',true)
        //     $('#wala-win').attr('hidden',true)
        //     $('#draw-win').attr('hidden',false)
        // }else if(result.winner == ''){
        //     $('.meron_box').removeClass('meron-win')
        //     $('.wala_box').removeClass('wala-win')
        //     $('.draw_box').removeClass('draw-win')
        //     $('#meron-win').attr('hidden',true)
        //     $('#wala-win').attr('hidden',true)
        //     $('#draw-win').attr('hidden',true)
        // }
        
        
        // notif=''
        // if(result.bet_status == 'OPEN'){
        //     ctr='<button class="btn btn-warning callbtn col-12 fs-2 mb-2 " typ="LAST CALL" game="'+result.fightid+'">LAST CALL BET</button>'
        //     notif='<span class="badge bg-success fw-bolder fs-4 closenotif" >OPEN</span>'
        // }else if(result.bet_status == 'LAST CALL'){
        //     ctr='<button class="btn btn-danger callbtn col-12 fs-2 mb-2 " typ="CLOSING" game="'+result.fightid+'">CLOSE BET</button>'
        //     notif='<span class="badge bg-warning text-danger fw-bolder fs-4  blink callnotif" >LAST CALL</span>'
        
        // }else if(result.bet_status == 'CLOSING'){
        //     ctr='<div class="row"> <div class="col-6 mt-2">\
        //  <button class="btn btn-danger fs-2 w-100 betwin" game="'+result.fightid+'"  id="MERON" gameid="'+result.game_id+'">MERON WIN?</button></div>\
        //  <div class="col-6 mt-2">\
        //    <button class="btn btn-primary fs-2 w-100 betwin" game="'+result.fightid+'" id="WALA" gameid="'+result.game_id+'">WALA WIN?</button>\
        //    </div><div class="col-6 mt-2">\
        //     <button class="btn btn-success fs-2 w-100 betwin" game="'+result.fightid+'" id="DRAW" gameid="'+result.game_id+'">DRAW WIN?</button>\
        //   </div><div class="col-6 mt-2">\
        //    <button class="btn btn-secondary fs-2 w-100 betwin"  game="'+result.fightid+'" id="CANCELLED" gameid="'+result.game_id+'">CANCEL FIGHT?</button>\
        //         </div></div>\
        //     <br>\
        //    <button class="btn btn-warning fs-2 w-100 longbetwin"  game="'+result.fightid+'" id="LONGEST" gameid="'+result.game_id+'">LONGEST FIGHT?</button>'
        //     notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
        
        // }else if(result.bet_status == 'DECLARED'){
        //     notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
        //     ctr='<div class="row"><div class="col-12 mt-2">\
        //   <button class="btn btn-secondary fs-2 w-100 revert_btn"  game="'+result.fightid+'" >REVERT?</button>\
        //    </div> <div class="col-12 mt-2">\
        //     <button class="btn btn-danger fs-2 w-100 disburse_btn"  game="'+result.fightid+'"  >DISBURSE </button>\
        //    </div></div>\
        //    <br>\
        //    <button class="btn btn-warning fs-2 w-100 longbetwin"  game="'+result.fightid+'" id="LONGEST" gameid="'+result.game_id+'">LONGEST FIGHT?</button>'
        
        // }else if(result.bet_status == 'CLOSED'){
        //     notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
        //     ctr='<button class="btn btn-success callbtn col-12 fs-2 mb-2 " typ="OPEN" game="'+result.fightid+'">OPEN BET</button>'
        // }else if(result.bet_status == 'DONE'){
        //     notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
        //     ctr='<button class="btn btn-success nxtfight col-12 fs-2 mb-2  " id="'+result.game_id+'" typ="NEW"  game="'+result.fightid+'" > NEW FIGHT?</button>'
        //     $('.meron_box').removeClass('meron-win')
        //     $('.wala_box').removeClass('wala-win')
        //     $('.draw_box').removeClass('draw-win')
        //     $('#meron-win').attr('hidden',true)
        //     $('#wala-win').attr('hidden',true)
        //     $('#draw-win').attr('hidden',true)
        // }
        // else if(result.bet_status == ''){
        //     notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
        //     ctr='<button class="btn btn-secondary addfight col-12 fs-2 mb-2  " id="'+result.game_id+'" typ="NEW"  game="'+result.fightid+'" >CREATE NEW FIGHT?</button>'
        // }
        
        // $('.notif').append(notif)
        // $('.controls').append(ctr)
        
        // dmeron = $('.dmeron-val').val()
        // $('.dmeron_bet').text(result.dmeron)
        // $('.dmeron-val').val(result.dmeron)
        // $('.dmeron_bet').each(function () {
        //     $(this).prop('Counter',dmeron).animate({
        //         Counter: $(this).text()
        //     }, {
        //         duration: 1000,
        //         easing: 'swing',
        //         step: function (now) {
        //             $(this).text(Math.ceil(now).toLocaleString('en'));
        //         }
        //     })
        // });
        
        // dwala = $('.dwala-val').val()
        // $('.dwala_bet').text(result.dwala)
        // $('.dwala-val').val(result.dwala)
        // $('.dwala_bet').each(function () {
        //     $(this).prop('Counter',dwala).animate({
        //         Counter: $(this).text()
        //     }, {
        //         duration: 1000,
        //         easing: 'swing',
        //         step: function (now) {
        //             $(this).text(Math.ceil(now).toLocaleString('en'));
        //         }
        //     })
        // });
        
        // meron = $('.meron-val').val()
        // $('.meron_bet').text(result.meron)
        // $('.meron-val').val(result.meron)
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
        // $('.wala_bet').text(result.wala)
        // $('.wala-val').val(result.wala)
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
        // $('.draw_bet').text(result.draw)
        // $('.draw-val').val(result.draw)
        // $('.draw_bet').each(function () {
        //     $(this).prop('Counter',draw).animate({
        //         Counter: $(this).text()
        //     }, {
        //         duration: 1000,
        //         easing: 'swing',
        //         step: function (now) {
        //             $(this).text(Math.ceil(now).toLocaleString('en'));
        //         }
        //     })
        // });
        
        // long = $('.long-val').val()
        // $('.long_bet').text(result.longest)
        // $('.long-val').val(result.longest)
        // $('.long_bet').each(function () {
        //     $(this).prop('Counter',long).animate({
        //         Counter: $(this).text()
        //     }, {
        //         duration: 1000,
        //         easing: 'swing',
        //         step: function (now) {
        //             $(this).text(Math.ceil(now).toLocaleString('en'));
        //         }
        //     })
        // });
        
        // $('.meronpayout').text(result.meronpayout.toFixed(2))
        // $('.walapayout').text(result.walapayout.toFixed(2))
        // }
    })
    
    
    
    
    
    // fight history
    function tablehistory(rows, columns, fightData) {
        const table = document.createElement('table');
        let fightIndex = 0;
        let lastFilledCell = null;
        
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
                    } else {
                        span.classList.add('badge_default');
                    }
                    td.appendChild(span);
                    fightIndex++;
                    
                    lastFilledCell = td;
                } else {
                    td.textContent = '';
                }
            }
        }
        
        return { table, lastFilledCell };
    }
    
    async function fetchFightline() {
        try {
            const gameId = document.getElementById('gid').value;
            const response = await fetch(`/get-fight-data/${gameId}/`);
            
            if (!response.ok) {
                throw new Error('Network response was not ok' + response.statusText);
            }
            const fightData = await response.json();
            return fightData;
        } catch (error) {
            return [];
        }
    }
    
    async function renderTablehistory() {
        const page = document.getElementById('page').value;
        if (page == "DECLA ARENA") {
            const fightData = await fetchFightline();
            if (fightData.length > 0) {
                const container = document.getElementById('tablehistory');
                container.innerHTML = '';
                const { table, lastFilledCell } = tablehistory(5, 300, fightData);
                container.appendChild(table);
                if (lastFilledCell) {
                    scrollToLastContent(lastFilledCell);
                }
            } else {
                console.log('No fight data available');
            }
        }
    }
    
    function scrollToLastContent(element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'end' });
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
            const gameId = document.getElementById('gid').value;
            const response = await fetch(`/get-fight-data/${gameId}/`);
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            const fightData = await response.json();
            return fightData;
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
            // alert('Failed to load fight data. Please try again later.');
            return [];
        }
    }
    
    async function renderTablereg() {
        const page = document.getElementById('page').value;
        if(page == "DECLA ARENA"){
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
    }
    renderTablereg(); ///org
    // reglahan
    
    
    
    
    
    
    $(document).on('click','.revertwin',function(res){
        var page = document.getElementById('page').value;
        var action=$(this).attr('action')
        var fight=$(this).attr('fightid')
        var gameid=$(this).attr('gameid')
        
        msg='REVERT PREVIOUS WINNER?'
        Swal.fire({
            title: msg,
            text: "Please confirm fight number!",
            icon: "question",
            html: `
            <div class="mb-3">
            <label class="pull-left">Fight number</label>
                <input id="fightNumberInput" class="form-control" type="number" placeholder="0" />
                <label class="pull-left">Fight Win</label>
                <select id="fightSelect" class="form-control">
                    <option value=""> - </option>
                    <option value="MERON">MERON</option>
                    <option value="WALA">WALA</option>
                    <option value="DRAW">DRAW</option>
                    <option value="CANCELLED">CANCELLED</option>
                </select>
                </div>
            `,
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "REVERT FIGHT!",
            preConfirm: () => {
                const fvalue = document.getElementById('fightNumberInput').value;
                const selectedFight = document.getElementById('fightSelect').value;
                if (!fvalue && !selectedFight && !action && fight && !gameid) {
                    Swal.showValidationMessage('You need to enter or select a fight number and winner!');
                }
                return { fvalue, selectedFight };;
            }
        }).then((result) => {
            if (result.isConfirmed) {
                var fightNum = result.value.fvalue;
                var fwinner = result.value.selectedFight;
                
                $.ajax({
                    method:'POST',
                    url:'../../revertwinner',
                    data:{action:action,fight:fight,gameid:gameid,fightNum:fightNum,fwinner:fwinner},
                    success:function(res){
                        if(res.data == 'success'){
                            Swal.fire({
                                title: "Revert successfully done!",
                                icon: "success"
                            });
                        }else if(res.data == 'notfound'){
                            Swal.fire({
                                title: "Revert successfully done! But no bets found in this fight!",
                                icon: "success"
                            });
                        }else if(res.data == 'invalid'){
                            Swal.fire({
                                title: "No changes was made. Same winner from previous fight could not be reverted.",
                                icon: "error"
                            });
                        }else if(res.data == 'dataerror'){
                            Swal.fire({
                                title: "Some error on updating data.",
                                icon: "error"
                            });
                        }else{
                            Swal.fire({
                                title: "Something went wrong.",
                                icon: "error"
                            });
                        }
                        if(page == "DECLA ARENA"){
                            fetchDeclaData()
                            renderTablehistory();
                            renderTablereg();
                        }
                        // socket.send(JSON.stringify({
                        //     'bet_stat': 'DECLARED',
                        //     'amount': 0,
                        //     'betin':'',
                        //     'fight_no':'',
                        // }))
                    }
                })
            }
        });
    })
    
    
    
    
    
    function fetchDeclaData() {
        const page = document.getElementById('page').value;
        if(page == "DECLA ARENA"){
            const gameId = document.getElementById('gid').value;
            if (gameId) {
                $.ajax({
                    url: `/decladata/${gameId}/`, 
                    type: 'GET',
                    success: function(data) {
                        $('.notif').html('')
                        $('.controls').html('')
                        $('.revertdiv').html('')
                        
                        if(data.winner == 'MERON'){
                            $('.meron_box').addClass('meron-win')
                            $('.wala_box').removeClass('wala-win')
                            $('.draw_box').removeClass('draw-win')
                            $('#meron-win').attr('hidden',false)
                            $('#wala-win').attr('hidden',true)
                            $('#draw-win').attr('hidden',true)
                            $('#cancel-win').attr('hidden',true)
                        }else if(data.winner == 'WALA'){
                            $('.meron_box').removeClass('meron-win')
                            $('.draw_box').removeClass('draw-win')
                            $('.wala_box').addClass('wala-win')
                            $('#meron-win').attr('hidden',true)
                            $('#wala-win').attr('hidden',false)
                            $('#draw-win').attr('hidden',true)
                            $('#cancel-win').attr('hidden',true)
                            
                        }else if(data.winner == 'CANCELLED'){
                            $('.meron_box').removeClass('meron-win')
                            $('.draw_box').removeClass('draw-win')
                            $('.wala_box').removeClass('wala-win')
                            $('#meron-win').attr('hidden',true)
                            $('#wala-win').attr('hidden',true)
                            $('#draw-win').attr('hidden',true)
                            $('#cancel-win').attr('hidden',false)

                        }else if(data.winner == 'DRAW'){
                            $('.draw_box').addClass('draw-win')
                            $('.meron_box').removeClass('meron-win')
                            $('.wala_box').removeClass('wala-win')
                            $('#meron-win').attr('hidden',true)
                            $('#wala-win').attr('hidden',true)
                            $('#draw-win').attr('hidden',false)
                            $('#cancel-win').attr('hidden',true)
                        }else if(data.winner == ''){
                            $('.meron_box').removeClass('meron-win')
                            $('.wala_box').removeClass('wala-win')
                            $('.draw_box').removeClass('draw-win')
                            $('#meron-win').attr('hidden',true)
                            $('#wala-win').attr('hidden',true)
                            $('#draw-win').attr('hidden',true)
                            $('#cancel-win').attr('hidden',true)
                        }
                        
                        
                        notif=''
                        if(data.bet_status == 'OPEN'){
                            ctr='<button class="btn btn-warning callbtn col-12 fs-2 mb-2 " typ="LAST CALL" game="'+data.fightid+'">LAST CALL BET</button>'
                            notif='<span class="badge bg-success fw-bolder fs-4 closenotif" >OPEN</span>'
                        }else if(data.bet_status == 'LAST CALL'){
                            ctr='<button class="btn btn-danger callbtn col-12 fs-2 mb-2 " typ="CLOSING" game="'+data.fightid+'">CLOSE BET</button>'
                            notif='<span class="badge bg-warning text-danger fw-bolder fs-4  blink callnotif" >LAST CALL</span>'
                            
                        }else if(data.bet_status == 'CLOSING'){
                            ctr='<div class="row"> <div class="col-6 mt-2">\
                    <button class="btn btn-danger fs-2 w-100 betwin" game="'+data.fightid+'"  id="MERON" gameid="'+data.game_id+'">MERON WIN?</button></div>\
                    <div class="col-6 mt-2">\
                    <button class="btn btn-primary fs-2 w-100 betwin" game="'+data.fightid+'" id="WALA" gameid="'+data.game_id+'">WALA WIN?</button>\
                    </div><div class="col-6 mt-2">\
                        <button class="btn btn-success fs-2 w-100 betwin" game="'+data.fightid+'" id="DRAW" gameid="'+data.game_id+'">DRAW WIN?</button>\
                    </div><div class="col-6 mt-2">\
                    <button class="btn btn-secondary fs-2 w-100 betwin"  game="'+data.fightid+'" id="CANCELLED" gameid="'+data.game_id+'">CANCEL FIGHT?</button>\
                            </div></div>\
                        <br>\
                        <button class="btn btn-warning fs-2 w-100 longbetwin mt-3"  game="'+data.fightid+'" id="LONGEST" gameid="'+data.game_id+'" hidden>LONGESTss FIGHT?</button>'
                            notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
                            
                        }else if(data.bet_status == 'DECLARED'){
                            notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
                            ctr='<div class="row"><div class="col-12 mt-2">\
                    <button class="btn btn-secondary fs-2 w-100 revert_btn"  game="'+data.fightid+'" >REVERT?</button>\
                    </div> <div class="col-12 mt-2">\
                        <button class="btn btn-danger fs-2 w-100 disburse_btn"  game="'+data.fightid+'"  >DISBURSE </button>\
                    </div></div>\
                    <br>\
                    <button class="btn btn-warning fs-2 w-100 longbetwin mt-3"  game="'+data.fightid+'" id="LONGEST" gameid="'+data.game_id+'" hidden>LONGEST ffffFIGHT?</button>'
                            
                        }else if(data.bet_status == 'CLOSED'){
                            notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
                            ctr='<button class="btn btn-success callbtn col-12 fs-2 mb-2 " typ="OPEN" game="'+data.fightid+'">OPEN BET</button>'
                        }else if(data.bet_status == 'DONE'){
                            notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
                            ctr='<button class="btn btn-success nxtfight col-12 fs-2 mb-2  " id="'+data.game_id+'" typ="NEW"  game="'+data.fightid+'" > NEW FIGHT?</button>'
                            $('.meron_box').removeClass('meron-win')
                            $('.wala_box').removeClass('wala-win')
                            $('.draw_box').removeClass('draw-win')
                            $('#meron-win').attr('hidden',true)
                            $('#wala-win').attr('hidden',true)
                            $('#draw-win').attr('hidden',true)
                        }
                        else if(data.bet_status == ''){
                            notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
                            ctr='<button class="btn btn-secondary addfight col-12 fs-2 mb-2  " id="'+data.game_id+'" typ="NEW"  game="'+data.fightid+'" >CREATE NEW FIGHT?</button>'
                        }
                        revertdiv = '<button class="btn btn-secondary fs-2 w-100 revertwin mt-3"  fightid="'+data.fightid+'" action="REVERTWIN" gameid="'+data.game_id+'">REVERT PREV WINS?</button>';
                        $('.revertdiv').append(revertdiv)
                        $('.notif').append(notif)
                        $('.controls').append(ctr)
                        
                        dmeron = $('.dmeron-val').val()
                        $('.dmeron_bet').text(data.dmeron)
                        $('.dmeron-val').val(data.dmeron)
                        $('.dmeron_bet').each(function () {
                            $(this).prop('Counter',dmeron).animate({
                                Counter: $(this).text()
                            }, {
                                duration: 1000,
                                easing: 'swing',
                                step: function (now) {
                                    $(this).text(Math.ceil(now).toLocaleString('en'));
                                }
                            })
                        });
                        
                        dwala = $('.dwala-val').val()
                        $('.dwala_bet').text(data.dwala)
                        $('.dwala-val').val(data.dwala)
                        $('.dwala_bet').each(function () {
                            $(this).prop('Counter',dwala).animate({
                                Counter: $(this).text()
                            }, {
                                duration: 1000,
                                easing: 'swing',
                                step: function (now) {
                                    $(this).text(Math.ceil(now).toLocaleString('en'));
                                }
                            })
                        });
                        
                        meron = $('.meron-val').val()
                        $('.meron_bet').text(data.meron)
                        $('.meron-val').val(data.meron)
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
                        
                        wala = $('.wala-val').val()
                        $('.wala_bet').text(data.wala)
                        $('.wala-val').val(data.wala)
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
                        $('.draw_bet').text(data.draw)
                        $('.draw-val').val(data.draw)
                        $('.draw_bet').each(function () {
                            $(this).prop('Counter',draw).animate({
                                Counter: $(this).text()
                            }, {
                                duration: 1000,
                                easing: 'swing',
                                step: function (now) {
                                    $(this).text(Math.ceil(now).toLocaleString('en'));
                                }
                            })
                        });
                        
                        long = $('.long-val').val()
                        $('.long_bet').text(data.longest)
                        $('.long-val').val(data.longest)
                        $('.long_bet').each(function () {
                            $(this).prop('Counter',long).animate({
                                Counter: $(this).text()
                            }, {
                                duration: 1000,
                                easing: 'swing',
                                step: function (now) {
                                    $(this).text(Math.ceil(now).toLocaleString('en'));
                                }
                            })
                        });
                        
                        $('.meronpayout').text(data.meronpayout.toFixed(2))
                        $('.walapayout').text(data.walapayout.toFixed(2))
                    },
                    error: function(error) {
                        console.error('Error fetching data:', error);
                    }
                });
            } else {
                console.error('Game ID not found!');
            }
        }
    }
    function refreshFunction() {
        fetchDeclaData()
    }
    setInterval(refreshFunction, 2000);
    
    function fghtfocus(x) {
        var rewardsamount = document.getElementById('id_f_number');
        rewardsamount.addEventListener("keydown", function(e) {
            if (invalidChars.includes(e.key)) {
                e.preventDefault();
            }
        });
        if (x.readOnly) {
            return;
        }
        var salesintc = x.value;
        if (salesintc === "0") {
            x.value = "";
        }
        if (isNaN(salesintc) || salesintc.trim() === "") {
            x.value = "";
        }
    }
    
