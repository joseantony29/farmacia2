let form_almacen = document.getElementById('form_almacen');

let getData = async () => {
    // PROVIDERS LIST
    await getDataTable(
        // paging
        true,
        // searching
        true,
        // ordering
        true,
        '#listado_almacen',
        {
            'action': 'search_almacen',
        },
        [
            {"data": "id"},
            {"data": "nombre"},
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
        '/listado-de-almacenes/'
    );

}


$( async function () {
    await getData();

	// ALMACEN SEND FORM
	form_almacen.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_almacen);
        await SendDataJsonForm(type_actions['almacen'][action.value], parameters, async () => {  
            await getData();
            $('#smallmodal').modal('hide');   
            $("#form_almacen")[0].reset(); 
        });
    });

    // REGISTER ALMACEN
    $('#btn_nuevo_almacen').on('click', function () {
        $('#form_almacen')[0].reset();
        $('input[name="action"]').val('nuevo_almacen');
        $('#smallmodal').modal('show');
    });

    // ALMACEN EDIT
    $('#listado_almacen tbody').on('click', 'a[rel="edit"]', function () {
        $('#form_almacen')[0].reset();
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();

        $('input[name="action"]').val('edit_almacen');
        $('input[name="id"]').val(data.id);
        $('input[name="nombre"]').val(data.nombre);

        $('#smallmodal').modal('show');
    });
    
});