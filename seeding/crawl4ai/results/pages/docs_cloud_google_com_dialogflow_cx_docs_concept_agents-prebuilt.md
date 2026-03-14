Some products and features are in the process of being renamed. Generative playbook and flow features are also being migrated to a single consolidated console. See [the details](https://docs.cloud.google.com/dialogflow/cx/docs#consolidation). 


Send feedback 
#  Prebuilt agents Stay organized with collections  Save and categorize content based on your preferences.
  * On this page
  * [Import a prebuilt agent](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#import)
  * [Customize the imported prebuilt agent](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#customize)
  * [Modifying webhook code](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#modify-webhook)
  * [Financial services agent](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#financial-services)
    * [Sample utterances](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#sample_utterances)
  * [Healthcare agent](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#healthcare)
    * [Sample utterances](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#sample_utterances_2)
  * [Order and account management agent](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#order-account-management)
    * [Sample utterances](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#sample_utterances_3)
  * [Payment arrangement agent](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#payment-arrangement)
    * [Sample utterances](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#sample_utterances_4)
  * [Small talk agent](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#small-talk)
    * [Sample utterances](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#sample_utterances_5)
  * [Telecommunications agent](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#telecommunications)
    * [Sample utterances](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#sample_utterances_6)
  * [Travel: baggage claim agent](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#travel-baggage-claim)
    * [Sample utterances](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#sample_utterances_7)
  * [Travel: car rental agent](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#travel-car-rental)
    * [Sample utterances](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#sample_utterances_8)
  * [Travel: flight information agent](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#travel-flight-information)
    * [Sample utterances](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#sample_utterances_9)


Prebuilt agents are a collection of agents provided by Dialogflow CX for common use cases. These agents can be used to establish a base for building conversations. In Dialogflow CX, you will find popular use cases across industries, such as telecommunications, financial services, healthcare, retail, and travel. [Generative prebuilt agents](https://docs.cloud.google.com/dialogflow/cx/docs/concept/generative/prebuilt-agent) are also available with limited access, demonstrating common use cases implemented using [generative features](https://docs.cloud.google.com/dialogflow/cx/docs/concept/generative).
Prebuilt agents include [intents](https://docs.cloud.google.com/dialogflow/cx/docs/concept/intent) and [entities](https://docs.cloud.google.com/dialogflow/cx/docs/concept/entity) for their use cases, but you need to modify the example [route groups](https://docs.cloud.google.com/dialogflow/cx/docs/concept/handler#route-group) and [fulfillment](https://docs.cloud.google.com/dialogflow/cx/docs/concept/fulfillment) (where applicable).
## Limitations
The following limitations apply:
  * Prebuilt agents currently only support English (en).


## Import a prebuilt agent
To import a prebuilt agent to your project:
  1. Go to the [Dialogflow CX console](https://dialogflow.cloud.google.com/cx/projects).
  2. Click the project where you would like to import the prebuilt agent.
  3. Click **Use pre-built agents**.
  4. Click the agent of interest and click **Import**.
  5. Choose your desired [location](https://docs.cloud.google.com/dialogflow/cx/docs/concept/region#avail) and click **Create**.
  6. Start testing and customizing.


## Customize the imported prebuilt agent
  1. [Test the agent](https://docs.cloud.google.com/dialogflow/cx/docs/concept/console#simulator) using the simulator to understand what it can help users accomplish.
  2. Click the **Manage** tab in the left pane and then **Test Cases** to see coverage and example scripts. For more information, see the [Test cases](https://docs.cloud.google.com/dialogflow/cx/docs/concept/test-case) documentation.
  3. [Delete any flows](https://docs.cloud.google.com/dialogflow/cx/docs/concept/flow#delete) that are irrelevant to your use case.
  4. Edit agent dialogue and [custom entities](https://docs.cloud.google.com/dialogflow/cx/docs/concept/entity-custom) to meet your business needs.
  5. If there is [webhook source code](https://docs.cloud.google.com/dialogflow/cx/docs/concept/webhook), see [Modifying webhook code](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agents-prebuilt#modify-webhook).


## Modifying webhook code
A selection of the prebuilt agents utilize webhooks. The original webhook source code uses Node.js and is hosted in Google's internal Cloud Functions project.
To use and modify this code in your own Cloud Functions project, please follow the subsequent directions:
  1. Go to the [Dialogflow CX console](https://dialogflow.cloud.google.com/cx/projects).
  2. Click the project where you would like to import the prebuilt agent.
  3. Click **Use pre-built agents**.
  4. Click the agent of interest then click **Documentation link** , which will bring you to the relevant pre-built agent section of this document.
  5. See the **Webhook** subsection for the prebuilt agent and copy the source code.
  6. Go to the [Google Cloud console](https://console.cloud.google.com/) and select **Cloud Functions** on the left panel.
  7. Click the project where you would like to import the source code.
  8. Click **Create Function**. For further instructions, take a look at the [Create a Cloud Function](https://docs.cloud.google.com/functions/docs/create-deploy-nodejs#create_a_function) documentation.
  9. Under the **Source code** section, select **Inline Editor** and paste the copied source code.
  10. Click **Source** and then **Edit** to change the logic based on your business rules. Once finished, click **Deploy**.
  11. Click **Trigger** and copy the **Trigger URL**.
  12. Replace that Trigger URL in your agent by going to **Manage > Webhooks** and selecting the webhook to paste the new URL into. Paste the Trigger URL into the field labeled Webhook URL. Click **Save**.
  13. Using the [Webhooks](https://docs.cloud.google.com/dialogflow/cx/docs/concept/webhook) documentation, test your fulfillment.


## Financial services agent
This template helps end-users with their cards, checks an application status, and investigates suspicious charges.
### Sample utterances
  * _I'd like to make a payment towards my balance._
  * _I lost my card and need a new one._
  * _I want to report some suspicious activity on my checking account._
  * _What is my auto loan application status?_
  * _What are the different annual fees on your business credit cards?_


### Webhook
The Cloud Functions webhook performs the following actions:
  * Validates an end-user's identity
  * Provides sample balances, loan status, and credit card feature information
  * Mocks sample payments, including validating payment amounts and dates
  * Controls opening hours


package.json ```
{
  "name": "sample-http",
  "version": "0.0.1"
}
    
```

index.js ```
/**
 * Responds to any HTTP request.
 *
 * @param {!express:Request} req HTTP request context.
 * @param {!express:Response} res HTTP response context.
 */
exports.cxPrebuiltAgentsFinServ=(req,res)=>{
console.log('Cloud Function:','Invoked cloud function from Dialogflow CX');
lettag=req.body.fulfillmentInfo.tag;

if(!!tag){
switch(tag){
//BEGINvalidateAccount
case'validateAccount':
console.log(tag+' was triggered.');
letcard_last_four=req.body.sessionInfo.parameters.card_last_four;

letcard_verified;
//cardvalidationonlyfailsifcardnumberis0000
if(card_last_four=='0000'){
card_verified='false';
}else{
card_verified='true';
}

res.status(200).send(
{sessionInfo:{parameters:{card_verified:card_verified}}});

console.log(' verified: '+card_verified);
break;

//BEGINgetAccountInfo
case'getAccountInfo':
console.log(tag+' was triggered.');
letcurrent_balance;
letlast_statement_balance;
letminimum_due;

//Randomcurrentbalancebetween1and1000
current_balance=Math.floor(Math.random()*1000);

//Laststatementbalanceis70%ofcurrentbalance
last_statement_balance=Math.floor(current_balance*0.7);

//Minimumdueis25%oflaststatementbalance
minimum_due=Math.floor(last_statement_balance*0.25);

res.status(200).send({
sessionInfo:{
parameters:{
current_balance:current_balance,
last_statement_balance:last_statement_balance,
minimum_due:minimum_due
}
}
});

console.log(
'current balance: '+current_balance+
' last statement balance: '+last_statement_balance);
break;

//BEGINgetPaymentSource
case'getPaymentSource':
console.log(tag+' was triggered.');

//staticarrayofaccountnames
letaccount_names=
['National Checking Account', 'My Checking', 'Personal Checking'];

//randomarrayvalueforaccountnames
letaccount_index=Math.floor(Math.random()*account_names.length);
letselected_account=account_names[account_index];

res.status(200).send(
{sessionInfo:{parameters:{selected_account:selected_account}}});

console.log(' selected account: '+selected_account);
break;

//BEGINsubmitPayment
case'submitPayment':
console.log(tag+' was triggered.');

letcard_digits=
String(req.body.sessionInfo.parameters.card_last_four);

letpayment_status;
//Whenfirstdigitofcard_digitsis9thetransactionfails
if(card_digits[0]=='9'){
payment_status='fail';
}else{
payment_status='success';
}

res.status(200).send(
{sessionInfo:{parameters:{payment_status:payment_status}}});

console.log(' verified: '+card_verified);
break;

//BEGINvalidatePaymentAmount
case'validatePaymentAmount':
console.log(tag+' was triggered.');

//getpaymentamount
letpayment_amount=
Number(req.body.sessionInfo.parameters.other_amount);
letcurrent_balance_temp=
req.body.sessionInfo.parameters.current_balance;
letamount_valid;

payment_amount=Number(payment_amount);

console.log(
`payment_amount:`+payment_amount+`currentbalance:`+
current_balance_temp);

//confirmpaymentamountisapositivevaluelessthanorequaltothe
//currentbalance
if(payment_amount0){
if(payment_amount<=current_balance_temp){
amount_valid=true;
}else{
amount_valid=false;
}
}else{
amount_valid=false;
}

res.status(200).send(
{sessionInfo:{parameters:{amount_valid:amount_valid}}});

console.log('payment status: '+payment_status);
break;

//BEGINvalidatePaymentDate
case'validatePaymentDate':
console.log(tag+' was triggered.');

//getpaymentdate
letpayment_date_raw=req.body.sessionInfo.parameters.payment_date;

//setpaymentdateindateobjectformat.subtractonefrommonth
//becausemonthisindexedto0.
letpayment_year=payment_date_raw.year;
letpayment_month=payment_date_raw.month-1;
letpayment_day=payment_date_raw.day;

console.log(
'Payment - Year: '+payment_year+' Month '+payment_month+
' Day: '+payment_day);

//settoday's date
        let today = new Date();

        let this_year = today.getFullYear();
        let this_month = today.getMonth();
        let this_day = today.getDate();

        console.log(
Today-Year:' + this_year + 'Month' + this_month +
Day:' + this_day);

        let payment_date_valid;

        // check if the payment date is after today
        if (payment_year > this_year) {
          payment_date_valid = true;
          console.log('Futureyear');
        } else if (payment_year == this_year && payment_month > this_month) {
          payment_date_valid = true;
          console.log('Futuremonth');
        } else if (
            payment_year == this_year && payment_month == this_month &&
            payment_day >= this_day) {
          payment_date_valid = true;
          console.log('Todayorlaterthismonth');
        } else {
          payment_date_valid = false;



        res.status(200).send({
          sessionInfo: {parameters: {payment_date_valid: payment_date_valid}}
        });

        console.log('paymentdatevalid:' + payment_date_valid);
        break;

      // BEGIN checkInHours
      case 'checkInHours':
        console.log(tag + 'wastriggered.');

        // check if we are currently in hours
        let currentDate = new Date();
        console.log('currenttimeis' + currentDate);

        let currentHour = currentDate.getHours();
        console.log('currenthouris' + currentHour);
        if (currentHour >= 8 && currentHour <= 20) {
          in_hours = 'true';
          console.log('currentlyinhours');
        } else {
          in_hours = 'false';
          console.log('currentlyoutofhours');


        res.status(200).send({sessionInfo: {parameters: {in_hours: in_hours}}});
        break;

      // BEGIN getRetryCount
      case 'getRetryCount':
        console.log(tag + 'wastriggered.');

        // increment the current retry counter
        let retry_count = req.body.sessionInfo.parameters.retry_count;
        retry_count = retry_count + 1;

        res.status(200).send(
            {sessionInfo: {parameters: {retry_count: retry_count}}});
        break;

      // BEGIN getLoanStatus
      case 'getLoanStatus':
        console.log(tag + 'wastriggered.');

        let loan_reference =
            String(req.body.sessionInfo.parameters.loan_reference);
        let loan_type = loan_reference[0];
        let loan_status = loan_reference[1];
        let loan_found = 'true';

        console.log('loanrefis' + loan_reference);
        console.log('typeis' + loan_type);
        console.log('statusis' + loan_status);

        // mock loan not found
        if (loan_reference[0] == '0') {
          loan_found = 'false';


        // mock loan found
        if ((loan_type != 'auto') && (loan_type != 'home')) {
          if (loan_reference[0] > '5') {
            loan_type = 'home';
          } else {
            loan_type = 'auto';



        res.status(200).send({
          sessionInfo: {
            parameters: {
              loan_type: loan_type,
              loan_status: loan_status,
              loan_found: loan_found


        });
        break;

      // BEGIN validateTransactionDate
      case 'validateTransactionDate':
        console.log(tag + 'wastriggered.');

        // get date queried
        let date_queried_raw = req.body.sessionInfo.parameters.date_queried;

        // set date queried in date object format. subtract one from month
        // because month is indexed to 0.
        date_queried = new Date(
            date_queried_raw.year, date_queried_raw.month - 1,
            date_queried_raw.day);

        console.log(date_queried + 'isthedateimlookingfor.');

        let date_valid;
        let date_now = new Date();

        // check if the payment date is after today
        if (date_queried > date_now) {
          date_valid = 'false';
        } else {
          date_valid = 'true';


        res.status(200).send(
            {sessionInfo: {parameters: {date_valid: date_valid}}});
        break;

      // BEGIN lookupTransactions
      case 'lookupTransactions':
        console.log(tag + 'wastriggered.');

        // select a random retailer from the retailers array
        let retailers = [
Dior', 'Walmart', 'Target', 'Costco', 'Macy\'s','Bed Bath & Beyond',
'Amazon','Walgreens','Home Depot','Best Buy','Kohl\'s'

        let randomRetail = Math.floor(Math.random() * retailers.length);
        console.log('randomretailvalue' + randomRetail);

        let retailer_queried = retailers[randomRetail];

        // Alter the transaction amount
        let amount_queried =
            Number(req.body.sessionInfo.parameters.amount_queried.amount);
        let transaction_value = Number(amount_queried);
        let randomAdjust = Math.floor(Math.random() * 5);
        randomAdjust = Number(randomAdjust / 100);
        let adjustment = Number(amount_queried * randomAdjust);

        let randomMath = Math.floor(Math.random() * 1);
        if (randomMath < 1) {
          transaction_value = Number(transaction_value - adjustment).toFixed(2);
        } else if (randomMath = 1) {
          transaction_value = Number(transaction_value + adjustment).toFixed(2);


        if (amount_queried < 1000) {
          transaction_found = 'true';
        } else {
          transaction_found = 'false';


        res.status(200).send({
          sessionInfo: {
            parameters: {
              retailer_queried: retailer_queried,
              transaction_value: transaction_value,
              transaction_found: transaction_found


        });

        break;

      // BEGIN lookupCardFeatures
      case 'lookupCardFeatures':
        console.log(tag + 'wastriggered.');

        // setup arrays for card features
        let interestRate = [
14.5%APR',
0%APRinyear1andthenincreasesto25%APRinyear2',
10%APRinyear1andthenincreasesto20%APRinyear2', '18%APR'

        let annualFee = [
$0annualfeeforyear1andthenincreasesto$90inyear2',
$70annualfeestartinginyear1',
$15annualfeeforyear1andthenincreasesto$80inyear2',
$50annualfeestartinginyear1'

        let cashBackRate = ['1%', '3%', '6%', '2%', '5%', '4%'];
        let pointsBonus = ['50,000', '25,000', '10,000', '100,000', '75,000'];

        // setup card one features
        let cardOneRandomInterest =
            Math.floor(Math.random() * interestRate.length);
        let card_one_interest = interestRate[cardOneRandomInterest];
        let cardOneRandomFee = Math.floor(Math.random() * annualFee.length);
        let card_one_fee = annualFee[cardOneRandomFee];
        let cardOneRandomCashback =
            Math.floor(Math.random() * cashBackRate.length);
        let card_one_cashback = cashBackRate[cardOneRandomCashback];
        let cardOneRandomPoints =
            Math.floor(Math.random() * pointsBonus.length);
        let card_one_points = pointsBonus[cardOneRandomPoints];

        // setup card two features
        let cardTwoRandomInterest =
            Math.floor(Math.random() * interestRate.length);
        let card_two_interest = interestRate[cardTwoRandomInterest];
        let cardTwoRandomFee = Math.floor(Math.random() * annualFee.length);
        let card_two_fee = annualFee[cardTwoRandomFee];
        let cardTwoRandomCashback =
            Math.floor(Math.random() * cashBackRate.length);
        let card_two_cashback = cashBackRate[cardTwoRandomCashback];
        let cardTwoRandomPoints =
            Math.floor(Math.random() * pointsBonus.length);
        let card_two_points = pointsBonus[cardTwoRandomPoints];

        res.status(200).send({
          sessionInfo: {
            parameters: {
              card_one_interest: card_one_interest,
              card_one_fee: card_one_fee,
              card_one_cashback: card_one_cashback,
              card_one_points: card_one_points,
              card_two_interest: card_two_interest,
              card_two_fee: card_two_fee,
              card_two_cashback: card_two_cashback,
              card_two_points: card_two_points


        });
        break;

      default:
        console.log('defaultcasecalled');
res.status(200).end();
break;
}
}
};

```

## Healthcare agent
This template helps end-users check their claims, benefits, and find a doctor.
### Sample utterances
  * _What is coinsurance?_
  * _Can you help me find a doctor?_
  * _I'm not feeling well._
  * _What is my deductible?_


## Order and account management agent
This template helps end-users purchase or return a product, track orders, and manage account settings, such as loyalty points, addresses, and passwords.
### Sample utterances
  * _I haven't received my order, where is it?_
  * _I want to get a new phone._
  * _I forgot my password._
  * _Can you tell me how many points I have?_
  * _I moved and need to update my address._


## Payment arrangement agent
This template helps end-users set up a two installment payment arrangement or extend a payment due date.
### Sample utterances
  * _My account was suspended._
  * _I won't get paid on time to pay my bill._
  * _I need to extend my due date._
  * _I lost my job due to covid-19._


### Webhook
This Cloud Functions webhook performs the following actions:
  * Provides sample amount due and maximum extension dates.
  * Calculates the second payment installment based on the difference between the total balance and the first payment installment paid.
  * Validates that the requested extension date does not surpass the maximum extension date.


package.json ```
{
  "name": "sample-http",
  "version": "0.0.1",
  "dependencies": {
    "moment": "2.27.0"
  }
}
    
```

index.js ```
constmoment=require('moment');

functiongetRandomAmount(min,max){
returnMath.random()*(max-min)+min;
}

functionformatCurrency(amount){
returnNumber(amount).toFixed(2);
}

functionformatUserDate(dateObject){
if(!dateObject){
console.log('dateObject error. dateObject passed to formatUserDate is:',dateObject);
console.log('dateObject requires day, month, year properties:');
//returnfalseifthedatesarenotvalid
//returningfalsepreventstheif/elseblockfromrunning,whichcausesthefunctiontocrash.
returnfalse;
}
console.log('formatUserDate date set.');
const{day,year,month}=dateObject;
return`${year}-${month}-${day}`;
}

/**
*RespondstoanyHTTPrequest.
*
*@param{!express:Request}reqHTTPrequestcontext.
*@param{!express:Response}resHTTPresponsecontext.
*/

exports.cxPrebuiltAgentsPaymentArrangement=(req,res)=>{

vartag=req.body.fulfillmentInfo.tag;
varfirst_payment;
varamount_due_1;
//varadjust_due_date;
varmax_date_1;
varmaxDate1;
varmax_date_2;
varmaxDate2;
varcurrent_due_date;
varmax_extension_date;
varmaxExtensionDate;
varamount_due;
varpayment_amount_2;
vardateFromUser;
varvalid_payment;
varvalid_date;

if(!!tag){
switch(tag){

//InitializeDynamicparameters
case'setDynamicParams':
console.log(tag+' was triggered.');
max_date_1=moment().add(15,'days').calendar();
max_date_2=moment().add(25,'days').calendar();
current_due_date=moment().add(10,'days').calendar();
max_extension_date=moment().add(30,'days').calendar();
amount_due=formatCurrency(getRandomAmount(200,400));

res.status(200).send({
sessionInfo:{
parameters:{
max_date_1:max_date_1,
max_date_2:max_date_2,
current_due_date:current_due_date,
max_extension_date:max_extension_date,
amount_due:amount_due,
}
}
});
break;

//InitializeStaticparameters
case'setStaticParams':
console.log(tag+' was triggered.');
user_id=req.body.sessionInfo.parameters.user_id;
if(user_id=='1001'){
max_date_1="2021-01-15";
max_date_2="2021-01-30";
current_due_date="2021-01-01";
max_extension_date="2021-02-15";
amount_due='225.00';
}elseif(user_id=='2002'){
max_date_1="2021-03-15";
max_date_2="2021-03-30";
current_due_date="2021-03-01";
max_extension_date="2021-04-15";
amount_due='333.00';
}elseif(user_id=='3003'){
max_date_1="2021-05-15";
max_date_2="2021-05-30";
current_due_date="2021-05-01";
max_extension_date="2021-06-15";
amount_due='189.00';
}else{
max_date_1=moment().add(15,'days').calendar();
max_date_2=moment().add(25,'days').calendar();
current_due_date=moment().add(10,'days').calendar();
max_extension_date=moment().add(30,'days').calendar();
amount_due=formatCurrency(getRandomAmount(200,400));
}
res.status(200).send({
sessionInfo:{
parameters:{
max_date_1:max_date_1,
max_date_2:max_date_2,
current_due_date:current_due_date,
max_extension_date:max_extension_date,
amount_due:formatCurrency(amount_due),
}
}
});
break;

//Automaticallysetsecondpaymentbasedonfirstpaymentamount
case'secondPayment':
console.log(tag+' was triggered.');
first_payment=req.body.sessionInfo.parameters.payment_amount_1.amount;
amount_due_1=req.body.sessionInfo.parameters.amount_due;
payment_amount_2=formatCurrency(amount_due_1-formatCurrency(first_payment));

res.status(200).send({
sessionInfo:{
parameters:{
payment_amount_2:payment_amount_2
}
}
});
break;

//BEGINvalidatePayment
case'validatePayment':
console.log(tag+' was triggered.');
first_payment=req.body.sessionInfo.parameters.payment_amount_1.amount;
amount_due_1=req.body.sessionInfo.parameters.amount_due;
if((formatCurrency(first_payment)>='100.00')(formatCurrency(first_payment)amount_due_1)){
valid_payment="True";
}else{
valid_payment="False"
}
res.status(200).send({
sessionInfo:{
parameters:{
valid_payment:valid_payment,
}
}
});
break;

//BEGINvalidateDate
case'validateDate':
//LogwhenthecloudfunctionforthevalidateDatetagistriggered
console.log(tag+' was triggered.');

//LogALLofthesessionparameterspassedtothecloudfunction
console.log('validateDate sessionInfo parameters',req.body.sessionInfo.parameters);

//LogONLYmax_extension_dateandadjust_due_datevaluesfromsessionparameters.
console.log('sessionInfo >>> max_extension_date',req.body.sessionInfo.parameters.max_extension_date);
console.log('sessionInfo >>> adjust_due_date',req.body.sessionInfo.parameters.adjust_due_date);

//IftheformatUserDatefunctionsucceedsrunning,thenthedatewillbeastringformattedasyyyy-mm-dd.
//IfthesessionparamsdateObjectisnotformattedcorrectlytheformatUserDatefunctionreturnsthebooleanvaluefalse.
//formatUserDatereturnsfalsetopreventtheMomentfunctionfromrunning(see3conditionsbelow).
dateFromUser=formatUserDate(req.body.sessionInfo.parameters.adjust_due_date);
maxExtensionDate=req.body.sessionInfo.parameters.max_extension_date;

//Setvalid_datetofalse.WedothissothecloudfunctiondoesnotcrashandalwaysreturnsavaluetoDialogflowCX
valid_date="False"

//Onlysetvalid_datetotruewhen
//1)dateFromUserisadatestringandnotsettofalsebytheformatUserDatefunction
//2)maxExtensionDateisstringandnotsettofalsebytheformatUserDatefunction
//3)ifMomentdeterminesthedateFromUserisbeforemaxExtensionDate

if(dateFromUsermaxExtensionDatemoment(dateFromUser).isSameOrBefore(maxExtensionDate)){
valid_date="True";
}

res.status(200).send({
sessionInfo:{
parameters:{
valid_date:valid_date,
//YouwillseethedebugpropertyintheDialogflowCXUI
//ifformatUserDatefailedforeitehrdateyouwill
//see'false'intheUI.
//Otherwise,youwillseethestringformatteddate
debug:{dateFromUser,maxExtensionDate}
}
}
});
break;

case'validateDate1':
//LogwhenthecloudfunctionforthevalidateDatetagistriggered
console.log(tag+' was triggered.');

//LogALLofthesessionparameterspassedtothecloudfunction
console.log('validateDate sessionInfo parameters',req.body.sessionInfo.parameters);

//LogONLYmax_date_1andpayment_date_1valuesfromsessionparameters.
console.log('sessionInfo >>> max_date_1',req.body.sessionInfo.parameters.max_date_1);
console.log('sessionInfo >>> payment_date_1',req.body.sessionInfo.parameters.payment_date_1);

//IftheformatUserDatefunctionsucceedsrunning,thenthedatewillbeastringformattedasyyyy-mm-dd.
//IfthesessionparamsdateObjectisnotfomattedcorrectlytheformatUserDatefunctionreturnsthebooleanvaluefalse.
//formatUserDatereturnsfalsetopreventtheMomentfunctionfromrunning(see3conditionsbelow).
dateFromUser=formatUserDate(req.body.sessionInfo.parameters.payment_date_1);
//maxExtensionDate=formatUserDate(req.body.sessionInfo.parameters.max_extension_date);
maxDate1=req.body.sessionInfo.parameters.max_date_1;

//Setvalid_datetofalse.WedothissothecloudfunctiondoesnotcrashandalwaysreturnsavaluetoDialogflowCX
valid_date="False"

//Onlysetvalid_datetotruewhen
//1)dateFromUserisadatestringandnotsettofalsebytheformatUserDatefunction
//2)maxExtensionDateisstringandnotsettofalsebytheformatUserDatefunction
//3)ifMomentdeterminesthedateFromUserisbeforemaxExtensionDate

if(dateFromUsermaxDate1moment(dateFromUser).isSameOrBefore(maxDate1)){
valid_date="True";
}

res.status(200).send({
sessionInfo:{
parameters:{
valid_date:valid_date,
//YouwillseethedebugpropertyintheDialogflowCXUI
//ifformatUserDatefailedforeitehrdateyouwill
//see'false'intheUI.
//Otherwise,youwillseethestringformatteddate
debug:{dateFromUser,maxDate1}
}
}
});
break;

case'validateDate2':
//LogwhenthecloudfunctionforthevalidateDatetagistriggered
console.log(tag+' was triggered.');

//LogALLofthesessionparameterspassedtothecloudfunction
console.log('validateDate sessionInfo parameters',req.body.sessionInfo.parameters);

//LogONLYmax_date_2andpayment_date_2valuesfromsessionparameters.
console.log('sessionInfo >>> max_extension_date',req.body.sessionInfo.parameters.max_date_2);
console.log('sessionInfo >>> adjust_due_date',req.body.sessionInfo.parameters.payment_date_2);

//IftheformatUserDatefunctionsucceedsrunning,thenthedatewillbeastringformattedasyyyy-mm-dd.
//IfthesessionparamsdateObjectisnotfomattedcorrectlytheformatUserDatefunctionreturnsthebooleanvaluefalse.
//formatUserDatereturnsfalsetopreventtheMomentfunctionfromrunning(see3conditionsbelow).
dateFromUser=formatUserDate(req.body.sessionInfo.parameters.payment_date_2);
//maxExtensionDate=formatUserDate(req.body.sessionInfo.parameters.max_extension_date);
maxDate2=req.body.sessionInfo.parameters.max_date_2;

//Setvalid_datetofalse.WedothissothecloudfunctiondoesnotcrashandalwaysreturnsavaluetoDialogflowCX
valid_date="False"

//Onlysetvalid_datetotruewhen
//1)dateFromUserisadatestringandnotsettofalsebytheformatUserDatefunction
//2)maxExtensionDateisstringandnotsettofalsebytheformatUserDatefunction
//3)ifMomentdeterminesthedateFromUserisbeforemaxExtensionDate

if(dateFromUsermaxDate2moment(dateFromUser).isSameOrBefore(maxDate2)){
valid_date="True";
}

res.status(200).send({
sessionInfo:{
parameters:{
valid_date:valid_date,
//YouwillseethedebugpropertyintheDialogflowCXUI
//ifformatUserDatefailedforeitehrdateyouwill
//see'false'intheUI.
//Otherwise,youwillseethestringformatteddate
debug:{dateFromUser,maxDate2}
}
}
});
break;
default:
break;
}
}
};

```

## Small talk agent
This template helps customize and personalize agents with simple questions.
### Sample utterances
  * _What's up?_
  * _Who are you?_
  * _Today is my birthday._
  * _Sorry._
  * _What do you mean?_


## Telecommunications agent
This template helps end-users resolve billing and plan questions, troubleshoot, and add travel and cruise plans.
### Sample utterances
  * _How can I save money on my bill?_
  * _My texts aren't going through._
  * _How much more will I pay if I upgrade to Plan A?_
  * _I need data coverage for a trip I'm going on to Jamaica._


### Webhook
The Cloud Functions webhook performs the following actions:
  * Compares plan costs based on a trip location and duration
  * Identifies billing anomalies based on an end-user's phone number


package.json ```
{
  "name": "sample-http",
  "version": "0.0.1",
  "dependencies": {
    "moment": "2.24.0"
  }
}
    
```

helpers.js ```
//Getthecurrentmonth,firstdayofcurrentmonthandlastmonthvalues
//basedontoday's date

module.exports={
get_date_details:function(bill_state){
constmonthNames=["January","February","March","April","May","June",
"July","August","September","October","November","December"
];
lettoday=newDate()
letfirst_month_name=monthNames[today.getMonth()]
letfirstDay=newDate(today.getFullYear(),today.getMonth(),1);
letfirst_day_str=first_month_name+' 0'+firstDay.getDate()+', '+firstDay.getFullYear()

letlast_month_name=monthNames[today.getMonth()-1]
letlast_month_first_day_str=last_month_name+' 0'+firstDay.getDate()+', '+firstDay.getFullYear()
letsecond_last_month_name=monthNames[today.getMonth()-2]

if(bill_state.toString()=='current'){
return[first_month_name,first_day_str,last_month_name]
}
else{
return[last_month_name,last_month_first_day_str,second_last_month_name]
}

}
}

```

index.js ```
/**
*RespondstoanyHTTPrequest.
*
*@param{!express:Request}reqHTTPrequestcontext.
*@param{!express:Response}resHTTPresponsecontext.
*/
consthelpers=require('./helpers.js')

exports.cxPrebuiltAgentsTelecom=(req,res)=>{
console.log('Cloud Function:','Invoked cloud function from Dialogflow CX');
lettag=req.body.fulfillmentInfo.tag;

if(!!tag){
switch(tag){
//BEGINdetectCustomerAnomaly
case'detectCustomerAnomaly':
console.log(tag+' was triggered.');
letphone_number=req.body.sessionInfo.parameters.phone_number;
letbill_month=req.body.sessionInfo.parameters.bill_state;
letparameters=req.body.sessionInfo.parameters;
letbill_amount;
letproduct_line;
letanomaly_detect="false"
letpurchase="The Godfather"
letpurchase_amount=9.99
lettotal_bill_amount=64.33
letbill_without_purchase=54.34
letupdated_parameters={}

let[month_name,first_of_month,last_month_name]=helpers.get_date_details(bill_month)
console.log(month_name,first_of_month,last_month_name)

//Gettingthemonthnamebasedonthebillstate-currentorprevious
//Forexample,ifthecurrentmonthisDecember,wegetthevaluesas
//December,December1st,November

//Only999999willhaveanomalydetection
if(phone_number.toString()=='999999'){
anomaly_detect="true"
product_line="phone"
purchase="device protection"
updated_parameters["product_line"]=product_line
updated_parameters["bill_month"]=month_name
updated_parameters["last_month"]=last_month_name
}

//Ifbillhikeamountisgiven-wejustaddittothetotalbill
if('bill_amount'inparameters){
bill_amount=parameters['bill_amount']
purchase_amount=bill_amount['amount']
total_bill_amount=54.34+purchase_amount
}

//Addingtheupdatedsessionparameterstothenewparametersjson
updated_parameters["anomaly_detect"]=anomaly_detect
updated_parameters["purchase"]=purchase
updated_parameters["purchase_amount"]=purchase_amount
updated_parameters["bill_without_purchase"]=bill_without_purchase
updated_parameters["total_bill"]=total_bill_amount
updated_parameters["first_month"]=first_of_month

res.status(200).send({
sessionInfo:{
parameters:updated_parameters
}
});
break;

//BEGINvalidatePhoneLine
case'validatePhoneLine':
console.log(tag+' was triggered.');
letphone=req.body.sessionInfo.parameters.phone_number;
letphone_line_verified;
letline_index;
letdomestic_coverage;
letcovered_lines=
['5555555555','5105105100','1231231234','9999999999'];

//Loopoverthecoveredlinesarray
covered_lines.forEach((line,index)=>{
//Foreachphonelineinthearray,checkifthelast4digitsare
//includedinthestring.whentrue,updatetheline_indexvariable
if(line.includes(phone)){
line_index=index;
console.log('This is the index '+line_index);
}
});

//Only9999willfail;
if(line_index===3){
phone_line_verified='false';
}else{
phone_line_verified='true';
}

//Only1234willhavedomesticcoverage.
if(line_index===2){
domestic_coverage='true';
}else{
domestic_coverage='false';
}

res.status(200).send({
sessionInfo:{
parameters:{
phone_line_verified:phone_line_verified,
domestic_coverage:domestic_coverage
}
}
});
break;

//BEGINcruisePlanCoverage
case'cruisePlanCoverage':
console.log(tag+' was triggered.');

letport=req.body.sessionInfo.parameters.destination;
letport_is_covered;
//Samplelistofcoveredcruiseports.
letcovered_ports=[
'mexico',
'canada',
'anguilla',

];

if(covered_ports.includes(port.toLowerCase())){
port_is_covered='true';
}else{
port_is_covered='false';
}

res.status(200).send(
{sessionInfo:{parameters:{port_is_covered:port_is_covered}}});
break;

//BEGINinternationalCoverage
case'internationalCoverage':
console.log(tag+' was triggered.');
letdestination=req.body.sessionInfo.parameters.destination;
letcoverage;
//Samplelistofcoveredinternationalmonthlydestinations.
letcovered_by_monthly=[
'anguilla',
'australia',
'brazil',
'canada',
'chile',
'england',
'france',
'india',
'japan',
'mexico',
'russia',
'singapore',
];
//Samplelistofcoveredinternationaldailydestinations.
letcovered_by_daily=[
'anguilla','australia','brazil','canada','chile','england',
'france','india','japan','mexico','singapore'
];

if(covered_by_monthly.includes(destination.toLowerCase())
covered_by_daily.includes(destination.toLowerCase())){
coverage='both';
}elseif(
covered_by_monthly.includes(destination.toLowerCase())
!covered_by_daily.includes(destination.toLowerCase())){
coverage='monthly_only';
}elseif(
!covered_by_monthly.includes(destination.toLowerCase())
!covered_by_daily.includes(destination.toLowerCase())){
coverage='neither';
}else{
//Thisshouldneverhappen,becausecovered_by_dailyisasubsetof
//covered_by_monthly
coverage='daily_only';
}

res.status(200).send({sessionInfo:{parameters:{coverage:coverage}}});
break;

//BEGINcheapestPlan
case'cheapestPlan':
console.log(tag+' was triggered.');
lettrip_duration=req.body.sessionInfo.parameters.trip_duration;
letmonthly_cost;
letdaily_cost;
letsuggested_plan;

//Canonlysuggestcheapestifbotharevalidforlocation.

//Whentripislongerthan30days,calculateper-monthcost(example$
//amounts).Suggestmonthlyplan.
if(trip_duration30){
monthly_cost=(Math.floor(trip_duration/30))*70;
daily_cost=trip_duration*10;
suggested_plan='monthly';
}
//Whentripis<=30days,butgreaterthan6days,calculatemonthly
//plancostanddailyplancost.Suggestmonthlyb/citisthecheaper
//one.
elseif(trip_duration<=30trip_duration6){
monthly_cost=70;
daily_cost=trip_duration*10;
suggested_plan='monthly';
}
//Whentripis<=6days,calculatedailyplancost.Suggestdaily
//plan.
elseif(trip_duration<=6trip_duration0){
monthly_cost=(Math.floor(trip_duration/30))*70;
daily_cost=trip_duration*10;
suggested_plan='daily';
}else{
//Thisshouldneverhappenb/ctrip_durationwouldhavetobe
//negative
suggested_plan='null';
}

res.status(200).send({
sessionInfo:{
parameters:{
monthly_cost:monthly_cost,
daily_cost:daily_cost,
suggested_plan:suggested_plan
}
}
});
break;

default:
console.log('default case called');
res.status(200).end();
break;
}
}
};

```

## Travel: baggage claim agent
This template helps end-users create or check the status of a claim related to lost, delayed, or damage baggage.
### Sample utterances
  * _Can you help me file a claim for the bag you lost?_
  * _I'd like to know the status of my damaged bag claim._
  * _When will my luggage arrive?_


### Webhook
This Cloud Functions webhook performs the following actions:
  * Verifies user and flight details.
  * Generates a claim ID and returns claim information.


package.json ```
{
  "name": "sample-http",
  "version": "0.0.1",
  "dependencies": {
    "moment": "2.27.0"
  }
}
    
```

index.js ```
constmoment=require('moment')
/**
* Responds to any HTTP request.
*
* @param {!express:Request} req HTTP request context.
* @param {!express:Response} res HTTP response context.
*/
exports.cxPrebuiltAgentsClaimStatus=(req,res)=>{
lettag=req.body.fulfillmentInfo.tag;
letpassenger_last_name;
if(!!tag){
switch(tag){
//CheckClaimStatustag
//ValidatesthattheclaimIDis'REF123456'
//Andthatthelastnameis'Garcia'
//Sendsbackastaticstatusmessage
case'claimStatus':
console.log(tag+' was triggered.')
letclaim_id=req.body.sessionInfo.parameters.claim_id;
passenger_last_name=req.body.sessionInfo.parameters.passenger_last_name;
letclaim_status;

if(claim_id=='REF123456'passenger_last_name=="Garcia"){
claim_status='valid';
}
else{
claim_status='invalid';
}
letclaim_status_message='Your lost bag claim is being processed and you should receive payment to your account ending in 6873 within 5-7 business days. '

res.status(200).send({
sessionInfo:{
parameters:{
claim_status:claim_status,
claim_status_message:claim_status_message
}
}
});
break;

//CasetosubmitanewclaimandgenerateaconfirmationID
//Validatesthattheflightnumber=AJ143,lastname=Garcia
//andreferenceid=1234567890123
//Ideallyyouwouldincludebetterlogic,thisisjustanexampleofaworkingwebhook
case'submitClaim':
console.log(tag+' was triggered.')
//Currentlynotusingthesetwoparametersbutjustanexample
letclaim_type=req.body.sessionInfo.parameters.claim_type;
letpassenger_flight_date=req.body.sessionInfo.parameters.passenger_flight_date;

//Calculatequalifyingrebateamountfordelayedbags
letrebate_amount=0
if(claim_type=='delayed'){
letdate_difference=Math.abs(moment(passenger_flight_date).diff(moment(),'days'));
//Capthequalifyingdaysat5
letrebate_qual_days=Math.min(date_difference,5)
//Anexampleofgiving$50perdayofdelay
rebate_amount=rebate_qual_days*50
}

//Theseparametersarebeingchecked
letpassenger_flight_number=req.body.sessionInfo.parameters.passenger_flight_number;
passenger_last_name=req.body.sessionInfo.parameters.passenger_last_name;
letpassenger_reference_id=req.body.sessionInfo.parameters.passenger_reference_id;
letclaim_confirmation_id;

if(passenger_flight_number=='AJ143'passenger_last_name=='Garcia'passenger_reference_id=='1234567890123'){
claim_filed=true;
//Generaterandom6digitnumbertoreturn
constrand_id=Math.floor(100000+Math.random()*900000)
claim_confirmation_id='REF'+rand_id.toString()
}else{
claim_filed=false;
}

res.status(200).send({
sessionInfo:{
parameters:{
claim_filed:claim_filed,
claim_confirmation_id:claim_confirmation_id,
rebate_amount:rebate_amount
}
}
});

break;
//Thisisthecasetoverifyformparametersthatgetupdatedthroughouttheconversation
case'verifyParameters':
//Capturenewlyupdatedformparameters
console.log(tag+' was triggered.')
letparams=req.body.pageInfo.formInfo.parameterInfo
letparamToValidate={name:'',value:''}

//Onlyvalidatetheformparameterifitwasjustcollected
for(letparamofparams){
if(param.justCollected==true){
console.log('Received parameter: ',param)
paramToValidate=param;
}
}

//ValidatePassengerReferenceID
//Must=='1234567890123'inordertocontinue
if(paramToValidate.displayName=='passenger_reference_id'){
if(paramToValidate.value!='1234567890123'){
paramToValidate.state='INVALID'
}else{
paramToValidate.state='VALID'
}
}

//ValidateFlightDate
//Mustbeonorbeforecurrentdate
if(paramToValidate.displayName=='passenger_flight_date'){
letflight_date=paramToValidate.value
letnow=moment()
if((moment(flight_date)<=now)){
paramToValidate.state='VALID'
}else{
paramToValidate.state='INVALID'
}
}

res.status(200).send({
pageInfo:{
formInfo:{
parameterInfo:[paramToValidate]
}
}
});
break;
default:
break;
}
}
};

```

## Travel: car rental agent
This template helps end-users start a new car rental reservation.
### Sample utterances
  * _I need to reserve a van._
  * _Hi, I'm traveling to LA for the weekend and I need to rent a car while I'm down there._
  * _I need help booking an SUV._


## Travel: flight information agent
This template helps end-users book and change tickets, find flight information, and request a refund.
### Sample utterances
  * _My flight XX4597 needs to be changed. Can you help me?_
  * _Can you help me find out the new departure time for my flight._
  * _What about the credit on my account from my cancelled flight?_
  * _Can you book my flight to San Francisco next month?_
  * _Book SFO 10am to MIA on August 10th, 2020 one way._


[ Previous Travel  ](https://docs.cloud.google.com/dialogflow/cx/docs/concept/playbook/prebuilt/travel)
[ Next Playbooks  ](https://docs.cloud.google.com/dialogflow/cx/docs/concept/playbook)
Send feedback 
Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.
Last updated 2026-03-05 UTC.
