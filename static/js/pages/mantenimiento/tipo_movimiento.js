let form_tipo_movi = document.getElementById('form_tipo_movi');

let getData = async () => {
    // tipo de movimiento LIST
    await getDataTable(
        // paging
        true,
        // searching
        true,
        // ordering
        true,
        '#listado_tipo_movi',
        {
            'action': 'search_tipo_mov',
        },
        [
            {"data": "id"},
            {"data": "nombre"},
            {"data": "operacion"},
            {"data": "id"},
        ],
        [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="#" rel="edit" class="btn btn-icon btn-dark" data-bs-toggle="tooltip" data-bs-placement="top" title="Editar tipo de insumo"><i class="fa fa-edit"></i></a>';
                    return buttons
                }
            },
        ],
        '/listado-de-tipos-movimientos/'
    );

}


$( async function () {
    await getData();

	// TIPO MOVIMIENTO SEND FORM
	form_tipo_movi.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_tipo_movi);
        await SendDataJsonForm(type_actions['tipo_movi'][action.value], parameters, async () => {  
            await getData();
            $('#smallmodal').modal('hide');   
            $("#form_tipo_movi")[0].reset(); 
        });
    });

    // REGISTER TIPO MOVIMIENTO
    $('#btn_tipo_movi').on('click', function () {
        $('#form_tipo_movi')[0].reset();
        $('input[name="action"]').val('nuevo_tipo_movi');
        $('#smallmodal').modal('show');
    });

    // TIPO MOVIMIENTO EDIT
    $('#listado_tipo_movi tbody').on('click', 'a[rel="edit"]', function () {
        $('#form_tipo_movi')[0].reset();
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();

        $('input[name="action"]').val('edit_tipo_movi');
        $('input[name="id"]').val(data.id);
        $('input[name="nombre"]').val(data.nombre);
        $('select[name="operacion"]').val(data.operacion);

        $('#smallmodal').modal('show');
    });
    
});