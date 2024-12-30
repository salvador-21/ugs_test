




// $(document).on('click','.loadingtrans',function(){
//     $('#cashoutnowmodal').modal('show')
// })
// $(document).on('change', '.transactype', function() {
//     var transacval = $(this).val();
//     $.ajax({
//         method: 'POST',
//         url: 'pointsTransaction',
//         data: {
//             transacval: transacval,
//             csrfmiddlewaretoken: '{{ csrf_token }}'
//         },
//         success: function(res) {
//             $("#mptranstype").html(res); 
//             $("#processbtn").html(transacval); 
//         }
//     });
// });





// $(document).on('change','.withdrawaccount',function(){
//     var withdrawacnt = $(this).val();
//     var transtype = document.getElementById('actiontype').value
//     let selectedValues = withdrawacnt.split(' | ');
//     let userid = selectedValues[0];
//     let username = selectedValues[1];
    
//     $.ajax({
//         method: 'POST',
//         url: 'withdrawal_accnt',
//         data: {
//             withdrawacnt: userid,
//             transtype: transtype,
//             csrfmiddlewaretoken: '{{ csrf_token }}'
//         },
//         success: function(res) {
//             let formattedWalletBal = parseFloat(res.walletbal).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
//             document.getElementById('wallet_bal').innerHTML = formattedWalletBal;
//             document.getElementById('walletpoints').value = res.walletbal;
//             if(username){
//                 document.getElementById('selectedusr').innerHTML=username;
//             }  
//         }
//     });
// })



// $('#pointsForm').on('submit', function(e) {
//     e.preventDefault();
//     var transtype   = document.getElementById("transaction").value;
//     var accountid   = document.getElementById("withdrawaccount").value;
//     var load_point   = document.getElementById("load_point").value;
//     var walletpoints   = document.getElementById("walletpoints").value;
//     var outbutton = document.getElementById('outbtn');
    
//     if (transtype && transtype.trim() !== "" && accountid && accountid.trim() !== "" && load_point && load_point.trim() !== "" && walletpoints && walletpoints.trim() !== "") {
//         load_point = parseFloat(load_point)
//         balances = parseFloat(walletpoints)
//         let selectedValues = accountid.split(' | ');
//         let userid = selectedValues[0];
//         let isNumber = /^\d+(\.\d+)?$/.test(load_point); 
//         if (isNumber) {
//             if (balances>0 && balances >= load_point) {
//                 if (load_point!="" && load_point > 0) {
//                     Swal.fire({
//                         title: "Are you sure?",
//                         text: "you want to " + transtype + " points now?",
//                         icon: "question",
//                         showCancelButton: true,
//                         confirmButtonColor: "#3085d6",
//                         cancelButtonColor: "#d33",
//                         confirmButtonText: transtype
//                     }).then((result) => {
//                         if (result.isConfirmed) {
//                             outbutton.disabled = true;
//                             $(".addrowspin").show();
//                             let randomDelay = Math.floor(Math.random() * 2000) + 1000;
//                             // console.log('Delay:', randomDelay, 'milliseconds');
//                             setTimeout(function() {
//                                 $.ajax({
//                                     method: 'POST',
//                                     url:'points_transactions',
//                                     data:{userid:userid, load_point:load_point, transtype:transtype},
//                                     success: function(res) {
//                                         outbutton.disabled = false;
//                                         $(".addrowspin").hide();
//                                         if (res.data === 'success') {
//                                             toastr["success"]("Cashout request successfully sent!");
//                                             document.getElementById('transaction').value="";
//                                             $('#withdrawaccount')[0].selectize.clear();
//                                             document.getElementById('load_point').value="";
//                                             document.getElementById('walletbal').innerHTML=res.newPoints;
//                                             $('#cashoutnowmodal').modal('hide')
//                                             $("#import_raw_table").load('load_points_table');
//                                         }else if (res.data === 'error') {
//                                             toastr["error"]("Error processing request!");
//                                         }else if (res.data === 'insufficient') {
//                                             toastr["error"]("Insufficient Points Balance!");   
//                                         }else if (res.data === 'tryagain') {
//                                             toastr["error"]("Please try again after a few seconds.");  
//                                         }else{
//                                             toastr["error"]("Invalid inputs!");   
//                                         } 
//                                     }
//                                 });
//                             }, randomDelay);
//                         }
//                     });
//                 }else{
//                     toastr["error"]("Invalid inputs!");   
//                 }
//             }else{
//                 toastr["error"]("Insufficient Points Balance!");    
//             }
//         } else {
//             toastr["error"]("Invalid inputs!");  
//         }
//     }else{
//         toastr["error"]("All fields are required!");   
//     }
// });

