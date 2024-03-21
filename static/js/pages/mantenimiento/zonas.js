let form_zonas = document.getElementById('form_zonas');

let getData = async () => {
    // tipo de movimiento LIST
    await getDataTable(
        // paging
        true,
        // searching
        true,
        // ordering
        true,
        '#listado_zonas',
        {
            'action': 'search_zonas',
        },
        [
            {"data": "id"},
            {"data": "zona_residencia"},
            {"data": "id"},
        ],
        [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="#" rel="edit" class="btn btn-icon btn-dark" data-bs-toggle="tooltip" data-bs-placement="top" title="Editar zonas"><i class="fa fa-edit"></i></a>';
                    return buttons
                }
            },
        ],
        '/listado-de-zonas/'
    );

}


$( async function () {
    await getData();

	// TIPO MOVIMIENTO SEND FORM
	form_zonas.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_zonas);
        await SendDataJsonForm(type_actions['zonas'][action.value], parameters, async () => {  
            await getData();
            $('#smallmodal').modal('hide');   
            $("#form_zonas")[0].reset(); 
        });
    });

    // REGISTER TIPO MOVIMIENTO
    $('#btn_nueva_zona').on('click', function () {
        $('#form_zonas')[0].reset();
        $('input[name="action"]').val('nueva_zona');
        $('#smallmodal').modal('show');
    });

    // TIPO MOVIMIENTO EDIT
    $('#listado_zonas tbody').on('click', 'a[rel="edit"]', function () {
        $('#form_zonas')[0].reset();
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();

        $('input[name="action"]').val('edit_zona');
        $('input[name="id"]').val(data.id);
        $('input[name="zona_residencia"]').val(data.zona_residencia);

        $('#smallmodal').modal('show');
    });
    
});