let form_tipo_insu = document.getElementById('form_tipo_insu');

let getData = async () => {
    // PROVIDERS LIST
    await getDataTable(
        // paging
        true,
        // searching
        true,
        // ordering
        true,
        '#lista_tipo_ins',
        {
            'action': 'search_tipo_ins',
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
        '/listado-de-insumos/'
    );

}


$( async function () {
    await getData();

	// TIPO INSUMO SEND FORM
	form_tipo_insu.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_tipo_insu);
        await SendDataJsonForm(type_actions['type_ins'][action.value], parameters, async () => {  
            await getData();
            $('#smallmodal').modal('hide');   
            $("#form_tipo_insu")[0].reset(); 
        });
    });

    // REGISTER TIPO DE INSUMO
    $('#btn_tipo_insu').on('click', function () {
        $('#form_tipo_insu')[0].reset();
        $('input[name="action"]').val('nuevo_tipo_insu');
        $('#smallmodal').modal('show');
    });

    // TIPOS DE INSUMOS EDIT
    $('#lista_tipo_ins tbody').on('click', 'a[rel="edit"]', function () {
        $('#form_tipo_insu')[0].reset();
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();

        $('input[name="action"]').val('edit_t_ins');
        $('input[name="id"]').val(data.id);
        $('input[name="nombre"]').val(data.nombre);

        $('#smallmodal').modal('show');
    });
    
});