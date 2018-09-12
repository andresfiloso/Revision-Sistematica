/*
Template Name: Monster Admin
Author: Themedesigner
Email: niravjoshi87@gmail.com
File: js
*/
$(function() {
    "use strict";
      $(".tst1").click(function(){
           $.toast({
            heading: 'Welcome to Monster admin',
            text: 'Use the predefined ones, or specify a custom position object.',
            position: 'top-right',
            loaderBg:'#ff6849',
            icon: 'info',
            hideAfter: 3000, 
            stack: 6
          });

     });

      $(".tst2").click(function(){
           $.toast({
            heading: 'Welcome to Monster admin',
            text: 'Use the predefined ones, or specify a custom position object.',
            position: 'top-right',
            loaderBg:'#ff6849',
            icon: 'warning',
            hideAfter: 3500, 
            stack: 6
          });

     });
      $(".saveClassify").click(function(){
           $.toast({
            heading: 'Articulo guardado con exito!',
            text: '',
            position: 'top-right',
            loaderBg:'#ff6849',
            icon: 'success',
            hideAfter: 3500, 
            stack: 6
          });

     });

      $(".saveArticle").click(function(){
           $.toast({
            heading: 'Articulo agregado con exito!',
            text: 'Vas a poder clasificarlo accediendo al proyecto',
            position: 'top-right',
            loaderBg:'#ff6849',
            icon: 'success',
            hideAfter: 3500, 
            stack: 6
          });

     });

      $(".deleteArticle").click(function(){
           $.toast({
            heading: 'Articulo eliminado de la busqueda',
            text: 'El articulo no aparecera mas en los resultados. Puede aparecer nuevamente si haces una nueva busqueda',
            position: 'top-right',
            loaderBg:'#ff6849',
            icon: 'error',
            hideAfter: 5000, 
            stack: 6
          });

     });

});
          
