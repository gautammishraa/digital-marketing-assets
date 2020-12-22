function onOpen() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var menubuttons = [ 
      {name: "Send changes to FB", functionName: "sendChanges"}
    ];
    ss.addMenu("Magic", menubuttons);
}

function sendChanges() {
  var sheet = SpreadsheetApp.getActive().getSheetByName('Dashboard');
  var changes = sheet.getRange('P5:P100').getValues();
  var res;
  for (var i = 0; i < changes.length; i++){
    if (changes[i][0].indexOf("http")>-1) {
      res = UrlFetchApp.fetch(changes[i][0], {'method': 'post'});
      sheet.getRange('Q' + String(i+5)).setValue(res.getContentText());  // set change log
    }
  } 
}
