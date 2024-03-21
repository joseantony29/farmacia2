let form_lab = document.getElementById('form_lab');

let getData = async () => {
    // PROVIDERS LIST
    await getDataTable(
        // paging
        true,
        // searching
        true,
        // ordering
        true,
        '#lista_lab',
        {
            'action': 'search_labs',
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
                    let buttons = '<a href="#" rel="edit" class="btn btn-icon btn-dark" data-bs-toggle="tooltip" data-bs-placement="top" title="Editar Laboratorio"><i class="fa fa-edit"></i></a>';
                    return buttons
                }
            },
        ],
        '/listado-de-laboratorios/'
    );

}


$( async function () {
    await getData();

	// LABS SEND FORM
	form_lab.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_lab);
        await SendDataJsonForm(type_actions['labs'][action.value], parameters, async () => {  
            await getData();
            $('#smallmodal').modal('hide');   
            $("#form_lab")[0].reset(); 
        });
    });

    // REGISTER LABS
    $('#btn_add_labs').on('click', function () {
        $('#form_lab')[0].reset();
        $('input[name="action"]').val('nuevo_lab');
        $('#smallmodal').modal('show');
    });

    // LABS EDIT
    $('#lista_lab tbody').on('click', 'a[rel="edit"]', function () {
        $('#form_lab')[0].reset();
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();

        $('input[name="action"]').val('edit_lab');
        $('input[name="id"]').val(data.id);
        $('input[name="nombre"]').val(data.nombre);

        $('#smallmodal').modal('show');
    });
    
});