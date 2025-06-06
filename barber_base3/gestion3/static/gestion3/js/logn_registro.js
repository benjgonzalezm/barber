document.addEventListener('DOMContentLoaded', function () {
            const btnIniciar = document.getElementById('btnIniciar');
            const submenuIniciar = document.getElementById('submenuIniciar');

            btnIniciar.addEventListener('click', function (e) {
                e.stopPropagation(); 
                if (submenuIniciar.style.display === 'none' || submenuIniciar.style.display === '') {
                    submenuIniciar.style.display = 'block';
                } else {
            submenuIniciar.style.display = 'none';
                }
          });

   
            document.addEventListener('click', function () {
                submenuIniciar.style.display = 'none';
            });
         });