$(document).on('click','.stake_btn',function(){
    var stakewallet = document.getElementById('stakewallet').value
    var typ=$(this).attr('id')
    var rate=$(this).attr('rate')
    var amnt=$(this).attr('amnt')
    var type=$(this).attr('type')
    var type=$(this).attr('type')
    let amntValues = parseFloat(amnt);
    var stakewallet = parseFloat(stakewallet);
    let formatamnt = amntValues.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    
    if(stakewallet >= amntValues){
        document.getElementById('actbtn').disabled = false;
        $('#stake_modal').modal('show')
    }else{
        document.getElementById('actbtn').disabled = true;
        toastr["error"]("Insufficient stake fund!"); 
    }
    $('.stake_name').val(typ)
    $('.stake_rate').val(rate)
    $('.stake_amount').val(amnt)
    $('.s_type').val(type)
    $('.stakedue').html(90)
    $('.percent').html(rate*100)
    $('.stakeamnt').html(formatamnt)
    
    
})


$('#stake_frm').on('submit',function(e){
    e.preventDefault()
    var s_type   = document.getElementById("s_type").value;
    var s_rate   = document.getElementById("stake_rate").value;
    var s_amount = document.getElementById("s_amount").value;
    
    if(s_type!="" && s_rate!="" && s_amount!=""){
        Swal.fire({
            title: "Are you sure?",
            text: "do you want to process this staking activation?",
            icon: "question",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Activate Stake"
        }).then((result) => {
            if (result.isConfirmed) {
                $(".stakespinner").show();
                document.getElementById('actbtn').disabled = true;
                $.ajax({
                    method:'POST',
                    url:'save_stake',
                    data:{s_type:s_type,s_rate:s_rate,s_amount:s_amount},
                    success:function(res){
                        $(".stakespinner").hide();
                        document.getElementById('actbtn').disabled = false;
                        $('#stake_modal').modal('hide')
                        if(res.data == 'success'){
                            toastr["success"]("Successfully done.");
                            let valstakeamnts = parseFloat(res.stakebalance);
                            let formattedAmount = valstakeamnts.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                            document.getElementById('stakebal').innerHTML = formattedAmount;
                            document.getElementById('stakewallet').value = res.stakebalance;
                            
                            let valstakeactve = parseFloat(res.stakeActive);
                            let stakeamnt = valstakeactve.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                            document.getElementById('stakeactive').innerHTML = stakeamnt;
                            
                        }else if(res.data == 'error01'){
                            toastr["error"]("Insufficient stake fund!"); 
                        }else if(res.data == 'error02'){
                            toastr["error"]("Try again later!");
                        }else{
                            toastr["error"]("Unable to process request!");
                        }
                    }
                })
            }
        });
    }else{
        toastr["error"]("Something went wrong. Please try again.");  
    }
})



$('#stakingmodal').on('show.bs.modal', function (e) {
    var opener=e.relatedTarget;
    var stakingtype  = $(opener).attr('stakingtype');
    stakelist(stakingtype)
});

function stakelist(stakingtype){
    $.ajax({
        method: 'POST',
        url: 'activeStakingSlot',
        data: {
            stakingtype: stakingtype,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        success: function(res) {
            $("#importstaking").html(res); 
        }
    });
}



$(document).on('click','.stakeclaim',function(){
    var stakecode=$(this).attr('scode')
    var staketype=$(this).attr('staketype')
    
    Swal.fire({
        title: "Are you sure?",
        text: "do you want to claim this staking income?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Claim!"
    }).then((result) => {
        if (result.isConfirmed) {
            $("." + stakecode).show();
            document.getElementById('claimbtn').disabled = true;
            $.ajax({
                method:'POST',
                url:'claimstake',
                data:{stakecode:stakecode},
                success:function(res){
                    $("." + stakecode).hide();
                    document.getElementById('claimbtn').disabled = false;
                    
                    if(res.data == 'success'){
                        toastr["success"]("Successfully done.");
                        stakelist(staketype)
                        let valstakeamnts = parseFloat(res.earnings);
                        let formattedAmount = valstakeamnts.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                        document.getElementById('stkeearnings').innerHTML = formattedAmount;
                        
                        let valsbal = parseFloat(res.avilearnings);
                        let valsbalfrmat = valsbal.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                        document.getElementById('availablestake').innerHTML = valsbalfrmat;
                        
                    }else if(res.data == 'insufficient'){
                        toastr["error"]("Insufficient stake fund earnings!"); 
                    }else if(res.data == 'tryagain'){
                        toastr["error"]("Try again later!");
                    }else{
                        toastr["error"]("Unable to process request!");
                    }
                }
            })
        }
    });
});








$('#stakeCashout').on('show.bs.modal', function (e) {
    var opener=e.relatedTarget;
    var balance  = $(opener).attr('balance');
    var costat  = $(opener).attr('costat');

    if(costat == 0){
        document.getElementById('coutbtn').disabled = false;
    }else{
        document.getElementById('coutbtn').disabled = true;
    }
    
    
    var cash_amnt = document.getElementById('cash_amnt');
    cash_amnt.addEventListener("keydown", function(e) {
        if (invalidChars.includes(e.key)) {
            e.preventDefault();
        }
    });
});


$('#stake_cashout').on('submit',function(e){
    e.preventDefault()
    var mop = document.getElementById("mop").value;
    var acct_name = document.getElementById("acct_name").value;
    var acct_number = document.getElementById("acct_number").value;
    var cash_amnt = document.getElementById("cash_amnt").value;
    
    if(mop!="" && acct_name!="" && acct_number!="" && cash_amnt!=""){
        if(cash_amnt>0){
            Swal.fire({
                title: "Are you sure?",
                text: "do you want to withdraw this staking income?",
                icon: "question",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                confirmButtonText: "Withdraw!"
            }).then((result) => {
                if (result.isConfirmed) {
                    $(".coutspinner").show();
                    document.getElementById('coutbtn').disabled = true;
                    
                    $.ajax({
                        method:'POST',
                        url:'withdarwStake',
                        data:{
                            mop:mop,
                            acct_name:acct_name,
                            acct_number:acct_number,
                            cash_amnt:cash_amnt
                        },
                        success:function(res){
                            $(".coutspinner").hide();
                            document.getElementById('coutbtn').disabled = false;
                            
                            if(res.data == 'success'){
                                toastr["success"]("Successfully done.");
                                $('#stakeCashout').modal('hide');
                                
                                let valsbal = parseFloat(res.stkebalance);
                                let valsbalfrmat = valsbal.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                                document.getElementById('availablestake').innerHTML = valsbalfrmat;
                                
                                let valcoutbal = parseFloat(res.stkecoutbal);
                                let valcoutfrmat = valcoutbal.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                                document.getElementById('coutbaltext').innerHTML = valcoutfrmat;
                                
                                $("#import_raw_table").load('importswithdraw');
                                document.getElementById("mop").value = "";
                                document.getElementById("acct_name").value = "";
                                document.getElementById("acct_number").value = "";
                                document.getElementById("cash_amnt").value = "";
                                
                            }else if(res.data == 'insufficient'){
                                toastr["error"]("Insufficient stake fund earnings!!"); 
                            }else if(res.data == 'tryagain'){
                                toastr["error"]("Try again later!");
                            }else{
                                toastr["error"]("Unable to process request!");
                            }
                        }
                    })
                }
            });
        }else{
            toastr["error"]("Invalid input!"); 
        }
    }else{
        toastr["error"]("All fields are required!");
    }
});





