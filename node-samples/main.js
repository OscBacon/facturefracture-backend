const { sendMoney } = require('./build/src/requestMoney');

//var people = ["Banana", "Orange", "Apple", "Mango"];
var info = JSON.parse('{"split-by":"total","participants":["cheryl@beta.inter.ac", "roya@beta.inter.ac", "oscar@beta.inter.ac"],"unassigned":{"total":60.00},"unpaid":{"roya":20.00,"cheryl":20.00},"paid":{"oscar":20.00},"total":60.00,"dinner-daddy":"roya","final":true}');

var people = info.participants;
var total = 100;
var part = total/people.length;
var i;
// Loop through each of the people in the list of tuples passed in
for (i = 0 ; i < people.length; i++){
    sendMoney(part, people[i], 'Pls send monies');
    // Need to enter the amount for the request, email, optional note (default to be blank??)
}
console.log(part);
//}




//const { sendMoney } = require('./build/src/requestMoney');

//var people = ["Banana", "Orange", "Apple", "Mango"];
// Loop through each of the people in the list of tuples passed in
//for (let  i = 0 ; i < people.length; i++){
//  sendMoney(100, 'cheryl@beta.inter.ac');
    // Need to enter the amount for the request, email, optional note (default to be blank??)

//}
