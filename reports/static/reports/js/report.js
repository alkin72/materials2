var minDate, maxDate;

    moment.updateLocale('ru', {
        longDateFormat: {
            LLL : 'D MMMM, HH:mm', // 6 окт., 16:27
        }
    });
// Custom filtering function which will search data in column four between two values
$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {

        var min = minDate.val();
        var max = maxDate.val();
        var date = new Date( data[3] );

        if (
            ( min === null && max === null ) ||
            ( min === null && date <= max ) ||
            ( min <= date   && max === null ) ||
            ( min <= date   && date <= max )
        ) {
            return true;
        }
        return false;
    }
);



$(document).ready(function() {
    // Create date inputs

    minDate = new DateTime($('#min'), {
        format: 'll'
    });

    maxDate = new DateTime($('#max'), {
        format: 'll'
    });

    // DataTables initialisation
//    var table = $('#dt-table').DataTable();
    var table = $('#dt-table').DataTable({
            language: {
                url: '//cdn.datatables.net/plug-ins/1.12.1/i18n/ru.json',
            },
        });

    // Refilter the table
    $('#min, #max').on('change', function () {
        table.draw();
    });
});



