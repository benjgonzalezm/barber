document.addEventListener('DOMContentLoaded', function () {
    const btnIniciar = document.getElementById('btnIniciar');
    const submenuIniciar = document.getElementById('submenuIniciar');
    
    const btnOpciones = document.getElementById('btnOpciones');
    const submenuOpciones = document.getElementById('submenuOpciones');

    function toggleMenu(submenu) {
        submenuIniciar.classList.remove('activo');
        submenuOpciones.classList.remove('activo');

        if (!submenu.classList.contains('activo')) {
            submenu.classList.add('activo');
        }
    }

    btnIniciar.addEventListener('click', function (e) {
        e.stopPropagation();
        console.log('Click en Iniciar');
        toggleMenu(submenuIniciar);
    });

    btnOpciones.addEventListener('click', function (e) {
        e.stopPropagation();
        console.log('Click en Administrar');
        toggleMenu(submenuOpciones);
    });

    document.addEventListener('click', function () {
        submenuIniciar.classList.remove('activo');
        submenuOpciones.classList.remove('activo');
    });

    submenuIniciar.addEventListener('click', function (e) {
        e.stopPropagation();
    });

    submenuOpciones.addEventListener('click', function (e) {
        e.stopPropagation();
    });
});




