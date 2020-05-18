/***
script for box project
netvaast 2018
***/
var updateInterval = 6000;
var maxTemperature = 20;
var maxDepot = 4;

function checkTemperature(i, temperature){
    /* 
    fonction qui affiche une icone rouge
    ou verte selon la tematarature.
    Voir la var maxTemperature
    */
    let iconeTemp = $("#icone" + i + "-temp");
    let lastTemp = $("#last" + i + "-temp");
    let message = ""
    
    if (Number(temperature) > maxTemperature) {
        message = "<i class='fas fa-thermometer-full rouge'></i>"
    }
    else{
       message = "<i class='fas fa-thermometer-quarter vert'></i>"         
    }
    iconeTemp.html(message);
    lastTemp.html(temperature);
}

function checkDepot(i, nbrDepot){
    /* 
    fonction qui affiche une icone rouge
    ou verte selon la tematarature.
    Voir la var maxTemperature
    */
    let iconeDepot = $("#icone" + i + "-deposit-count");
    let depotBox = $("#box" + i + "-deposit-count");
    let message = ""
    
    if (Number(nbrDepot) > maxDepot) {
        message = "<i class='fas fa-vials rouge'></i>"
    }
    else{
       message = "<i class='fas fa-vials vert'></i>"         
    }
    iconeDepot.html(message);
    depotBox.html(nbrDepot);
}

function manageDoors(i, topDoorStatus, frontDoorStatus){
    /* 
    fonction qui affiche une icone rouge
    ou verte selon l'état d'ouverture des portes.
    */
    let iconeFrontDoor = $("#icone" + i + "-front-door");
    let iconeTopDoor = $("#icone" + i + "-top-door");
    let boxTopStatus = $("#box" + i + "-top-status");
    let boxDoorStatus = $("#box" + i + "-door-status");
    
    if (frontDoorStatus == 'OPEN') {
        //console.log("frontDoorStatus == 'OPEN'");
        iconeFrontDoor.html("<img src='++theme++mitsibox/images/box_door_front_open.png' alt='porte frontale' />")
    }
    else{
       iconeFrontDoor.html("<img src='++theme++mitsibox/images/box_door_front_close.png' alt='porte frontale' />")
    }

    if (topDoorStatus == 'OPEN') {
        iconeTopDoor.html("<img src='++theme++mitsibox/images/box_door_top_open.png' alt='porte supérieure' />")
    }
    else{
       iconeTopDoor.html("<img src='++theme++mitsibox/images/box_door_top_close.png' alt='porte supérieure' />")
    }
    boxTopStatus.html(topDoorStatus);
    boxDoorStatus.html(frontDoorStatus);    
}

function displayBox(i, numBox, data){
    /*
    fonction qui affiche toutes les infos d'une boite
    Les identifiants sont construits dynamiquement
    Appel des fonction pour la gestions des icones
    thermomètre et portes
    */
    let boxLabId = $(numBox + '-lab-id');
    let boxName = $(numBox + '-name');
    let boxDepositCount = $(numBox + '-deposit-count');
    let boxLastHumidity = $(numBox + '-last-humidity');
    let boxAddress = $(numBox + '-address');
    let boxLat = $(numBox + '-lat');
    let boxLong = $(numBox + '-long');
    let boxTopStatus = $(numBox + '-top-status');
    let boxDoorStatus = $(numBox + '-door-status');
    let boxFirstDeposit = $(numBox + '-first-deposit');
    let boxLastDeposit = $(numBox + '-last-deposit');
    let boxLastRelief = $(numBox + '-last-relief');
    let boxLastUpdate = $(numBox + '-last-update');
    
    boxName.text(data.name);
    boxLastHumidity.text(data.last_humidity);
    boxAddress.text(data.address);
    boxLat.text(data.lat);             
    boxLong.text(data.long);                
    boxFirstDeposit.text(data.first_deposit);
    boxLastDeposit.text(data.last_deposit);
    boxLastRelief.text(data.last_relief);
    boxLastUpdate.text(data.last_update);
    boxLabId.text(data.lab_id);
    
    checkTemperature(i, data.last_temp);
    checkDepot(i, data.deposit_count);
    manageDoors(i, data.top_status, data.door_status);
}

function getBox() {
    $.ajax({
        url: "getJsonBox",
        type:'GET',
        dataType: 'json',
        success: 
            function(data){
                jQuery.each(data, function(i, val) {
                    //console.log(val);
                    let numBox = '#box' + i;
                    displayBox(i, numBox, val);
                });
                setTimeout(function(){getBox()}, updateInterval);
            },
        error: 
            function(xhr, status, error, textStatus, errorThrown) {
                let errorMessage = xhr.status + ': ' + xhr.textStatus + ' ' + xhr.statusText + ' ' + errorThrown;
                alert('Error - ' + errorMessage);
            }
    })
}
getBox();


