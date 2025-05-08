//jquery//
var expr = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])+$/;
var expr1 = /((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,20})/
$(document).ready(function () {
  $("#registrof").submit(function (e) {
    let mensajesMostrar = "";
    let entrar = false;

    var nombre = $("#nombreregistro").val();
    if (nombre.trim().length < 4 || nombre.trim().length > 9) {
      mensajesMostrar +=
        "La longitud del nombre no es correcto(min 4 y max 9) <br>";
      entrar = true;
    }


    var celular = $("#celularregistro").val();
    if (!/^[9][0-9]{7,9}$/.test(celular)) {
      mensajesMostrar += "El número de celular debe comenzar con 9 y tener entre 8 y 10 dígitos en total.<br>";
      entrar = true;
    }
    


    //trim le quita los espacios en blanco//

    var letrainicial = nombre.charAt(0);
    if (!esMAYUSCULA(letrainicial)) {
      mensajesMostrar += "La primera letra del nombre es minuscula <br>";
      entrar = true;
    }

    var apellido = $("#apellidoregistro").val();
    if (apellido.trim().length < 4 || apellido.trim().length > 12) {
      mensajesMostrar +=
        "La longitud del apellido no es la correcta(min 4 y max 12) <br>";
      entrar = true;
    }

    var letrainicial1 = apellido.charAt(0);
    if (!esMAYUSCULA(letrainicial1)) {
      mensajesMostrar += "La primera letra del apellido es minuscula <br>";
      entrar = true;
    }

    var correoderegistro = $("#registrocorreo").val();
    if (correoderegistro == ""|| !expr.test(correoderegistro)) {
      mensajesMostrar += "El correo debe cumplir el siguiente formato (texto) , @ , gmail , . ,com/cl/etc para poder ser enviado <br>";
      entrar = true;
    }







    var contraseña = $("#contraseñaregistro").val();
    if (contraseña == ""|| !expr1.test(contraseña)) {
      mensajesMostrar += " EN EL APARTADO DE LA CONTRASEÑA: <br> Por favor ingrese al menos 8 caracteres <br>Por favor ingrese no más de 20 caracteres<br>Por favor ingrese algunas letras Minusculas y Mayusculas <br> Por favor introduzca algunos simbolos especiales <br>";
      entrar = true;
    }

    


    var letrainicial2 = contraseña.charAt(0);
    if (!esMAYUSCULA(letrainicial2)) {
      mensajesMostrar +=
        "La primera letra de la contraseña debe de ser una letra mayuscula<br>";
      entrar = true;
    }

    var contraseñaconfirmar = $("#confirmarcontraseñaregistro").val();
    if (contraseñaconfirmar != contraseña) {
      mensajesMostrar += "Las contraseñas no coinciden <br>";
      entrar = true;
    }




    
    if (entrar) {
      console.log("entrar");
      e.preventDefault();
      $("#mensajes").html(mensajesMostrar);
    } else {
      console.log("else");
      $("#mensajes").html("formulario enviado");
    }
  });

  function esMAYUSCULA(letra) {
    return letra == letra.toUpperCase();
  }
});