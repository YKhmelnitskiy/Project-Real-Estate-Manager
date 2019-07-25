$.datetimepicker.setDateFormatter({
    parseDate: function (date, format) {
        var d = moment(date, format);
        return d.isValid() ? d.toDate() : false;
    },
    formatDate: function (date, format) {
        return moment(date).format(format);
    },
});

$('.datetime').datetimepicker({
    format:'DD-MM-YYYY hh:mm A',
    formatTime:'hh:mm A',
    formatDate:'DD-MM-YYYY',
    useCurrent: false,
});

// Initialise Pusher
const pusher = new Pusher("71fa2dc10281921e8d02", {
    cluster: 'us2',
    encrypted: true
});

var channel = pusher.subscribe('table');

channel.bind('new-record', (data) => {

    const check_in = moment(`${data.data.Closing_Date}`, 'DD/MM/YYYY hh:mm a').format('YYYY-MM-DD hh:mm:ss a')
    const departure = moment(`${data.data.departure}`, 'DD/MM/YYYY hh:mm a').format('YYYY-MM-DD hh:mm:ss a')
   $('#flights').append(`
        <tr id="${data.data.id}">
            <th scope="row"> ${data.data.Seller} </th>
            <td> ${data.data.Buyer} </td>
            <td> ${Sold_Price} </td>
            <td> ${Closing_Date} </td>
            <td> ${Type} </td>
            <td> ${Status} </td>
            <td> ${Address} </td>
        </tr>
   `)
});

channel.bind('update-record', (data) => {

    const check_in = moment(`${data.data.Closing_Date}`, 'DD/MM/YYYY hh:mm a').format('YYYY-MM-DD hh:mm:ss a')

    $(`#${data.data.id}`).html(`
        <th scope="row"> ${data.data.Seller} </th>
        <td> ${data.data.Buyer} </td>
        <td> ${Sold_Price}
        <td> ${Closing_Date} </td>
        <td> ${Type} </td>
        <td> ${Status}
        <td> ${Address} </td>
    `)

 });

 $(".submit").click(function() {
     alert("ok")
    
 });