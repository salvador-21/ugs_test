$(document).ready(function(){
    
})









$(document).on('click','.activateaccount',function(){
    accid=$(this).attr('accid')
    acc=$(this).attr('acct')
    comrate=$(this).attr('comrate')
    usertype=$(this).attr('plstat')
    userstat=$(this).attr('userstat')
    agentId=$('#agentid').val()
    myagent=$(this).attr('myagent')
    
    if(agentId==myagent){
        if(usertype == 'PLAYER' || usertype == 'DECLARATOR'){
            document.getElementById('commission').readOnly  = true;
            document.getElementById('usertype').disabled  = false;
            document.getElementById('commission').value = '0';
            $('#nfcommission').text('Commissions are applicable only to agent accounts.')
        }else{
            if(agentId==myagent){
                document.getElementById('commission').readOnly  = false;
                document.getElementById('usertype').disabled  = false;
                document.getElementById('commission').value = (comrate * 100).toFixed(0);
                $('#nfcommission').text('')
            }else{
                document.getElementById('commission').readOnly  = true;
                document.getElementById('usertype').disabled  = true;
                document.getElementById('commission').value = (comrate * 100).toFixed(0);
                $('#nfcommission').text('Updating commission and account category only applicable into your invite!!')
            } 
        }
    }else{
        document.getElementById('commission').readOnly  = true;
        document.getElementById('usertype').disabled  = true;
        document.getElementById('commission').value = (comrate * 100).toFixed(0);
        $('#nfcommission').text('Updating commission and account category only applicable into your invite!!')
    }
    
    $('.usertype').val(usertype)
    $('.acc_stat').val(userstat)
    $('.acct_id').val(accid)
    $('.unames').text(acc)
    $('#superadmin_upuser').modal('show')
    
    var commission = document.getElementById('commission');
    commission.addEventListener("keydown", function(e) {
        if (invalidCharcoms.includes(e.key)) {
            e.preventDefault();
        }
    });
})

$(document).on('change','.usertype',function(){
    let usertype = $(this).val();
    if(usertype == 'PLAYER' || usertype == 'DECLARATOR'){
        document.getElementById('commission').readOnly  = true;
        document.getElementById('commission').value = '0';
        $('#nfcommission').text('Commissions are applicable only to agent accounts.')
    }else{
        document.getElementById('commission').readOnly  = false;
        document.getElementById('commission').value = (comrate * 100).toFixed(0);
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
                                    $(".upuser").show();
                                    $.ajax({
                                        method:'POST',
                                        url:'supradmiactiveuser',
                                        data:data,
                                        success:function(res){
                                            $(".upuser").hide();
                                            if(res.data == 'ok'){
                                                toastr["success"]("Successfully done.");
                                                $('#superadmin_upuser').modal('hide')
                                                $("#import_row_table").load('import_super_adminuser');
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








$('#spadaccount_reg').on('submit',function(e){
    $(".spuser").show();
    e.preventDefault()
    $('.adduser_err').html('')
    data=$(this).serializeArray()
    if($('.pass1').val() != $('.pass2').val()){
        $('.adduser_err').append('<div class="alert alert-danger alert-dismissible fade show" role="alert">\
        <strong>Password Not Matched!</strong>\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>')
        }else{
            var outbutton = document.getElementById('spadbtn');
            outbutton.disabled = true;
            $.ajax({
                method:'POST',
                url:'account_reg',
                data:data,
                success:function(res){
                    $(".spuser").hide();
                    outbutton.disabled = false;
                    if(res.data == 'ok'){
                        $('#spadaccount_reg').trigger('reset')
                        toastr["success"]("Successfully registered!");
                        $("#import_row_table").load('import_super_adminuser');
                        }else{
                            toastr["error"]("Please try again after a few seconds.");  
                        }
                    }
                })
                
            }
        })
        
        
        
        
        
        
        
        
        
        
        function pointsAmount(amntVal) {
            let pointamnt = amntVal.value || 0;
            let pointamnts = parseFloat(pointamnt);
            if (isNaN(pointamnts)) {
                pointamnts = 0;
            }
            let poitformat = pointamnts.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
            document.getElementById('vpoint_amnt').innerHTML = poitformat;
        }
        
        function sdpointsfield(x) {
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
            
            var adload_point = document.getElementById('spadload_point');
            adload_point.addEventListener("keydown", function(e) {
                if (invalidChars.includes(e.key)) {
                    e.preventDefault();
                }
            });
        }
        
        
        $('#spadpointsForm').on('submit', function(e) {
            e.preventDefault();
            var transtype   = document.getElementById("adtransaction").value;
            var accountid   = document.getElementById("adwithdrawaccount").value;
            var load_point   = document.getElementById("spadload_point").value;
            var walletpoints   = document.getElementById("adwalletpoints").value;
            var outbutton = document.getElementById('adoutbtn');
            
            if (transtype && transtype.trim() !== "" && accountid && accountid.trim() !== "" && load_point && load_point.trim() !== "" && walletpoints && walletpoints.trim() !== "") {
                load_point = parseFloat(load_point)
                balances = parseFloat(walletpoints)
                let selectedValues = accountid.split(' | ');
                let userid = selectedValues[0];
                let isNumber = /^\d+(\.\d+)?$/.test(load_point); 
                if (isNumber) {
                    if (balances>0 && balances >= load_point) {
                        if (load_point!="" && load_point > 0) {
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
                                    $.ajax({
                                        method: 'POST',
                                        url:'spadminloading',
                                        data:{userid:userid, load_point:load_point, transtype:transtype},
                                        success: function(res) {
                                            outbutton.disabled = false;
                                            $(".loadspinner").hide();
                                            if (res.data === 'success') {
                                                toastr["success"]("Successfully sent!");
                                                
                                                document.getElementById('adtransaction').value="";
                                                $('#adwithdrawaccount')[0].selectize.clear();
                                                document.getElementById('spadload_point').value="";
                                                $("#import_raw_table").load('import_spadload');
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        