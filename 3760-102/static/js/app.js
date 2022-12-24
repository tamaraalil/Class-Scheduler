$( document ).ready(function() {
	console.log( "ready! Page has rendered." );
  
  window.addEventListener("unload", function() {
    navigator.sendBeacon("/emptyFile", '');
  });

  document.getElementById("dwld").onclick = function(){
    var element = document.getElementById("wholeCal");
    let t = document.querySelector('.table-wrapper2');
    t.setAttribute('data-html2canvas-ignore','true');

    html2canvas(element, {backgroundColor:"#222529"}).then(function(canvas) {
      // https://www.digitalocean.com/community/tutorials/js-canvas-toblob
        canvas.toBlob(blob => {
          const anchor = document.createElement('a');
          anchor.download = 'schedule.jpg'; 
          anchor.href = URL.createObjectURL(blob);
      
          anchor.click(); 
      
          URL.revokeObjectURL(anchor.href); 
        },
        'image/jpeg',
        0.9,
        )
    });
  }
  document.getElementById("toggleimages").onclick = function(){
    var element = document.getElementById("images");
    if(element.style.display == "none")
    {
      element.style.display = "block";
    }
    else {
      element.style.display = "none";
    }
  }
});