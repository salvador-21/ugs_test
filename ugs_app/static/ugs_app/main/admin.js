$(document).ready(function(){
    // load_users()
    // function load_users(){
    //     $.ajax({
    //         method:'POST',
    //         url:'getusers',
    //         success:function(res){
    //             $('#acc_tbl').html('')
    
    //             for(d in res.data){
    //                 // console.log(res.data[d].type)
    //                 if(res.data[d].type != 'ADMIN'){
    //                     if(res.data[d].status == 'ACTIVE'){
    //                         stat=' <button type="button" class="btn btn-success btn-sm mb-2 me-2 btn-stat" acc="'+res.data[d].user+'" aid="'+res.data[d].uid+'" utyp="'+res.data[d].type+'"   st="'+res.data[d].status+'" comirate="'+res.data[d].comrate+'">ACTIVE</button>'
    //                     }else if(res.data[d].status == 'INACTIVE'){
    //                         stat=' <button type="button" class="btn btn-warning btn-sm mb-2 me-2 btn-stat" acc="'+res.data[d].user+'" aid="'+res.data[d].uid+'" utyp="'+res.data[d].type+'"  st="'+res.data[d].status+'" comirate="'+res.data[d].comrate+'">INACTIVE</button>'
    //                     }else if(res.data[d].status == 'BANNED'){
    //                         stat=' <button type="button" class="btn btn-danger btn-sm mb-2 me-2 btn-stat" acc="'+res.data[d].user+'" aid="'+res.data[d].uid+'" utyp="'+res.data[d].type+'"  st="'+res.data[d].status+'" comirate="'+res.data[d].comrate+'">BANNED</button>'
    //                     }
    //                     data='<tr>\
    //                  <td>'+res.data[d].datejoin+'</td>\
    //                 <td class="text-white fs-4" style="text-transform: capitalize;">'+res.data[d].user+'</td>\
    //                  <td>'+res.data[d].type+'</td>\
    //                 <td>'+res.data[d].wallet+'</td>\
    //                 <td>'+res.data[d].comrate+'</td>\
    //                 <td style="text-transform: capitalize;" class="fw-bolder">'+res.data[d].agent+'</td>\
    //                 </tr>'
    //                     $('#acc_tbl').append(data)
    //                 }
    //             }
    //         }
    //     })
    // }
    
    // $(document).on('click','.btn-stat',function(){
    //     st=$(this).attr('st')
    //     acc=$(this).attr('acc')
    //     aid=$(this).attr('aid')
    //     comrate=$(this).attr('comirate')
    //     utype=$(this).attr('utyp')
    
    //     $('.acc_type').val(utype)
    //     $('.acc_stat').val(st)
    //     $('.acc_id').val(aid)
    //     $('.uname').text(acc)
    //     $('#agentcommi').val(comrate)
    //     $('.adduser_err').html('')
    //     $('#upuser').modal('show')  
    // })
    
    // $(document).on('submit','#upuser_frm',function(e){
    //     e.preventDefault()
    //     var agntacc_stat  = document.getElementById("agntacc_stat").value;
    //     var agentcommi    = document.getElementById("agentcommi").value;
    //     if(agntacc_stat!=""){
    //         document.getElementById("nfacc_stat").innerHTML = '';
    //         if(agentcommi!=""){
    //             if(agentcommi <=0.12){
    //                 document.getElementById("nfadmincommi").innerHTML = '';
    //                 data=$(this).serializeArray()
    //                 $.ajax({
    //                     method:'POST',
    //                     url:'upstat',
    //                     data:data,
    //                     success:function(res){
    //                         console.log(JSON.stringify(res))
    //                         if(res.data == 'ok'){
    //                             toastr["success"]("Successfully done.");
    //                             document.getElementById("agentcommi").value='';
    //                             $('#upuser').modal('hide')
    //                             load_users()
    //                         }else{
    //                             toastr["error"]("Error processing request!");  
    //                         }
    //                     }
    //                 })
    //             }else{document.getElementById("nfadmincommi").innerHTML = 'Commission rate should not be exceeded in 12% only!'; $("#agentcommi").focus();}   
    //         }else{document.getElementById("nfadmincommi").innerHTML = 'Required!'; $("#agentcommi").focus();}
    //     }else{document.getElementById("nfacc_stat").innerHTML = 'Required!'; $("#agntacc_stat").focus();}
    // })
    
})









$(document).on('click','.adactivateuser',function(){
    accid=$(this).attr('accid')
    acc=$(this).attr('acct')
    comrate=$(this).attr('comrate')
    usertype=$(this).attr('plstat')
    userstat=$(this).attr('userstat')
    agentId=$('#agentid').val()
    myagent=$(this).attr('myagent')
    
    if(agentId==myagent){
        if(usertype == 'PLAYER'){
            document.getElementById('adcomrate').readOnly  = true;
            document.getElementById('usertype').disabled  = false;
            document.getElementById('adcomrate').value = '0';
            $('#nfcommission').text('Commissions are applicable only to agent accounts.')
        }else{
            if(agentId==myagent){
                document.getElementById('adcomrate').readOnly  = false;
                document.getElementById('usertype').disabled  = false;
                document.getElementById('adcomrate').value = (comrate * 100).toString();
                
                $('#nfcommission').text('')
            }else{
                document.getElementById('adcomrate').readOnly  = true;
                document.getElementById('usertype').disabled  = true;
                document.getElementById('adcomrate').value = (comrate * 100).toString();
                $('#nfcommission').text('Updating commission and account category only applicable into your invite!!')
            } 
        }
    }else{
        document.getElementById('adcomrate').readOnly  = true;
        document.getElementById('usertype').disabled  = true;
        document.getElementById('adcomrate').value = (comrate * 100).toString();
        $('#nfcommission').text('Updating commission and account category only applicable into your invite!!')
    }
    
    $('.usertype').val(usertype)
    $('.acc_stat').val(userstat)
    $('.acct_id').val(accid)
    $('.unames').text(acc)
    $('#admin_upuser').modal('show')
    
    var adcomrate = document.getElementById('adcomrate');
    adcomrate.addEventListener("keydown", function(e) {
        if (invalidCharcoms.includes(e.key)) {
            e.preventDefault();
        }
    });
})

$(document).on('change','.usertype',function(){
    let usertype = $(this).val();
    if(usertype == 'PLAYER'){
        document.getElementById('adcomrate').readOnly  = true;
        document.getElementById('adcomrate').value = '0';
        $('#nfcommission').text('Commissions are applicable only to agent accounts.')
    }else{
        document.getElementById('adcomrate').readOnly  = false;
        document.getElementById('adcomrate').value = (comrate * 100).toString();
        $('#nfcommission').text('')
    }
})

function inputFocuss(x) {
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


$(document).on('submit','#upuser_frm',function(e){
    e.preventDefault()
    var plstatus   = document.getElementById("plstatus").value;
    var commission = document.getElementById("adcomrate").value;
    var acct_id    = document.getElementById("acct_id").value;
    var commirate  = document.getElementById("commirate").value;
    var usertype   = document.getElementById("usertype").value;
    var userpage   = document.getElementById("usercatpage").value;
    var outbutton = document.getElementById('adusercombtn');
    
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
                    if(comrate >= comm){
                        if(usertype == "ADMIN" || usertype == "MASTER OPERATOR" || usertype == "INCORPORATOR" || usertype == "SUB ADMIN" || usertype == "SUB OPERATOR" || usertype == "MASTER AGENT"){
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
                                    $(".acspinner").show();
                                    outbutton.disabled = true;
                                    $.ajax({
                                        method:'POST',
                                        url:'adminActivateUser',
                                        data:data,
                                        success:function(res){
                                            $(".acspinner").hide();
                                            outbutton.disabled = false;
                                            if(res.data == 'ok'){
                                                document.getElementById('adcomrate').readOnly  = true;
                                                // document.getElementById("commirate").value = res.nwcommi; 
                                                // document.getElementById("usertype").value="";
                                                document.getElementById("plstatus").value="";
                                                
                                                toastr["success"]("Successfully done.");
                                                document.getElementById("adcomrate").value='';
                                                $('#admin_upuser').modal('hide')
                                                
                                                $("#import_raw_table").load('import_adminUser');
                                                
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
            }else{document.getElementById("nfcommission").innerHTML = 'Required!'; $("#adcomrate").focus();}
        }else{document.getElementById("nfplstatus").innerHTML = 'Required!'; $("#plstatus").focus();}
    }else{document.getElementById("nfusertype").innerHTML = 'Required!'; $("#usertype").focus();}
})





































$('#addaccount_reg').on('submit',function(e){
    e.preventDefault()
    $(".addusrs").show();
    $('.adduser_err').html('')
    data=$(this).serializeArray()
    if($('.pass1').val() != $('.pass2').val()){
        $('.adduser_err').append('<div class="alert alert-danger alert-dismissible fade show" role="alert">\
        <strong>Password Not Matched!</strong>\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>')
        }else{
            var outbutton = document.getElementById('aduserbtn');
            outbutton.disabled = true;
            $.ajax({
                method:'POST',
                url:'account_reg',
                data:data,
                success:function(res){
                    $(".addusrs").hide();
                    outbutton.disabled = false;
                    if(res.data == 'ok'){
                        $('#addaccount_reg').trigger('reset')
                        $("#import_raw_table").load('import_adminUser');
                    }else{
                        toastr["error"]("Please try again after a few seconds.");  
                    }
                }
            })
            
        }
    })
    
    
    
    
    
    
    
    
    
    
    
    
    
    function inputstake(x) {
        var stakeamnt = document.getElementById('stakeamnt');
        stakeamnt.addEventListener("keydown", function(e) {
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
    
    $('#stakingForm').on('submit', function(e) {
        e.preventDefault();
        var valuserid = document.getElementById('userid').value;
        var valstakeamnt = document.getElementById('stakeamnt').value;
        var stakebtn = document.getElementById('stakebtn');
        
        if(valuserid && valstakeamnt){
            var values = valuserid.split('|');
            var userId = values[0];
            if(valstakeamnt >=1){
                let valstakeamnts = parseFloat(valstakeamnt);
                let formattedAmount = valstakeamnts.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                Swal.fire({
                    title: "SEND STAKING AMOUNT OF <br>"+formattedAmount +"?",
                    text: "send staking amount",
                    icon: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#3085d6",
                    cancelButtonColor: "#d33",
                    confirmButtonText: "Proceed!"
                }).then((result) => {
                    if (result.isConfirmed) {
                        $(".loadstake").show();
                        stakebtn.disabled = true;
                        $.ajax({
                            method: 'POST',
                            url:'loadStaking',
                            data:{valstakeamnt:valstakeamnt,userId:userId},
                            success: function(res) {
                                $(".loadstake").hide();
                                stakebtn.disabled = false;
                                if (res.data === 'ok') {
                                    toastr["success"]("Stake amount successfully sent!");
                                    $('#stakingForm').trigger('reset')
                                    $('#userid').selectize()[0].selectize.clear();
                                    document.getElementById('stakeamnt').value='';
                                    $("#import_raw_table").load('load_stake_tbl');
                                }else {
                                    toastr["warning"]("Error: " + JSON.stringify(res.errors));
                                }
                            }
                        });
                    }
                });
            }else{
                toastr["error"]("Invalid inputs!");
            }
        }else{
            toastr["error"]("All fields are required!");
        }
    });
    
    
    function selecteduser(option){
        var optionVal = option.value;
        if(optionVal){
            var values = optionVal.split('|');
            var userId = values[0];
            var username = values[1];
            var fullname = values[2];
        }else{
            var userId = "";
            var username = "";
            var fullname = "";
        }
        document.getElementById('uname').innerHTML=username;
        document.getElementById('fname').innerHTML=fullname;
        document.getElementById('sendto').innerHTML="("+username+")";
    }
    function stakeAmount(amntVal){
        var amntValue = amntVal.value || 0;
        let amntValues = parseFloat(amntValue);
        if (isNaN(amntValues)) {
            amntValues = 0;
        }
        let formatamnt = amntValues.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
        document.getElementById('amtname').innerHTML=formatamnt;
    }
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    // loading
    $(document).on('click','.adloadingtrans',function(){
        $('#adloadingstation').modal('show')
    });
    
    $(document).on('change', '.adtransactype', function() {
        var transacval = $(this).val();
        $.ajax({
            method: 'POST',
            url: 'adpointsTransaction',
            data: {
                transacval: transacval,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(res) {
                $("#admptranstype").html(res); 
                $("#adprocessbtn").html(transacval); 
            }
        });
        
    });
    
    
    function pointsAmount(amntVal) {
        let pointamnt = amntVal.value || 0;
        let pointamnts = parseFloat(pointamnt);
        if (isNaN(pointamnts)) {
            pointamnts = 0;
        }
        let poitformat = pointamnts.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
        document.getElementById('vpoint_amnt').innerHTML = poitformat;
    }
    
    
    $(document).on('change','.adwithdrawaccount',function(){
        var withdrawacnt = $(this).val();
        var transtype = document.getElementById('adactiontype').value
        let selectedValues = withdrawacnt.split(' | ');
        let userid = selectedValues[0];
        let username = selectedValues[1];
        
        $.ajax({
            method: 'POST',
            url: 'adwithdrawal_accnt',
            data: {
                withdrawacnt: userid,
                transtype: transtype,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(res) {
                let formattedWalletBal = parseFloat(res.walletbal).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                document.getElementById('adwallet_bal').innerHTML = formattedWalletBal;
                document.getElementById('adwalletpoints').value = res.walletbal;
                if(username){
                    document.getElementById('adselectedusr').innerHTML=username;
                }  
            }
        });
    })
    
    $('#adpointsForm').on('submit', function(e) {
        e.preventDefault();
        var transtype   = document.getElementById("adtransaction").value;
        var accountid   = document.getElementById("adwithdrawaccount").value;
        var load_point   = document.getElementById("adload_point").value;
        var walletpoints   = document.getElementById("adwalletpoints").value;
        var outbutton = document.getElementById('adoutbtn');
        
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
                                $(".loadspinner").show();
                                let randomDelay = Math.floor(Math.random() * 1000) + 1000;
                                // console.log('Delay:', randomDelay, 'milliseconds');
                                setTimeout(function() {
                                    $.ajax({
                                        method: 'POST',
                                        url:'adpoints_transactions',
                                        data:{userid:userid, load_point:load_point, transtype:transtype},
                                        success: function(res) {
                                            outbutton.disabled = false;
                                            $(".loadspinner").hide();
                                            if (res.data === 'success') {
                                                toastr["success"]("Sent Successfully.");
                                                document.getElementById('adtransaction').value="";
                                                $('#adwithdrawaccount')[0].selectize.clear();
                                                document.getElementById('adload_point').value="";
                                                
                                                let fWalletBal = parseFloat(res.newPoints).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                                                document.getElementById('walletbal').innerHTML = fWalletBal;
                                                
                                                $('#adloadingstation').modal('hide')
                                                $("#import_raw_table").load('adload_points_table');
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
    
    
    $(document).on('click','.stkwithdrawconform',function(){
        var rowid=$(this).attr('rowid')
        var adw_code=$(this).attr('adw_code')
        var adw_amount=$(this).attr('adw_amount')
        var adw_mop=$(this).attr('adw_mop')
        var adw_acname=$(this).attr('adw_acname')
        var adw_acnum=$(this).attr('adw_acnumber')
        let vadw_amount = parseFloat(adw_amount);
        let fadw_amount = vadw_amount.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
        
        $('#adstake_withdrawal').modal('show')
        $('#rwid').val(rowid)
        $('#swcode').val(adw_code)
        $('#swamount').text(fadw_amount)
        $('#swmop').val(adw_mop)
        $('#swacname').val(adw_acname)
        $('#swacnum').val(adw_acnum)
    });
    
    
    
    
    $('#stakeCashoutForm').on('submit', function(e) {
        e.preventDefault();
        var rwid   = document.getElementById("rwid").value;
        if(rwid!=""){
            Swal.fire({
                title: "Are you sure?",
                text: "you want to process this withdrawal request?",
                icon: "question",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                confirmButtonText: "Process"
            }).then((result) => {
                if (result.isConfirmed) {
                    $(".stwspinner").show();
                    $.ajax({
                        method: 'POST',
                        url:'adstakewtdrawconfirm',
                        data:{rwid:rwid},
                        success: function(res) {
                            $(".stwspinner").hide();
                            if (res.data === 'success') {
                                Swal.fire({
                                    title: "Successfully Confirmed!",
                                    icon: "success"
                                });
                                $('#adstake_withdrawal').modal('hide')
                                $("#import_raw_table").load('ad_withdraw_confirmed');
                            }else if (res.data === 'error') {
                                toastr["error"]("Error processing request!");
                            }else{
                                toastr["error"]("Invalid inputs!");   
                            } 
                        }
                    });  
                }
            });
        }else{
            toastr["error"]("Unable to proceed!"); 
        }
    });
    
    
    
    
    
    
    $(document).on('click','.coutconfirm',function(){
        var rowid=$(this).attr('rowid')
        var adw_code=$(this).attr('adw_code')
        var adw_amount=$(this).attr('adw_amount')
        var adw_mop=$(this).attr('adw_mop')
        var adw_acname=$(this).attr('adw_acname')
        var adw_acnum=$(this).attr('adw_acnumber')
        let vadw_amount = parseFloat(adw_amount);
        let fadw_amount = vadw_amount.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
        
        $('#stkcomswithdraw').modal('show')
        $('#rrwid').val(rowid)
        $('#srwcode').val(adw_code)
        $('#srwamount').text(fadw_amount)
        $('#srwmop').val(adw_mop)
        $('#srwacname').val(adw_acname)
        $('#srwacnum').val(adw_acnum)
    });
    
    
    
    $('#stkcomcoutForm').on('submit', function(e) {
        e.preventDefault();
        var rwid   = document.getElementById("rrwid").value;
        var btncocoms = document.getElementById('btncocoms');
        if(rwid!=""){
            Swal.fire({
                title: "Are you sure?",
                text: "you want to process this withdrawal request?",
                icon: "question",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                confirmButtonText: "Process"
            }).then((result) => {
                if (result.isConfirmed) {
                    $(".stwspinner").show();
                    btncocoms.disabled = true;
                    $.ajax({
                        method: 'POST',
                        url:'confirmcocoms',
                        data:{rwid:rwid},
                        success: function(res) {
                            $(".stwspinner").hide();
                            btncocoms.disabled = false;
                            if (res.data === 'success') {
                                Swal.fire({
                                    title: "Successfully Confirmed!",
                                    icon: "success"
                                });
                                $('#stkcomswithdraw').modal('hide')
                                $("#import_cocoms_tbl").load('ad_comco_tbl');
                            }else if (res.data === 'error') {
                                toastr["error"]("Error processing request!");
                            }else{
                                toastr["error"]("Invalid inputs!");   
                            } 
                        }
                    });  
                }
            });
        }else{
            toastr["error"]("Unable to proceed!"); 
        }
    });
    
    
    
    
    
    
    $(document).on('change', '.fightEvent', function() {
        var geventval = $(this).val();
        console.log(geventval)
        if (geventval !== "") {
            $.ajax({
                method: 'POST',
                url: 'gamefight',
                data: {
                    geventval: geventval,
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                },
                success: function(res) {
                    $("#flogsnum").html(res);
                    const selectElement = document.getElementById('fgnum'); 
                    selectElement.disabled = false;
                },
                error: function(xhr, status, error) {
                    console.error("Error:", error);
                }
            });
        } else {
            const selectElement = document.getElementById('fgnum'); 
            selectElement.disabled = true;
            selectElement.value = 0;
        }
    });
    
    
    
    
    $(document).on('change', '.fightlogs', function() {
        var eventid = document.getElementById('fightevent').value;
        var fnum = document.getElementById('fgnum').value;
        let fvalue = fnum.split(' | ');
        let fgnum = fvalue[0];
        let mpout = fvalue[1];
        let wpout = fvalue[2];
        let winner = fvalue[3];
        let prevwin = fvalue[4];
        
        
        if (eventid !== "" && fgnum !== "") {
            $.ajax({
                method: 'POST',
                url: 'gamefightlogs',
                data: {
                    eventid: eventid,fgnum: fgnum,
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                },
                success: function(res) {
                    document.getElementById('mpayout').innerHTML=mpout;
                    document.getElementById('wpayout').innerHTML=wpout;
                    document.getElementById('fresult').innerHTML=winner;
                    document.getElementById('revertwin').innerHTML=prevwin;
                    
                    $("#importbetlogs").html(res);
                },
                error: function(xhr, status, error) {
                    toastr["error"]("Error processing request!");  
                }
            });
        } else {
            toastr["error"]("Invalid inputs!");   
        }
    });
    
    
    
    $('.coutstatus').on('change',function(){
        const checkbox = $('#flexSwitchCheckChecked');
        const ftypeSpan = $('.ftype');
        
        if (checkbox.is(':checked')) {
            ftypeSpan.text('Open Withdrawal').removeClass('text-danger').addClass('text-success');
            var coutstat = 0
        } else {
            ftypeSpan.text('Closed Withdrawal').removeClass('text-success').addClass('text-danger');
            var coutstat = 1
        }
        $.ajax({
            method: 'POST',
            url: 'stakecoutstatus',
            data: {
                coutstat: coutstat,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(res) {
                if (res.data === 'success') {
                    toastr["success"]("Successfully updated."); 
                } else{
                    toastr["error"]("Error processing request!"); 
                }
            },
            error: function(xhr, status, error) {
                toastr["error"]("Error processing request!");  
            }
        });
    })





    $('.coutseranings').on('change',function(){
        const checkbox = $('#SwitchCheckChecked');
        const ftypeSpan = $('.ftype');
        
        if (checkbox.is(':checked')) {
            ftypeSpan.text('Open Withdrawal').removeClass('text-danger').addClass('text-success');
            var coutstat = 0
        } else {
            ftypeSpan.text('Closed Withdrawal').removeClass('text-success').addClass('text-danger');
            var coutstat = 1
        }
        $.ajax({
            method: 'POST',
            url: 'stakeearningscout',
            data: {
                coutstat: coutstat,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(res) {
                if (res.data === 'success') {
                    toastr["success"]("Successfully updated."); 
                } else{
                    toastr["error"]("Error processing request!"); 
                }
            },
            error: function(xhr, status, error) {
                toastr["error"]("Error processing request!");  
            }
        });
    })
    
    
    
    
    $(document).on('click','.admupdatepass',function(){
        accid=$(this).attr('accid')
        realpass=$(this).attr('realpass')
        document.getElementById('usrid').value=accid;
        document.getElementById('rlpass').value=realpass;
        $('#admin_uppassword').modal('show')
    })






    
    $('#adupdateForm').on('submit', function (e) {
        e.preventDefault();
    
        const rlpass = document.getElementById("rlpass").value.trim();
        const newpass = document.getElementById("newpass").value.trim();
        const usrid = document.getElementById("usrid").value.trim();
        const btncocoms = document.getElementById("adupdatebtn");
    
        if (newpass && usrid && rlpass) {
            Swal.fire({
                title: "Are you sure?",
                text: "You want to change the password for this user account?",
                icon: "question",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                confirmButtonText: "Save Changes"
            }).then((result) => {
                if (result.isConfirmed) {
                    $(".upusrspin").show();
                    btncocoms.disabled = true;
    
                    $.ajax({
                        method: 'POST',
                        url: 'uchangepass',
                        data: {
                            usrid: usrid,
                            newpass: newpass,
                            rlpass: rlpass,
                            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
                        },
                        success: function (res) {
                            $(".upusrspin").hide();
                            btncocoms.disabled = false;
    
                            if (res.status === 'success') {
                                Swal.fire({
                                    title: "Successfully changed!",
                                    icon: "success"
                                });
                                document.getElementById("newpass").value='';
                                $('#admin_uppassword').modal('hide');
                                $("#import_raw_table").load('import_adminUser');
                            } else {
                                toastr["error"](res.message || "Error processing request!");
                            }
                        },
                        error: function () {
                            $(".upusrspin").hide();
                            btncocoms.disabled = false;
                            toastr["error"]("Failed to communicate with the server!");
                        }
                    });
                }
            });
        } else {
            toastr["error"]("All fields are required!");
        }
    });
    
    
    
    