$(document).on('click','.btn-actvateplyr',function(){
    accid=$(this).attr('accid')
    acc=$(this).attr('acct')
    comrate=$(this).attr('comrate')
    usertype=$(this).attr('pltype')
    plstatus=$(this).attr('plstatus')
    
    if(usertype == 'PLAYER'){
        document.getElementById('commission').readOnly  = true;
        document.getElementById('commission').value = '0';
        $('#nfcommission').text('Commissions are applicable only to agent accounts.')
    }else{
        document.getElementById('commission').readOnly  = false;
        document.getElementById('commission').value = (comrate * 100).toString();
        $('#nfcommission').text('')
    }
    
    $('#usertype').val(usertype)
    $('#plstatus').val(plstatus)
    $('.acct_id').val(accid)
    $('.unames').text(acc)
    $('#activateplyr').modal('show')
    var commission = document.getElementById('commission');
    commission.addEventListener("keydown", function(e) {
        if (invalidCharcoms.includes(e.key)) {
            e.preventDefault();
        }
    });
})

$(document).on('change','.usertype',function(){
    let usertype = $(this).val();
    if(usertype == 'PLAYER'){
        document.getElementById('commission').readOnly  = true;
        document.getElementById('commission').value = '0';
        $('#nfcommission').text('Commissions are applicable only to agent accounts.')
    }else{
        document.getElementById('commission').readOnly  = false;
        document.getElementById('commission').value = (comrate * 100).toString();
        $('#nfcommission').text('')
    }
})

function inputFocus(x) {
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


$(document).on('submit','#activate_form',function(e){
    e.preventDefault()
    var plstatus   = document.getElementById("plstatus").value;
    var commission = document.getElementById("commission").value;
    var acct_id    = document.getElementById("acct_id").value;
    var commirate  = document.getElementById("commirate").value;
    var usertype   = document.getElementById("usertype").value;
    var userpage   = document.getElementById("usercatpage").value;
    
    if(usertype!=""){
        document.getElementById("nfusertype").innerHTML = '';
        if(plstatus!=""){
            document.getElementById("nfplstatus").innerHTML = '';
            if(commission!=""){
                document.getElementById("nfcommission").innerHTML = '';
                if(acct_id!=""){
                    document.getElementById("notifid").innerHTML = '';
                    var commito = commission/100;
                    var comrate = parseFloat(commirate);
                    var comm = parseFloat(commito);
                    if(comrate > comm){
                        if(usertype == "MASTER OPERATOR" || usertype == "INCORPORATOR" || usertype == "SUB ADMIN" || usertype == "SUB OPERATOR" || usertype == "MASTER AGENT"){
                            if(comm>0){
                                var pass=1;
                            }else{
                                var pass=0;
                            }
                        }else{
                            var pass=1;
                        }
                        if(pass==1){
                            data=$(this).serializeArray()
                            Swal.fire({
                                title: "Are you sure?",
                                text: "do you want to process this account activation?",
                                icon: "question",
                                showCancelButton: true,
                                confirmButtonColor: "#3085d6",
                                cancelButtonColor: "#d33",
                                confirmButtonText: "Proceed!"
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    $(".agspinner").show();
                                    $.ajax({
                                        method:'POST',
                                        url:'upplyrstat',
                                        data:data,
                                        success:function(res){
                                            $(".agspinner").hide();
                                            if(res.data == 'ok'){
                                                document.getElementById('commission').readOnly  = true;
                                                document.getElementById("commirate").value = res.nwcommi; 
                                                document.getElementById("commis").innerHTML = res.nwcommi; 
                                                document.getElementById("usertype").value="";
                                                document.getElementById("plstatus").value="";
                                                
                                                toastr["success"]("Successfully done.");
                                                document.getElementById("commission").value='';
                                                $('#activateplyr').modal('hide')
                                                
                                                if(userpage =="ACTIVE PLAYER"){
                                                    $("#import_raw_table").load('load_player_user');
                                                }else if(userpage =="ACTIVE AGENT"){
                                                    $("#import_raw_table").load('load_agent_user');
                                                }else{
                                                    $("#import_raw_table").load('load_new_user');
                                                }
                                                
                                            }else{
                                                toastr["error"]("Error processing request!");  
                                            }
                                        }
                                    })
                                }
                            });
                        }else{toastr["error"]("Invalid commission entry!");}
                    }else{toastr["error"]("Current commission is not enough!");}
                }else{document.getElementById("notifid").innerHTML = 'Required!'; $("#acct_id").focus();}
            }else{document.getElementById("nfcommission").innerHTML = 'Required!'; $("#commission").focus();}
        }else{document.getElementById("nfplstatus").innerHTML = 'Required!'; $("#plstatus").focus();}
    }else{document.getElementById("nfusertype").innerHTML = 'Required!'; $("#usertype").focus();}
})














$('#convertPointsform').on('submit', function(e) {
    e.preventDefault();
    var convertpoint   = document.getElementById("convertpoint").value;
    var vlcomms_bal   = document.getElementById("vlcomms_bal").value;
    
    if(convertpoint && convertpoint.trim() !== "" && vlcomms_bal && vlcomms_bal.trim() !== ""){
        var convertpoint = parseFloat(convertpoint);
        var vlcomms_bal = parseFloat(vlcomms_bal);
        if(convertpoint>=1){
            if(vlcomms_bal>=1 && vlcomms_bal>=convertpoint){
                Swal.fire({
                    title: "Are you sure?",
                    text: "do you want to convert this commission?",
                    icon: "question",
                    showCancelButton: true,
                    confirmButtonColor: "#3085d6",
                    cancelButtonColor: "#d33",
                    confirmButtonText: "Proceed!"
                }).then((result) => {
                    if (result.isConfirmed) {
                        document.getElementById('convertbtn').disabled = true; 
                        $(".convertspin").show();
                        $.ajax({
                            method: 'POST',
                            url:'convertProcess',
                            data:{convertpoint:convertpoint},
                            success: function(res) {
                                $(".convertspin").fadeOut();
                                document.getElementById('convertbtn').disabled = false; 
                                if (res.data === 'ok') {
                                    toastr["success"]("Commission successfully converted into your points.");
                                    document.getElementById('convertpoint').value=0;
                                    let formattedWalletBal = parseFloat(res.newcomms).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                                    document.getElementById('comssBal').innerHTML = formattedWalletBal;
                                    document.getElementById('vlcomms_bal').value = res.newcomms;
                                    
                                    let dashWalletBal = parseFloat(res.newwalbal).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                                    document.getElementById('dashwallet').innerHTML = dashWalletBal;
                                    $("#converted_table").load('load_converted_table');
                                    
                                }else if (res.data === 'insufficient') {
                                    toastr["error"]("Insufficient rewads balance");  
                                }else if (res.data === 'invalid') {
                                    toastr["error"]("Invalid inputs!");  
                                }else if (res.data === 'tryagain') {
                                    toastr["error"]("Please try again after a few seconds.");  
                                } else {
                                    toastr["warning"]("Error: " + JSON.stringify(res.errors));
                                }
                            }
                        });
                    }
                })
            }else{
                toastr["error"]("Insufficient rewads balance");  
            }
        }else{
            toastr["error"]("Invalid inputs!");  
        }
    }else{
        toastr["error"]("Invalid inputs!");  
    }
});









// loading
// $(document).on('click','.loadingtrans',function(){
//     $('#agentloadpoints').modal('show')
// })
$(document).on('change', '.transactype', function() {
    var transacval = $(this).val();
    $.ajax({
        method: 'POST',
        url: 'pointsTransaction',
        data: {
            transacval: transacval,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        success: function(res) {
            $("#mptranstype").html(res); 
            $("#processbtn").html(transacval); 
            document.getElementById('outbtn').disabled = false;
        }
    });
});

function agpointAmnt(amntVal) {
    let pointamnt = amntVal.value || 0;
    let pointamnts = parseFloat(pointamnt);
    if (isNaN(pointamnts)) {
        pointamnts = 0;
    }
    let poitformat = pointamnts.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    document.getElementById('agpointamnt').innerHTML = poitformat;
}

$(document).on('change','.withdrawaccount',function(){
    var withdrawacnt = $(this).val();
    var transtype = document.getElementById('actiontype').value
    let selectedValues = withdrawacnt.split(' | ');
    let userid = selectedValues[0];
    let username = selectedValues[1];
    
    $.ajax({
        method: 'POST',
        url: 'withdrawal_accnt',
        data: {
            withdrawacnt: userid,
            transtype: transtype,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        success: function(res) {
            let formattedWalletBal = parseFloat(res.walletbal).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            document.getElementById('wallet_bal').innerHTML = formattedWalletBal;
            document.getElementById('walletpoints').value = res.walletbal;
            if(username){
                document.getElementById('selectedusr').innerHTML=username;
            }  
        }
    });
})

$('#pointsForm').on('submit', function(e) {
    e.preventDefault();
    var transtype   = document.getElementById("transaction").value;
    var accountid   = document.getElementById("withdrawaccount").value;
    var load_point   = document.getElementById("load_point").value;
    var walletpoints   = document.getElementById("walletpoints").value;
    var outbutton = document.getElementById('outbtn');
    
    if (transtype && transtype.trim() !== "" && accountid && accountid.trim() !== "" && load_point && load_point.trim() !== "" && walletpoints && walletpoints.trim() !== "") {
        load_point = parseFloat(load_point)
        balances = parseFloat(walletpoints)
        let selectedValues = accountid.split(' | ');
        let userid = selectedValues[0];
        let isNumber = /^\d+(\.\d+)?$/.test(load_point); 
        if (isNumber) {
            if (balances>=1 && balances >= load_point) {
                if (load_point!="" && load_point >=1) {
                    Swal.fire({
                        title: "Are you sure?",
                        text: "you want to " + transtype + " points now?",
                        icon: "question",
                        showCancelButton: true,
                        confirmButtonColor: "#3085d6",
                        cancelButtonColor: "#d33",
                        confirmButtonText: transtype
                    }).then((result) => {
                        if (result.isConfirmed) {
                            outbutton.disabled = true;
                            $(".addrowspin").show();
                            let randomDelay = Math.floor(Math.random() * 1000) + 1000;
                            console.log('Delay:', randomDelay, 'milliseconds');
                            setTimeout(function() {
                                $.ajax({
                                    method: 'POST',
                                    url:'points_transactions',
                                    data:{userid:userid, load_point:load_point, transtype:transtype},
                                    success: function(res) {
                                        outbutton.disabled = false;
                                        $(".addrowspin").hide();
                                        if (res.data === 'success') {
                                            
                                            toastr["success"]("Successfully sent!");
                                            $('#withdrawaccount')[0].selectize.clear();
                                            document.getElementById('transaction').value="";
                                            document.getElementById('load_point').value="";
                                            
                                            let fWalletBal = parseFloat(res.newPoints).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                                            document.getElementById('walletbal').innerHTML = fWalletBal;
                                            document.getElementById('agpointamnt').innerHTML = "0.00";
                                            
                                            $("#import_raw_table").load('load_points_table');
                                        }else if (res.data === 'error') {
                                            toastr["error"]("Error processing request!");
                                        }else if (res.data === 'insufficient') {
                                            toastr["error"]("Insufficient Points Balance!");   
                                        }else if (res.data === 'tryagain') {
                                            toastr["error"]("Please try again after a few seconds.");  
                                        }else{
                                            toastr["error"]("Invalid inputs!");   
                                        } 
                                    }
                                });
                            }, randomDelay);
                        }
                    });
                }else{
                    toastr["error"]("Invalid inputs!");   
                }
            }else{
                toastr["error"]("Insufficient Points Balance!");    
            }
        } else {
            toastr["error"]("Invalid inputs!");  
        }
    }else{
        toastr["error"]("All fields are required!");   
    }
});




function inputstkrewars(x) {
    var rewardsamount = document.getElementById('rewardsamount');
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



$('#stakeclaimreward').on('submit', function(e) {
    e.preventDefault();
    
    var mop   = document.getElementById("mop").value;
    var acct_name   = document.getElementById("acct_name").value;
    var acct_number   = document.getElementById("acct_number").value;
    var rewardsamount   = document.getElementById("rewardsamount").value;
    var currentrewards   = document.getElementById("currentrewards").value;
    
    if(rewardsamount && rewardsamount.trim() !== "" && currentrewards && currentrewards.trim() !== ""){
        var rewardsamount = parseFloat(rewardsamount);
        var currentrewards = parseFloat(currentrewards);
        if(rewardsamount>=100){
            if(currentrewards>=1 && currentrewards>=rewardsamount){
                Swal.fire({
                    title: "Are you sure?",
                    text: "do you want to withdraw this stake rewards?",
                    icon: "question",
                    showCancelButton: true,
                    confirmButtonColor: "#3085d6",
                    cancelButtonColor: "#d33",
                    confirmButtonText: "Proceed!"
                }).then((result) => {
                    if (result.isConfirmed) {
                        document.getElementById('stkeclaimbtn').disabled = true; 
                        $(".stkeclaimspin").show();
                        $.ajax({
                            method: 'POST',
                            url:'../stakerewardsWithdraw',
                            data:{
                                mop:mop,
                                acct_name:acct_name,
                                acct_number:acct_number,
                                rewardsamount:rewardsamount
                            },
                            success: function(res) {
                                $(".stkeclaimspin").fadeOut();
                                document.getElementById('stkeclaimbtn').disabled = false; 
                                if (res.data === 'ok') {
                                    toastr["success"]("Stake rewards withdrawal successfully done.");
                                    
                                    let formattedWalletBal = parseFloat(res.newcomms).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                                    document.getElementById('stakerewardbal').innerHTML = formattedWalletBal;
                                    
                                    let newcalimbalfrm = parseFloat(res.newcalimbal).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                                    document.getElementById('newclaimbal').innerHTML = newcalimbalfrm;
                                    document.getElementById('currentrewards').value = res.newcomms;
                                    document.getElementById("mop").value='';
                                    document.getElementById("acct_name").value='';
                                    document.getElementById("acct_number").value='';
                                    document.getElementById('rewardsamount').value=0;
                                    
                                    $("#stake_withdraw_tbl").load('import_stakecom_withdrw');
                                    
                                }else if (res.data === 'insufficient') {
                                    toastr["error"]("Insufficient points balance");  
                                }else if (res.data === 'invalid') {
                                    toastr["error"]("Invalid inputs!");  
                                }else if (res.data === 'tryagain') {
                                    toastr["error"]("Please try again after a few seconds.");  
                                } else {
                                    toastr["warning"]("Error: " + JSON.stringify(res.errors));
                                }
                            }
                        });
                    }
                })
            }else{
                toastr["error"]("Insufficient rewads balance");  
            }
        }else{
            toastr["error"]("Invalid inputs!");  
        }
    }else{
        toastr["error"]("Invalid inputs!");  
    }
});





$(document).on('change', '.gameevent', function() {
    var geventval = $(this).val();
    if (geventval !== "") {
        $('.tablespinner').show();
        $.ajax({
            method: 'POST',
            url: 'bettingcomms',
            data: {
                geventval: geventval,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(res) {
                $("#betcommslogs").html(res);
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });
    }
});

















